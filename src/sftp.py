import pysftp
import configparser



def test():
    parser = configparser.ConfigParser()
    parser.read("../conf.ini")

    print(parser.sections())
