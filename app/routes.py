import re
from flask import request, session
from app import app, bot, db
from .models import User
from config import VERIFY_TOKEN

global uname

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

def add_new_user(u_id, mtext):
    if mtext == '/start':
        message = 'Введите ФИО'
        bot.send_text_message(u_id, message)
        user = User(
            fb_id=u_id,
            fio="",
            phone=0,
            status=1)
        db.session.add(user)
        db.session.commit()
    else:
        message = "ВВедите /start"
        bot.send_text_message(u_id, message)

def add_fio(u_id, mtext):
    if re.match('[А-ЯЁ-а-яё]+|[A-Z-a-z]+', mtext):
        message = f"Приветствуем {mtext}\n Введите номер:"
        bot.send_text_message(u_id, message)
        rows = User.query.filter_by(fb_id = u_id).update({'fio': mtext, 'status':2})
        db.session.commit()
    else:
        message = "Не валидные данные"
        bot.send_text_message(u_id, message)

def add_phone(u_id, mtext):
    if re.match(r'\d', mtext):
        rows = User.query.filter_by(fb_id = u_id).update({'phone': mtext, 'status':3})
        db.session.commit()
        message = f"Наш менеджер скоро с вами свяжется"
        bot.send_text_message(u_id, message)
    else:
        message = "Не валидные данные"
        bot.send_text_message(u_id, message)

def final_notif(u_id, mtext):
    message = "Ожидайте звонка"
    bot.send_text_message(u_id, message)

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    else:
        call={0:add_new_user, 1:add_fio, 2:add_phone}
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for x in messaging:
                if x.get('message'):
                    recipient_id = x['sender']['id']
                    message_text = x['message'].get('text')
                    user_temp = User.query.filter_by(fb_id=recipient_id).first()
                    if user_temp:
                        call[user_temp.status](recipient_id, message_text)
                    else:
                        call[0](recipient_id, message_text)

                else:
                    pass
        return "Success"
