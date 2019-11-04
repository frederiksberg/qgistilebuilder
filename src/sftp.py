import pysftp
import configparser

parser = configparser.ConfigParser()
parser.read("../conf.ini")

print(parser.sections())
