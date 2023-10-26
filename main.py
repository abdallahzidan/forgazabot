from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes,filters
import json

TOKEN :Final = "********************"
BOT_USERNAME :Final  = "@savegazabot"

jsonString = {}
 
with open('brands.json') as json_file:
    jsonString = json.load(json_file)
    


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

#    
# Hewlett Packard helps run the biometric ID system that Israel uses to restrict Palestinian movement. For more information, see https://bdsmovement.net/boycott-hp. \n \
#     2- AXA invests in Israeli banks, which finance the theft of Palestinian land and natural resources. Do not buy insurance policies with AXA, or if you currently have an insurance policy with them, try cancelling it. For more information visit: https://bdsmovement.net/axa-divest \n \
#     3- 	Coca-Cola is an American multinational corporation. Coca-Cola Israel owns dairy farms in illegal Israeli settlements \n\
#     4-  Starbucks is an American multinational chain of coffeehouses. Starbucks has opened outlets in US bases in Afghanistan and Iraq and at the illegal torture center in Guantanamo Bay. Starbucks also sponsors fundraisers for Israel \n\
#     5-  McDonald’s Corporation is an American multinational fast-food chain. Its products include hamburgers, chicken, french fries, soft drinks, shakes, salads, desserts, hotcakes, coffee, breakfast, and wraps. McDonald’s offers free meals to hospitals and Israeli defense forces \n \
#     6-  Siemens is the largest industrial manufacturing company in Europe for buildings and distributed energy systems, and it will link Israel’s electricity grid with Europe \n\
#     7-  Puma SE is a German multinational corporation that manufactures athletic and casual footwear, apparel, and accessories. Puma sponsors the Israel Football Association \n\
#     8-  Sabra Dipping Company is a joint venture that produces food products. Sabra is co-owned by PepsiCo and the Strauss Group, which provides financial support to the Israeli army \n")

async def help_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(" أكتب إسم العلامة التجارية بالانجليزية و سنخبرك اذا ما كان عليك مقاطعتها\n Please Write the brand name in English and we will tell you if you should boycott it .. !")


async def food_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    for i in jsonString['food']:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo = i) 
    #await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/6bvk0YP")
    #await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/fY0xSRj")
    #await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://imgtr.ee/image/IId5rv")

    
async def support_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" 1-Awtad  https://awtad.ngo/programs/emergency-relief \n 2- Mersal : https://mersal-ngo.org/DynamicPage/RenderPage?id=48 \n 3- Unrwa https://support.savethechildren.org/site/Donation2?df_id=10067&10067.donation=form1&mfc_pref=T&cid=Paid_Search:Google_Paid:Emer_Middle_East:Nonbrand:101523&s_kwcid=AL!9048!3!677410240757!b!!g!!donate%20to%20palestine&gclid=CjwKCAjws9ipBhB1EiwAccEi1Km9CVV0FSdQs9Qk4uyeKzqOBujHmmNatGEH4S_m-SHCtsSVfaCdJxoCGFMQAvD_BwE&gclsrc=aw.ds")

#handle responses

def handle_response(text:str):
    if not text.isascii():
        return "من فضلك ادخل اسم العلامة التجارية بالاحرف الانجليزيه \n please write brand name in english letters"
    if text.lower() in [i["name"] for i in jsonString['brands']]:
        return "Yes, boycott this product \n نعم قاطع هذه العلامه التجارية  "
        
        
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
