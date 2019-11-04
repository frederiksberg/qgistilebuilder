import argparse
import uuid
import logging
from process import buildmbtiles
import sftp

def printerror(str):
    with open("/var/log/tilebuilder.err", "w") as fp:
        fp.write(str)

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
    printerror("A fatal error occurred while parsing arguments")
    exit(1)

logging.basicConfig(
    level=logging.INFO,
    filename="/var/log/tilebuilder.info",
    filemode="w",
    format="[%(levelname)s] => %(message)s"
    )

logging.info(f"Processing {ns.project}")

try:
    filepath = buildmbtiles(
        ns.project,
        ns.minzoom,
        ns.maxzoom,
        ns.extend,
        f"/opt/tiles/{str(uuid.uuid4())}.mbtiles"
    )
except:
    printerror("A fatal error occured while building tiles")
    exit(1)

logging.info(f"MBTiles file saved to {filepath}")

try:
    sftp.upload(filepath)
except:
    printerror("Error during sftp upload")
    exit(1)
