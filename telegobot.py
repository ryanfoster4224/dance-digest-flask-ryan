from telebot import TeleBot, types

bot = TeleBot("5602757659:AAHmbDMWM4iVQ9RTu79inwC3cCBTKqS361Q",
                  parse_mode=None)


def send_announce(announces='Hi'):
    # You can set parse_mode by default. HTML or MARKDOWN
    announces = '<b>hello</b>'
    wild_dances_channel_id = -1001866935354
    social_dances_id = -1001287171602
    bot.send_message(wild_dances_channel_id, text=announces, parse_mode='HTML')

send_announce()