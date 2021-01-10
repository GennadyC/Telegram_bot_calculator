from flask import Flask, request, make_response, jsonify
import requests
import json

app = Flask(__name__)

def results():
    return 'HELLLO GNGSTA'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print(request.json)
    return {'fulfillmentText': 'ТПУ насчитывает 29 корпусов'}


if __name__ == '__main__':
   app.run(debug=True)