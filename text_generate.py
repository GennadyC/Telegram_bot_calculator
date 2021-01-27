import random
from google.cloud import dialogflow


class Dictogram(dict):
    def __init__(self, iterable=None):
        super(Dictogram, self).__init__()
        if iterable:
            self.update(iterable)

    def update(self, iterable, **kwargs):
        for i in iterable:
            if i in self:
                self[i] += 1
            else:
                self[i] = 1

    def get_weighted_random_word(self):
        weight = self._get_random_weight()
        return self._get_random_item_by_weight(weight)[0]

    def _get_random_weight(self):
        weight_limit = sorted(self.items(), key=lambda x: x[1], reverse=True)[0][1]
        return random.randint(1, weight_limit)

    def _get_random_item_by_weight(self, weight):
        items = [i for i in self.items() if i[1] >= weight]
        return random.sample(items, 1)[0]


class MarkovChain:
    def __init__(self, order=1):
        self.model = {}
        self.N = order

    def parse_and_add(self, string):
        data = []
        words = [w.strip() for w in string.split()]
        is_end_of_sentence = False
        for word in words:
            data.append(word)
            if is_end_of_sentence:
                self.add(data)
                data = [word]
                is_end_of_sentence = False
            if word[-1] in ('.', '?', '!'):
                is_end_of_sentence = True
        self.add(data)

    def add(self, data):
        for i in range(len(data) - self.N):
            window = tuple(data[i: self.N + i])
            if i == 0:
                self._add_start_window(window)
            if window not in self.model:
                self.model[window] = Dictogram([data[i + self.N]])
            else:
                self.model[window].update([data[i + self.N]])

    def generate_sentence(self, length):
        window = self._get_start_window()
        window_str = ' '.join(window)
        sentence = [window_str]
        length -= len(window_str)
        while True:
            need_capitalize = sentence[-1][-1] in ('?', '!', '.')
            if window not in self.model:
                return self._get_joined_sentence(sentence)
            word = self.model[window].get_weighted_random_word()
            length = self._get_length_limit(length, word)
            if length < 0:
                return self._get_joined_sentence(sentence)
            sentence.append(word)
            window = tuple([sentence[-self.N]])
            if need_capitalize:
                sentence[-1] = sentence[-1].capitalize()

    def _get_start_window(self):
        return self.model['START'].get_weighted_random_word()

    def _add_start_window(self, window):
        if 'START' not in self.model:
            self.model['START'] = Dictogram([window])
        else:
            self.model['START'].update([window])

    @staticmethod
    def _get_length_limit(length, word):
        length -= len(word) + 1
        if length == 0:
            if word[-1] in ('.', '?', '!'):
                return length
            return length - 1
        return length

    @staticmethod
    def _get_joined_sentence(sentence):
        while sentence[-1][-1] in (',', ':', ';'):
            sentence[-1] = sentence[-1][:-1]
        if sentence[-1][-1] not in ('.', '?', '!'):
            sentence[-1] += '.'
        sentence[0] = sentence[0].capitalize()
        return ' '.join(sentence)


class Generator:
    def __init__(self, project_id):
        self.intents_client = dialogflow.IntentsClient()
        self.project_id = project_id
    
    def execute(self):
        parent = dialogflow.AgentsClient.agent_path(self.project_id)
        intents = self.intents_client.list_intents(request={'parent': parent})
        for intent in intents:
            chain = MarkovChain()
            messages = intent.messages[0].text.text
            if messages != []:
                for message in messages:
                     chain.parse_and_add(message)
                print('Сгенерированы новые ответы для намерения "%s":' % intent.display_name)
                for i in range(20):
                    print(chain.generate_sentence(140))
                print('\n')
