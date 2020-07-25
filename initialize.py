import fxcmpy
import configparser

config = configparser.ConfigParser()
config.read('credentials.cfg')
token = config['FXCM']['api_token']

con = fxcmpy.fxcmpy(access_token=token, log_level='error', server='demo')