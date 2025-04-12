# -*- coding: utf-8 -*-
"""
Script developed by Mohamed RIZKI
Description: This script allows you to select a layout, a layer, and specify the zoom dimensions as well as the export path
"""

from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterEnum,
    QgsProcessingParameterMapLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFileDestination,
    QgsProject,
    QgsLayoutItemMap,
    QgsRectangle,
    QgsLayoutExporter
)
from qgis.PyQt.QtCore import QCoreApplication

class EasyExportAlgorithm(QgsProcessingAlgorithm):
    # Définition des paramètres de l'algorithme
    LAYOUT = 'LAYOUT'
    LAYER = 'LAYER'
    OVERLAP_HORIZONTAL = 'OVERLAP_HORIZONTAL'
    OVERLAP_VERTICAL = 'OVERLAP_VERTICAL'
    EXPORT_PATH = 'EXPORT_PATH'

    def initAlgorithm(self, config=None):
        """
        Initialisation des paramètres de l'algorithme
        """
        # Paramètre pour sélectionner un layout
        self.addParameter(
            QgsProcessingParameterEnum(
                self.LAYOUT,
                self.tr('Sélectionner un Layout'),
                options=self.get_layout_names(),
                optional=False
            )
        )
        
        # Paramètre pour sélectionner une couche à exclure
        self.addParameter(
            QgsProcessingParameterMapLayer(
                self.LAYER,
                self.tr('Couche à ne pas prendre en compte (Optionnel)'),
                optional=True
            )
        )

        # Paramètres pour le chevauchement horizontal et vertical
        self.addParameter(
            QgsProcessingParameterNumber(
                self.OVERLAP_HORIZONTAL,
                self.tr('Chevauchement Horizontal (%)'),
                type=QgsProcessingParameterNumber.Double,
                optional=True,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.OVERLAP_VERTICAL,
                self.tr('Chevauchement Vertical (%)'),
                type=QgsProcessingParameterNumber.Double,
                optional=True,
                defaultValue=0
            )
        )

        # Paramètre pour le chemin d'exportation
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.EXPORT_PATH,
                self.tr('Chemin d\'exportation'),
                fileFilter='PDF files (*.pdf)'
            )
        )

    def get_layout_names(self):
        """
        Récupérer les noms des layouts disponibles dans le projet
        """
        project = QgsProject.instance()
        layout_manager = project.layoutManager()
        layouts = layout_manager.printLayouts()
        layout_names = [layout.name() for layout in layouts]
        return layout_names

    def get_layout_dimensions(self, layout_name):
        """
        Obtenir les dimensions du layout sélectionné
        """
        project = QgsProject.instance()
        layout_manager = project.layoutManager()
        layouts = layout_manager.printLayouts()
        for layout in layouts:
            if layout.name() == layout_name:
                for item in layout.items():
                    if isinstance(item, QgsLayoutItemMap):
                        rect = item.extent().toRectF()
                        return rect.width(), rect.height()
        return 0, 0

    def get_visible_extent(self, excluded_layer):
        """
        Calculer l'étendue englobante des couches visibles, en excluant la couche spécifiée
        """
        project = QgsProject.instance()
        layer_tree = project.layerTreeRoot()
        extent = QgsRectangle()

        for layer in project.mapLayers().values():
            if layer != excluded_layer and layer_tree.findLayer(layer.id()).isVisible():
                layer_extent = layer.extent()
                extent.combineExtentWith(layer_extent)

        return extent

    def divide_extent(self, extent, width, height, overlap_h, overlap_v):
        """
        Diviser l'étendue en fonction des dimensions du layout et des chevauchements
        """
        step_x = width * (1 - overlap_h / 100.0)
        step_y = height * (1 - overlap_v / 100.0)
        
        cols = int(extent.width() / step_x) + 1
        rows = int(extent.height() / step_y) + 1
        divided_extents = []

        for col in range(cols):
            for row in range(rows):
                x_min = extent.xMinimum() + col * step_x
                x_max = min(x_min + width, extent.xMaximum())
                y_min = extent.yMinimum() + row * step_y
                y_max = min(y_min + height, extent.yMaximum())
                divided_extents.append(QgsRectangle(x_min, y_min, x_max, y_max))

        return divided_extents

    def processAlgorithm(self, parameters, context, feedback):
        """
        Traitement principal de l'algorithme
        """
        layout_index = self.parameterAsEnum(parameters, self.LAYOUT, context)
        layout_name = self.get_layout_names()[layout_index]
        
        excluded_layer = self.parameterAsLayer(parameters, self.LAYER, context)
        overlap_h = self.parameterAsDouble(parameters, self.OVERLAP_HORIZONTAL, context)
        overlap_v = self.parameterAsDouble(parameters, self.OVERLAP_VERTICAL, context)
        export_path = self.parameterAsString(parameters, self.EXPORT_PATH, context)

        # Obtenir les dimensions du layout sélectionné
        layout_width, layout_height = self.get_layout_dimensions(layout_name)
        feedback.pushInfo(f"Dimensions du layout - Largeur : {layout_width} m, Hauteur : {layout_height} m")

        # Calculer l'étendue englobante des couches visibles
        visible_extent = self.get_visible_extent(excluded_layer)
        feedback.pushInfo(f"Étendue calculée - xMin: {visible_extent.xMinimum()}, xMax: {visible_extent.xMaximum()}, yMin: {visible_extent.yMinimum()}, yMax: {visible_extent.yMaximum()}")

        # Diviser l'étendue en fonction des dimensions du layout et des chevauchements
        divided_extents = self.divide_extent(visible_extent, layout_width, layout_height, overlap_h, overlap_v)

        info_text = f'Layout sélectionné : {layout_name}\n'
        info_text += f'Couche exclue : {excluded_layer.name() if excluded_layer else "Aucune"}\n'
        info_text += f'Pourcentage de chevauchement horizontal : {overlap_h} %\n'
        info_text += f'Pourcentage de chevauchement vertical : {overlap_v} %\n'
        info_text += f'Chemin d\'exportation : {export_path}\n'
        info_text += f'Nombre de pages exportées : {len(divided_extents)}\n'
        
        feedback.pushInfo(info_text)
        
        # Logique d'exportation des cartes
        pages_with_data = 0

        for i, extent in enumerate(divided_extents):
            output_file = f"{export_path}_{i + 1}.pdf"
            feedback.pushInfo(f"Exportation vers {output_file}")

            if self.has_data_in_extent(extent, excluded_layer):
                self.export_map(layout_name, extent, output_file, context, feedback)
                pages_with_data += 1
            
        feedback.pushInfo(f'Nombre de pages exportées avec données : {pages_with_data}')
        
        return {}

    def has_data_in_extent(self, extent, excluded_layer):
        """
        Vérifier si l'étendue spécifiée contient des données
        """
        project = QgsProject.instance()
        for layer in project.mapLayers().values():
            if layer != excluded_layer:
                layer_extent = layer.extent()
                if layer_extent.intersects(extent):
                    return True
        return False

    def export_map(self, layout_name, extent, output_file, context, feedback):
        """
        Exporter la carte pour l'étendue spécifiée
        """
        project = QgsProject.instance()
        layout_manager = project.layoutManager()
        original_layout = layout_manager.layoutByName(layout_name)

        if original_layout is None:
            feedback.reportError(f"Layout {layout_name} non trouvé.")
            return

        # Créer une copie temporaire du layout pour l'exportation
        temp_layout = original_layout.clone()
        temp_layout.setName(f"{layout_name}_temp")

        for item in temp_layout.items():
            if isinstance(item, QgsLayoutItemMap):
                item.setExtent(extent)
                temp_layout.refresh()
                exporter = QgsLayoutExporter(temp_layout)
                result = exporter.exportToPdf(output_file, QgsLayoutExporter.PdfExportSettings())
                if result != QgsLayoutExporter.Success:
                    feedback.reportError(f"Échec de l'exportation vers {output_file}")

        # Supprimer la copie temporaire du layout
        layout_manager.removeLayout(temp_layout)

    def name(self):
        return 'easyexportalgorithm'

    def displayName(self):
        return self.tr('EasyExport')

    def group(self):
        return self.tr('Mes Scripts')

    def groupId(self):
        return 'mes_scripts'

    def createInstance(self):
        return EasyExportAlgorithm()

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

# Enregistrer l'algorithme dans le registre de traitement
if __name__ == "__main__":
    import sys
    from qgis.core import QgsApplication

    app = QgsApplication([], False)
    app.initQgis()

    alg = EasyExportAlgorithm()
    QgsApplication.processingRegistry().addAlgorithm(alg)

    # Si vous exécutez ce script directement, utilisez le Processing Toolbox pour l'exécuter
    if not QgsApplication.instance().pluginManager().isPluginLoaded('processing'):
        QgsApplication.instance().pluginManager().loadPlugin('processing')
        QgsApplication.instance().pluginManager().initProcessing()

    processing.run("mes_scripts:easyexportalgorithm", {})
    
    app.exitQgis()
    app.exit()
