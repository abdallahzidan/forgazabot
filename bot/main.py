from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes,filters
from translate import Translator
import json
import requests
import re 
import yaml


TOKEN :Final = "****"
BOT_USERNAME :Final  = "@savegazabot"
API_KEY = "***"
brands_data = {}
config_data={}
 
with open('config/brands.json') as json_file:
    brands_data = json.load(json_file)

with open(yaml_file_path, "r",encoding="utf-8") as file:
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
        links= response.json().get("items", [])
        if links:
            print(links[0])
            first_link = links[0]['link'].split('.')[1].replace('com/','')
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
    
#commands
async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    ar=config_data['ar']['start_command']
    en=config_data['en']['start_command']

    await update.message.reply_text("{ar} \n {en} ")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/V9H3LmB")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/dPp87QJ")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/48TFMWN")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/hV9XGwH")
    
    ar_help=config_data['ar']['help_command']
    en_help=config_data['en']['help_command']
    await update.message.reply_text("{ar_help} \n {en_help} ")


async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    ar_help=config_data['ar']['help_command']
    en_help=config_data['en']['help_command']
    await update.message.reply_text("{ar_help} \n {en_help} ")

async def support_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    ar=config_data['ar']['support_command']
    en=config_data['en']['support_command']
    await update.message.reply_text(" {ar} \n {en} \n  1-Awtad  https://awtad.ngo/programs/emergency-relief \n 2- Mersal : https://mersal-ngo.org/DynamicPage/RenderPage?id=48 \n 3- Unrwa https://support.savethechildren.org/site/Donation2?df_id=10067&10067.donation=form1&mfc_pref=T&cid=Paid_Search:Google_Paid:Emer_Middle_East:Nonbrand:101523&s_kwcid=AL!9048!3!677410240757!b!!g!!donate%20to%20palestine&gclid=CjwKCAjws9ipBhB1EiwAccEi1Km9CVV0FSdQs9Qk4uyeKzqOBujHmmNatGEH4S_m-SHCtsSVfaCdJxoCGFMQAvD_BwE&gclsrc=aw.ds")

#handle responses
def handle_response(text:str):
    text = translate_arabic_to_english(text)
    text=text.replace(" ", "").replace("'","")
    if not text.isalpha():
        return f"{ config_data['ar']['handle_response_wrong_input'] } \n { config_data['en']['handle_response_wrong_input'] } "   
    brand_info = get_reason_by_brand(text.lower())
    ar_yes=config_data['ar']['handle_response_true']
    en_yes =config_data['en']['handle_response_true']
    ar_no=config_data['ar']['handle_response_false']
    en_no =config_data['en']['handle_response_false']
    if text.lower()  in [i["name"] for i in brands_data['brands']]: #or  gtext.lower() in [i["name"] for i in jsonString['brands']]:
        return f"{ar_yes}\n{en_yes}\n{brand_info}"
    else: 
        return f"{ar_no}\n{en_no}"
    
async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response : str = handle_response(text)
    await update.message.reply_text(response)
    
if __name__=="__main__":
    
    app=Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('support',support_command))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.run_polling(poll_interval=3)
