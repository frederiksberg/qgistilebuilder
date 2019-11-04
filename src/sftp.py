import pysftp
import configparser
import logging
import paramiko
from base64 import decodebytes

def upload(file):
    try:
        parser = configparser.ConfigParser()
        parser.read("/opt/conf.ini")
        conf = parser["SFTP"]
    except:
        logging.error("An error occured while parsing the sftp config file")
        raise ValueError("Config parsing error")
    
    cnopts = pysftp.CnOpts()
    # Workaround for using non-standard ports
    if conf["port"] != "22":
        
        hostname_np = conf["host"]
        hostname_p = f"[{hostname_np}]:{conf['port']}"

        host_key_type = host_key_value = None
        # Look up hostkey
        
        for hostname in [hostname_np, hostname_p]:
            try:
                host_key_set = cnopts.hostkeys[hostname]
            except KeyError:
                pass
            else:
                host_key_type, host_key_value = next(iter(host_key_set.items()))

        cnopts.hostkeys.add(hostname_np, host_key_type, host_key_value)

    try:
        with pysftp.Connection(
            host=conf["host"],
            port=int(conf["port"]),
            username=conf["user"],
            private_key=conf["private_key"],
            private_key_pass=conf["private_key_pass"],
            cnopts=cnopts
        ) as sftp:
            logging.info("Connection established")
            with sftp.cd("tiles"):
                sftp.put(file)
        logging.info("File uploaded succesfully!")
    except Exception as e:
        logging.error("An error occured while uploading file via sftp")
        logging.error(str(e))
        raise ValueError("SFTP Error")
