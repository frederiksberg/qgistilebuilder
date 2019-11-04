import qgis
import os
import sys
import logging
from qgis.core import QgsApplication, QgsProject, QgsProcessingFeedback
from qgis.gui import QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt5.QtGui import QColor

def buildmbtiles(project, minzoom, maxzoom, extend, outname):
    # Initialize QGIS
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    QgsApplication.setPrefixPath("/usr", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # Load project
    try:
        proj = QgsProject.instance()
        proj.read(project)
    except:
        logging.error(f"There was an error loading {project}")
        raise ValueError("Error loading QGIS project")

    # Initialize processing
    sys.path.append("/usr/share/qgis/python/plugins")
    import processing
    from processing.core.Processing import Processing
    Processing.initialize()

    # Call procedure
    params = {
        'EXTENT': extend,
        'ZOOM_MIN':minzoom,
        'ZOOM_MAX':maxzoom,
        'DPI':96,
        'BACKGROUND_COLOR': QColor(0,0,0,0),
        'TILE_FORMAT':1,
        'QUALITY':75,
        'METATILESIZE':4,
        'OUTPUT_FILE': outname
    }
    feedback = QgsProcessingFeedback()
    res = processing.run("qgis:tilesxyzmbtiles", params, feedback=feedback)

    # Clean up and return
    qgs.exitQgis()

    return res["OUTPUT_FILE"]
