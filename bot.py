import telebot # библиотека telebot
from config import token # импорт токена
from random import choice

bot = telebot.TeleBot(token) 
bad = ['Плохое слово', 'https://', 'http://', 'Бомба']

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Не пишите в чате плохие слова, не рассылайте рассылки иначе вы будете наказаны! /help посмотреть мои команды")


@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")
    

ban = 0
@bot.message_handler(func=lambda message: True )
def ban_message(message):
    for i in bad:
        global ban
        if ban == 0 and i in message.text:
            bot.reply_to(message, "Не пишите плохие слова и рассылки , иначе вы будете наказаны!")
            bot.delete_message(message.chat.id, message.message_id)
            ban += 1
        elif ban == 1 and i in message.text:
            bot.reply_to(message, 'Если вы еще напишите плохое слово или отправите рассылку вы будете заблокированы!')
            bot.delete_message(message.chat.id, message.message_id)
            ban += 1
        elif ban == 2 and message.text in bad:
            chat_id = message.chat.id # сохранение id чата
            # сохранение id и статуса пользователя, отправившего сообщение
            user_id = message.from_user.id
            user_status = bot.get_chat_member(chat_id, user_id).status 
            # проверка пользователя
            if user_status == 'administrator' or user_status == 'creator':
                bot.reply_to(message, "Невозможно забанить администратора.")
                ban == 0
            else:
                bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
                bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")


@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'Добавлен новый пользователь! Привет'+ message.from_user.first_name+ '!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)


    

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """\
У меня есть такие команды: /quote; /fact; /stupid_fact; /ban\
""")


@bot.message_handler(commands=['quote'])
def quote(message):
    quotes = choice(["Счастье — это не нечто готовое. Счастье зависит только от ваших действий", 
                     "Не так важно то, что вы получите, достигнув своих целей, как то, кем вы станете, сделав это.",
                     'Вы никогда не пересечёте океан, если не наберётесь мужества потерять берег из виду.',
                     'Начинайте делать всё, что вы можете сделать, и даже то, о чём можете хотя бы мечтать. В смелости — гений, сила и магия.'
                     ])
    bot.reply_to(message, f'Ваша цитата дня: {quotes}')

@bot.message_handler(commands=['fact'])
def fact(message):
    facts = choice(['Осьминоги имеют три сердца. Два из них прокачивают кровь через жабры, а третье — по всему телу. Когда осьминог плавает, одно из сердец перестает работать, что делает плавание для него утомительным.',
                    'Скорость света в алмазе в 2,5 раза медленнее, чем в вакууме. Алмазы настолько плотные, что замедляют свет, проходящий через них.',
                    'Бананы — это ягоды, а вот клубника — нет. В ботаническом смысле ягода — это плод с семенами внутри, что подходит для бананов, но не для клубники, чьи семена расположены снаружи.',
                    'Самая большая пещера в мире — Сон Дунг во Вьетнаме. В ней может поместиться целый квартал с небоскрёбами, а внутри есть собственные реки и леса!'
                    ])
    bot.reply_to(message, f'Интересный факт: {facts}')
@bot.message_handler(commands=['stupid_fact'])
def stupid_fact(message):
    stupid_facts = choice(['Мыши не любят сыр. Поп-культура нас обманывала! На самом деле мыши предпочитают сладости, как орехи или фрукты.',
                           'Примерно через 2,3 миллиарда лет, на Земле скорее всего что-то произойдет.',
                           'Если бы вы кричали на арбуз 8 лет, 7 месяцев и 6 дней, то скорее всего ничего бы не произошло',
                           'Ленивцы слишком ленивы, чтобы ходить в туалет. Они делают это раз в неделю, и для них это настоящее событие!'
                           ])
    bot.reply_to(message,f'Глупый факт: {stupid_facts}')

bot.infinity_polling(none_stop=True)
