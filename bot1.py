from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from geopy.geocoders import Nominatim
main_buttons = [
    [
        InlineKeyboardButton('Namangan', callback_data='Namangan'),
        InlineKeyboardButton('Toshkent', callback_data='Toshkent'),
        InlineKeyboardButton('Xorazm', callback_data='Xorazm'),
    ],
    [            
        InlineKeyboardButton('Andijon', callback_data='Andijon'),
        InlineKeyboardButton("Farg'ona", callback_data="Farg'ona"),
        InlineKeyboardButton('Buxoro', callback_data='Buxoro'),
    ],
]

BTN_SOTISH, BTN_SOTIBOLISH, BTN_QAYTARISH, BTN_CHIQISH = ( 'sotish', 'Uzgartirish', 'Qaytarish', 'Kalendar') 

button_xizmat = ReplyKeyboardMarkup([
    [
        KeyboardButton(text='Mening nomerim', request_contact=True),
        KeyboardButton(text='Joylashuv', request_location=True),
    ],
    # [
    #     BTN_SOTISH, BTN_SOTIBOLISH, BTN_QAYTARISH, BTN_CHIQISH
    # ]
], resize_keyboard=True)

STATE_REGION = 1,
STETE_CALENDAR = 2,

def start(update, context):
    chat_id = update.message.chat.id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    xabar = update.message.text

    update.message.reply_text(
        f"Assalomu alaykumkum! <b>{first_name} {last_name}</b> siz qaysi xududda yashaysiz?", 
        reply_markup = InlineKeyboardMarkup(main_buttons), parse_mode='HTML'
    )
    print(f'first_name: {first_name}, last_name: {last_name}, username: {username}')
    return STATE_REGION

def calendar_tuday(update, context):
    # update.message.delete()
    update.message.reply_text('Bugungi kun')
def sotish(update, context):
    # update.message.delete()
    update.message.reply_text('Sotish!')
def sotib_olish(update, context):
    # update.message.delete()
    update.message.reply_text('Sotib olish!')
def qaytarish(update, context):
    update.message.reply_text('Qaytarish')
    # update.message.delete()

def inline_callback(update, context):
    query = update.callback_query
    query.message.delete()
    query.message.reply_html(
        text=f'''Xush kelibsiz <b> {query.data} </b> xududiga, Menga <b> joylashuvingizni </b> junating qayerda ekanningizni aytib beraman! 👇''', 
        reply_markup = button_xizmat
    )
    return STETE_CALENDAR

def sss(ls):
    sumString = ""
    for i in ls:
        sumString+= f"{i}, "
    return sumString


def loc_handler(update, context):
    loc_date = update.message.location
    geolocator = Nominatim(user_agent="geoapiExercises")

    Latitude = str(loc_date.latitude)
    Longitude = str(loc_date.longitude)

    location = geolocator.reverse(Latitude+","+Longitude)
    address = location.raw['address']
    del address['country_code']
    del address['postcode']
    temp = []
    for key in address:
        if key.startswith("ISO"):
            pass
        temp.append(address[key])
    update.message.reply_html(f'Sizning manzilingiz: <b>{sss(reversed(temp))}</b>')
    print(temp)
    # for i in reversed(temp):
    #     new.append(i)
    # print(new)
    # update.message.reply_html(f'<b>{new}</b>')
    # print(address)

    # adreslar = {'country':'', 'region':'', 'county':'', 'city':'', 'town':'', 'industrial':'', 'road':''}
    # adreslar.values
    # # new_add = list()
    # adrescha = {}
    # # new_add.append
    
    # country = address.get('country')
    # region = address.get('region')
    # state = address.get('state')
    # county = address.get('county')
    # city = address.get('city')
    # town = address.get('town')
    # industrial = address.get('industrial')
    # road = address.get('road')
    # house_number = address.get('house_number')
    # neighbourhood = address.get('neighbourhood')
    # building = address.get('building')
    # amenity = address.get('amenity')
    # residential = address.get('residential')
    # shop = address.get('shop')

    # update.message.reply_html(
    #     f'''Sizning manzilingiz {country} {region}  {building} {county} {city} {town} {road} {neighbourhood} {industrial} {state} {amenity} {house_number} {residential} {shop}'''
    #     )


def main():
    updater = Updater('5512280575:AAE-BML8wWjHID7YAwJKwJZ4Q0reqdwXIuM', use_context=True)
    mydispatcher = updater.dispatcher

    # mydispatcher.add_handler(CommandHandler('start', start))
    # mydispatcher.add_handler(CallbackQueryHandler(inline_callback))

    conv_hendler = ConversationHandler(
        entry_points=[CommandHandler('start', start)], 
        states={
            STATE_REGION: [CallbackQueryHandler(inline_callback)],
            STETE_CALENDAR: [
                MessageHandler(Filters.regex('^('+BTN_CHIQISH+')$'), calendar_tuday),
                MessageHandler(Filters.regex('^('+BTN_SOTISH+')$'), sotish),
                MessageHandler(Filters.regex('^('+BTN_SOTIBOLISH+')$'), sotib_olish),
                MessageHandler(Filters.regex('^('+BTN_QAYTARISH+')$'), qaytarish),
            ]
        }, 
        fallbacks=[CommandHandler('start', start)]
    )

    loc_command = MessageHandler(filters=Filters.location, callback=loc_handler)

    mydispatcher.add_handler(loc_command)
    mydispatcher.add_handler(conv_hendler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
