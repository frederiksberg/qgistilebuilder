import argparse
import uuid
import logging
import os
from process import buildmbtiles
import sftp

# Set up arg parsing
parser = argparse.ArgumentParser(description="Builds MBTiles and uploads them to tilehut")
parser.add_argument("-p", "--project", type=str, help="The absolute path of the QGIS project")
parser.add_argument("--minzoom", type=int, help="The minimum zoom level")
parser.add_argument("--maxzoom", type=int, help="The maximum zoom level")
parser.add_argument("--extend", type=str, help="The of the mbtiles file.")

try:
    ns = parser.parse_args()
except:
    logging.error("An error occurred while parsing arguments")
    exit(1)

name = os.path.splitext(os.path.basename(ns.project))[0]

logging.basicConfig(
    level=logging.INFO,
    filename="/var/log/tilebuilder.log",
    filemode="a",
    format=f"[%(levelname)s]:[{name}]:[%(asctime)s] => %(message)s"
    )

logging.info(f"Processing {ns.project}")

try:
    filepath = buildmbtiles(
        ns.project,
        ns.minzoom,
        ns.maxzoom,
        ns.extend,
        f"/opt/tiles/{name}.mbtiles"
    )
except:
    exit(1)

logging.info(f"MBTiles file saved to {filepath}")

logging.info("Starting upload of mbtiles file")
try:
    sftp.upload(filepath)
except Exception as e:
    logging.error(str(e))
    os.remove(filepath)
    exit(1)

os.remove(filepath)
logging.info("Deleting mbtiles file")