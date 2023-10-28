from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
from translate import Translator
from typing import Final

import json
import os
import requests
import yaml


load_dotenv()

TOKEN: Final = os.environ["BOT_TOKEN"]
BOT_USERNAME: Final = os.environ["BOT_NAME"]
API_KEY = os.environ["API_KEY"]
SEARCH_ENGINE_ID = os.environ["SEARCH_ENGINE_ID"]

brands_data = {}
config_data = {}
yaml_file_path = r"bot/config/display_text.yaml"

with open("bot/config/brands.json") as json_file:
    brands_data = json.load(json_file)

with open(yaml_file_path, "r", encoding="utf-8") as file:
    config_data = yaml.safe_load(file)


def translate_arabic_to_english(text):
    translator = Translator(to_lang="en", from_lang="ar")
    translation = translator.translate(text)
    return translation


def perform_search(query, search_type="web"):
    # Construct the URL for the Google Custom Search JSON API
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "searchType": "SEARCH_TYPE_UNDEFINED",
    }

    # Make the API request
    response = requests.get(base_url, params=params)
    print(response.text)
    if response.status_code == 200:
        links = response.json().get("items", [])
        if links:
            print(links[0])
            first_link = links[0]["link"].split(".")[1].replace("com/", "")
            print(first_link)
            return first_link
        else:
            print("No links found in the given text.")
            return None
    else:
        print("Error: Unable to perform the search.")
        return None


def get_reason_by_brand(brand_name):
    print(brand_name)
    for brand in brands_data["brands"]:
        if brand["name"].lower() == brand_name.lower():
            return brand["reason"]
    return "Brand not found."


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ar = config_data["ar"]["start_command"]
    en = config_data["en"]["start_command"]

    await update.message.reply_text(f"{ar} \n {en} ")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://ibb.co/V9H3LmB")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://ibb.co/dPp87QJ")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://ibb.co/48TFMWN")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://ibb.co/hV9XGwH")

    ar_help = config_data["ar"]["help_command"]
    en_help = config_data["en"]["help_command"]
    await update.message.reply_text(f"{ar_help} \n {en_help} ")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ar_help = config_data["ar"]["help_command"]
    en_help = config_data["en"]["help_command"]
    await update.message.reply_text(f"{ar_help} \n {en_help} ")


async def support_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ar = config_data["ar"]["support_command"]
    en = config_data["en"]["support_command"]
    await update.message.reply_text(
        f"""
        {ar}
        {en}
        1- Awtad  : https://awtad.ngo/programs/emergency-relief
        2- Mersal : https://mersal-ngo.org/DynamicPage/RenderPage?id=48
        3- Unrwa  : https://support.savethechildren.org/site/Donation2?df_id=10067&10067.donation=form1&mfc_pref=T
        """
    )


async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://imageupload.io/UuflLQyJjOGkfeW")
    await update.message.reply_text("https://www.jerusalemstory.com/en")
    await update.message.reply_text("https://www.facebook.com/mhammed.taheer/videos/1932200987173473/")
    await update.message.reply_text("https://www.facebook.com/JoeHusseinLovers/videos/329283599683891/")
    await update.message.reply_text("https://www.facebook.com/JoeHusseinLovers/videos/2475401965952994/ ")
    await update.message.reply_text("https://www.instagram.com/p/CyxwIbtso96/")
    await update.message.reply_text("https://www.instagram.com/p/CyvNFvBoA50/ ")
    await update.message.reply_text("https://www.instagram.com/p/CyqnekKKxfv/")


# handle responses
def handle_response(text: str):
    text = translate_arabic_to_english(text)
    text = text.replace(" ", "").replace("'", "")
    if not text.isalpha():
        ar_err = config_data["ar"]["handle_response_wrong_input"]
        en_err = config_data["en"]["handle_response_wrong_input"]
        return f"{ar_err}\n{en_err}"
    brand_info = get_reason_by_brand(text.lower())
    ar_yes = config_data["ar"]["handle_response_true"]
    en_yes = config_data["en"]["handle_response_true"]
    ar_no = config_data["ar"]["handle_response_false"]
    en_no = config_data["en"]["handle_response_false"]
    if text.lower() in [i["name"] for i in brands_data["brands"]]:
        # or gtext.lower() in [i["name"] for i in jsonString["brands"]]:
        return f"{ar_yes}\n{en_yes}\n{brand_info}"
    else:
        return f"{ar_no}\n{en_no}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = handle_response(text)
    await update.message.reply_text(response)


if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("support", support_command))
    app.add_handler(CommandHandler("story", story_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling(poll_interval=3)
