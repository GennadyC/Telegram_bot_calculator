#!/usr/bin/env python
from google.cloud import dialogflow
import json
import enchant
import string
import requests


SYMBOLS = ["?", "!", ".", ",", ":", "-"]


class Helper:
    def __init__(self):
        self.latest_error_request = ''
        try:
            self.enchant = enchant.Dict("ru_RU")
            self.activity = True
        except enchant.errors.DictNotFoundError:
            print('Добавьте поддержу русского языка')
            self.activity = False

    def check_errors(self, request:str)->list:
        if self.activity and self.latest_error_request != request:
            list_request = request.split()
            for i in list_request:
                if not self.enchant.check(i):
                    self.latest_error_request = request
                    return {'status': False, 'word_with_error': i, 'options': self.enchant.suggest(i)}
        self.latest_error_request = ''
        return {'status': True}
    
    def remove_punctuation_marks(self, message):
        for s in SYMBOLS:
            message = message.replace(s, "")
        return message
    
    def google_ckeck(self, message):
        xml = """
        <?xml version="1.0" encoding="UTF-8" ?><br/>
        <spellrequest textalreadyclipped="0" ignoredups="0" ignoredigits="1" ignoreallcaps="1"><br/>
         <text>%s</text><br/>
        </spellrequest>
        """ % message

        response = requests.post("https://google.com/tbproxy/spell?lang=ru", data=xml.encode('utf-8'))


class Spellchecking:
    def __init__(self, project_id):
        self.helper = Helper()
        self.intents_client = dialogflow.IntentsClient()
        self.project_id = project_id
        self.found = False
    
    def execute(self):
        parent = dialogflow.AgentsClient.agent_path(self.project_id)
        intents = self.intents_client.list_intents(request={'parent': parent})
        for intent in intents:
            messages = intent.messages[0].text.text

            for message in messages:
                clean_message = self.helper.remove_punctuation_marks(message)
                result = self.helper.check_errors(clean_message)
                if not result['status']:
                    self.found = True
                    error = 'В намерение "%s" найдена ошибка "%s". Сообщение: "%s" \n' % (intent.display_name, result['word_with_error'], message)
                    print(error)
        
        if not self.found:
            print('Ошибок не найдено')

