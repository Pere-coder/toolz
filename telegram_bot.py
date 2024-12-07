import os
import telebot
from translate import Translator
from languages import language_codes

from dotenv import load_dotenv, dotenv_values

load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

user_language = {}

def get_language(lang1, lang2, text):
    lang1 = language_codes.get(lang1.lower(), lang1)
    lang2 = language_codes.get(lang2.lower(), lang2)
    translator = Translator(from_lang=lang1, to_lang=lang2)
    translation= translator.translate(text)
    return translation


@bot.message_handler(commands=["start","help"])
def lang_handler(message):
    text = ("Hi there, welcome to chT.\n"
            "Just text anything and I'll translate it to your preferred language.\n"
            "The format is simple, type /lang followed by the source and target language codes.\n"
            "Example: /lang french english \nTranslates from French to English.\n"
            "Example: /lang en de \nTranslates from English to German.\n"
            "Here is a list of some country short codes to help you get started:\n"
            "English: en\nFrench: fr\nGerman: de\nSpanish: es\nItalian: it\n"
            "Chinese: zh\nJapanese: ja\nRussian: ru\nHindi: hi\n"
            "Portuguese: pt\nArabic: ar\nKorean: ko\nDutch: nl\n"
            "Greek: el\nHebrew: he\nSwedish: sv\nTurkish: tr\n"
            "Polish: pl\nThai: th\nVietnamese: vi\nIndonesian: id\n"
            "Zulu: zu\nXhosa: xh\nAfrikaans: af\nMaori: mi\n"
            "Samoan: sm\nFijian: fj\nTongan: to\n")
    bot.reply_to(message, text)


@bot.message_handler(commands=['lang'])
def set_lang(message):
    try:
        languages = message.text.split()
        if len(languages) < 3:
            bot.reply_to(message,  "Please provide both source and target language codes. Example: /lang en de")
        
        lang1, lang2 = languages[1], languages[2]
        user_language[message.chat.id] = (lang1, lang2)
        bot.reply_to(message, f"Language set from {lang1} to {lang2}. Now send me the text to translate.")

    except IndexError:
        bot.reply_to(message, "An error occured!")

@bot.message_handler(func=lambda message: True)
def translate_lang(message):
    try:
        lang1, lang2 = user_language.get(message.chat.id, (None, None))
        if not lang1 or not lang2:
            bot.reply_to(message, "Please set the languages first using /lang command. Example: /lang en de")
            return
        text = message.text
        translated_text = get_language(lang1, lang2, text)
        bot.reply_to(message, translated_text)
    except Exception as e:
        bot.reply_to(message,  "An error occurred while translating. Please try again.")
    
bot.infinity_polling()