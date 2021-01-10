import telebot



class TelegramBot:
    def __init__(self, mail_client, mail_address, token):
        self.mail_client = mail_client
        self.mail_adress = mail_address
        self.token = token
        self.bot = telebot.TeleBot(self.token, parse_mode=None)
        self.all_messages()


    def all_messages(self):

        @self.bot.message_handler(commands=['start', 'help'])
        def repet_all_messages(message):
            self.bot.reply_to(message, 'hello')

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        def repet_all_messages(message):
            self.mail_client.send_mail('gennady.chursin2@gmail.com', message.text.encode())
            self.bot.send_message(message.chat.id, 'Сообщение передано в службу поддержки')

    def polling(self):
        print ('Start pulling telegram message')
        self.bot.polling()