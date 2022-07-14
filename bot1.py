from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

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
        KeyboardButton(text='my number', request_contact=True),
        KeyboardButton(text='my location', request_location=True),
    ],
    [
        BTN_SOTISH, BTN_SOTIBOLISH, BTN_QAYTARISH, BTN_CHIQISH
    ]
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
    return STATE_REGION

def calendar_tuday(update, context):
    update.message.reply_text('Bugungi kun')
def sotish(update, context):
    update.message.reply_text('Sotish!')
def sotib_olish(update, context):
    update.message.reply_text('Sotib olish!')
def qaytarish(update, context):
    update.message.reply_text('Qaytarish')

def inline_callback(update, context):
    query = update.callback_query
    query.message.delete()
    query.message.reply_html(
        text=f'''Xush kelibsiz <b> {query.data} </b> xududiga, Quyidagi xizmatlardan birini tanlang 👇''', 
        reply_markup = button_xizmat
    )
    return STETE_CALENDAR

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

    mydispatcher.add_handler(conv_hendler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
