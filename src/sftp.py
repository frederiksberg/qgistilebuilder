import pysftp
import configparser
import logging


def upload(file):
    try:
        parser = configparser.ConfigParser()
        parser.read("../conf.ini")
        conf = parser["SFTP"]
    except:
        logging.error("An error occured while parsing the sftp config file")
        raise ValueError("Config parsing error")
    
    try:
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None

        with pysftp.Connection(
            host=conf["host"],
            username=conf["user"],
            password=conf["password"],
            private_key=conf["private_key"],
            private_key_pass=conf["private_key_pass"],
            cnopts=cnopts
        ) as sftp:
            with sftp.cd("tiles"):
                sftp.put(file)
    except:
        logging.error("An error occured while uploading file via sftp")
        raise ValueError("SFTP Error")
