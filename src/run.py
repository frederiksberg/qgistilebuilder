import argparse
import uuid
import logging
from process import buildmbtiles

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

logging.basicConfig(
    level=logging.INFO,
    filename="/var/log/tilebuilder.log",
    filemode="w",
    format="[%(levelname)s] => %(message)s"
    )

logging.info(f"Processing {ns.project}")

filepath = buildmbtiles(
    ns.project,
    ns.minzoom,
    ns.maxzoom,
    ns.extend,
    f"/opt/tiles/{str(uuid.uuid4())}.mbtiles"
)

logging.info(f"MBTiles file saved to {filepath}")

# TODO: SFTP
