import pysftp
import configparser
import logging
import paramiko
from base64 import decodebytes

def upload(file):
    try:
        parser = configparser.ConfigParser()
        parser.read("../conf.ini")
        conf = parser["SFTP"]
    except:
        logging.error("An error occured while parsing the sftp config file")
        raise ValueError("Config parsing error")
    
    try:
        keydata = bytes(conf["known_host"])
        key = paramiko.RSAKey(data=decodebytes(keydata))

        cnopts = pysftp.CnOpts()
        cnopts.hostkeys.add("th.frb-data.dk", "ssh-rsa", key)

        with pysftp.Connection(
            host=conf["host"],
            username=conf["user"],
            private_key=conf["private_key"],
            private_key_pass=conf["private_key_pass"],
            cnopts=cnopts
        ) as sftp:
            with sftp.cd("tiles"):
                sftp.put(file)
    except Exception as e:
        logging.error("An error occured while uploading file via sftp")
        logging.error(str(e))
        raise ValueError("SFTP Error")
