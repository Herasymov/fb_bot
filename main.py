"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request
from pymessenger2.bot import Bot, NotificationType

import re

app = Flask(__name__)

ACCESS_TOKEN = "EAADrR56PF48BAEbsEu0eTcLTWB7aUjlpRSYMkDb6UgReb0zKnzALzcZAS" \
               "0iZCJVZCZA0DpeB6Yjn84KXR0k0ZC2ZCCiAGrfXWEY22AxIMCMZBXNdXWyZ" \
               "CFMOxIQF7O5eR12iEblW5g0ctoZAUiADmVbt6flrIGQm0PvDImRUpOiOyD55iEL5sRg1A"

VERIFY_TOKEN = "bot"


class OverridesBot(Bot):
    """
    Overrides class bot and fix bag
    """

    def send_recipient(self,
                       recipient_id,
                       payload,
                       notification_type=NotificationType.regular):
        payload['recipient'] = {'id': recipient_id}
        payload['notification_type'] = notification_type.value
        return self.send_raw(payload)


bot = OverridesBot(ACCESS_TOKEN)


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    message_text = x['message'].get('text')
                    if message_text == '/start':
                        message = 'Введите ФИО'
                        bot.send_text_message(recipient_id, message)
                    elif len(message_text.split()) == 3 and re.match('[А-ЯЁ-а-яё]+|[A-Z-a-z]+', message_text):
                        message = f"Приветствуем {message_text} Введите  номер"
                        bot.send_text_message(recipient_id, message)
                    elif re.match(r'\d', message_text):
                        message = f"Наш менеджер скоро с вами свяжется"
                        bot.send_text_message(recipient_id, message)

                else:
                    pass
        return "Success"


if __name__ == "__main__":
    app.run(port=5002, debug=True)
