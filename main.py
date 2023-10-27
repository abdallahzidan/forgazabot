from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes,filters
from translate import Translator
import json
import requests
import os

TOKEN: Final = os.environ['BOT_TOKEN']
BOT_USERNAME: Final = os.environ['BOT_NAME']
API_KEY = os.environ['API_KEY']
SEARCH_ENGINE_ID = os.environ['SEARCH_ENGINE_ID']

jsonString = {}
 
with open('brands.json') as json_file:
    jsonString = json.load(json_file)
    
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
    for brand in jsonString["brands"]:
        if brand["name"].lower() == brand_name.lower():
            return brand["reason"]
    return "Brand not found."
    
#commands
async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" لا تكن شريك في الجريمة .. قاطع من أجل غزة .. من أجل الانسانية \n Do not be an accomplice in crime. Stand with Gaza, stand  with humanity.. !")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/V9H3LmB")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/dPp87QJ")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/48TFMWN")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/hV9XGwH")

    #await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://pbs.twimg.com/media/F9IIDxOWUAAs5OB.jpg")
    #await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/fN52j1x")
    await update.message.reply_text(" أكتب إسم العلامة التجارية بالانجليزية و سنخبرك اذا ما كان عليك مقاطعتها\n Please Write the brand name in English and we will tell you if you should boycott it .. !")


async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(" أكتب إسم العلامة التجارية بالانجليزية و سنخبرك اذا ما كان عليك مقاطعتها\n Please Write the brand name in English and we will tell you if you should boycott it .. !")


async def food_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    for i in jsonString['food']:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo = i) 

    
async def support_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" 1-Awtad  https://awtad.ngo/programs/emergency-relief \n 2- Mersal : https://mersal-ngo.org/DynamicPage/RenderPage?id=48 \n 3- Unrwa https://support.savethechildren.org/site/Donation2?df_id=10067&10067.donation=form1&mfc_pref=T&cid=Paid_Search:Google_Paid:Emer_Middle_East:Nonbrand:101523&s_kwcid=AL!9048!3!677410240757!b!!g!!donate%20to%20palestine&gclid=CjwKCAjws9ipBhB1EiwAccEi1Km9CVV0FSdQs9Qk4uyeKzqOBujHmmNatGEH4S_m-SHCtsSVfaCdJxoCGFMQAvD_BwE&gclsrc=aw.ds")

#handle responses

def handle_response(text:str):
    text = translate_arabic_to_english(text)
    text=text.replace(" ", "").replace("'","")
    print(text)
    if text.lower()  in [i["name"] for i in jsonString['brands']]: #or  gtext.lower() in [i["name"] for i in jsonString['brands']]:
        brand_info = get_reason_by_brand(text.lower())
        return f"Yes, boycott this product\nنعم قاطع هذه العلامة التجارية\n{brand_info}"
    else: 
        return "هذا المنتج غير مقاطعة\n Not found!"
    
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
