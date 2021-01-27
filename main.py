import configparser
import argparse
import sys
import json
import os


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-task', '--task', required=True, choices=['spellchecking', 'profanity', 'generate'] , help='Spell checking in bot responses')

try:
    param = parser.parse_args()
except IOError as msg:
    parser.error(str(msg))

config = configparser.ConfigParser()
config.read('config.ini')
project_id = config['DIALOGFLOW']['project_id']
path_to_key = config['DIALOGFLOW']['path_to_key']

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_to_key


if param.task == 'spellchecking':
    from spellchecking import Spellchecking
    spellchecking = Spellchecking(project_id)
    spellchecking.execute()
elif param.task == 'profanity':
    if os.name != 'nt':
        from profanity import Profanity
        slang_detected = Profanity(project_id)
        slang_detected.execute()
    else:
        print('Данная операция не поддерживается на Windows')
        exit(0)
elif param.task == 'generate':
    from text_generate import Generator
    generator = Generator(project_id)
    generator.execute()
