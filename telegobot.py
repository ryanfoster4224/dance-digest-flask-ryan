from telebot import TeleBot, types
from monga import *
import datetime

bot = TeleBot("5602757659:AAHmbDMWM4iVQ9RTu79inwC3cCBTKqS361Q",
                  parse_mode=None)

def get_event_html(item: Event):
    return f'<em>{item.weekday}</em>, 💃{item.title}🕺, початок⏰ {item.start}, баланс🎸: <b>{item.balance}</b>, \n📍адреса {item.location}\n' \
                     f'вартість💰: <b>{item.price}</b> <a href="https://opendance.life/event/{item.pk}">деталі події</a>\n----------\n'
def get_events():
    weekday_id = datetime.datetime.today().weekday()
    return  Event.objects(weekdayId__gte=weekday_id) \
        .order_by('weekdayId')

def send_announce(announces='Hi'):
    # You can set parse_mode by default. HTML or MARKDOWN
    announces = '<b>пункти танцювальності на цьому тижні</b> \n'
    events = get_events()
    for event in events:
        announces+= get_event_html(event)
    announces += 'детальніша інформація про вечірки є на сайті https://opendance.life/' \
                '\n якщо якоїсь вечірки немає в списку, ви можете самостійно додати її до бази, ' \
                'через форму знизу сайта'
    wild_dances_channel_id = -1001866935354
    social_dances_id = -1001287171602
    bot.send_message(social_dances_id, text=announces, parse_mode='HTML')

if __name__ == '__main__':
    send_announce()