from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes,filters
TOKEN :Final = "*********"
BOT_USERNAME :Final  = "@savegazabot"


#commands
async def start_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://pbs.twimg.com/media/F9IIDxOWUAAs5OB.jpg")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/fN52j1x")
    
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
    await update.message.reply_text(" how can i help ?")

async def food_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/6bvk0YP")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/fY0xSRj")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://imgtr.ee/image/IId5rv")

async def fashion_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/R4SkL0S")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://ibb.co/3YV2wr8")
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://imgtr.ee/image/IIdDRT")

async def motor_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("BMW GROUP \n AUDI ")
    
async def insurance_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AXA \n  ALLIANZ")
  
async def it_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HP \n Siemens \n SAP")
              
    
async def support_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" 1-Awtad  https://awtad.ngo/programs/emergency-relief \n 2- Mersal : https://mersal-ngo.org/DynamicPage/RenderPage?id=48 \n 3- Unrwa https://support.savethechildren.org/site/Donation2?df_id=10067&10067.donation=form1&mfc_pref=T&cid=Paid_Search:Google_Paid:Emer_Middle_East:Nonbrand:101523&s_kwcid=AL!9048!3!677410240757!b!!g!!donate%20to%20palestine&gclid=CjwKCAjws9ipBhB1EiwAccEi1Km9CVV0FSdQs9Qk4uyeKzqOBujHmmNatGEH4S_m-SHCtsSVfaCdJxoCGFMQAvD_BwE&gclsrc=aw.ds")

def sayhi(bot, job):
    job.context.message.reply_text("قاطع من أجل غزة")

def time(bot, update,job_queue):
    job = job_queue.run_repeating(sayhi, 5, context=update)
    
#handle responses

def handle_response(text:str):
    if str.lower() in ["hp",'mackdonalds','starbucks']:
        return "نعم قاطع"
    else: 
        return "هذا المنتج غير مقاطعة"
    
async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Free Palestine.  \n You always have something to do.. ")

if __name__=="__main__":
    
    app=Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('food',food_command))
    app.add_handler(CommandHandler('fashion',fashion_command))
    app.add_handler(CommandHandler('motor',motor_command))
    app.add_handler(CommandHandler('insurance',insurance_command))
    app.add_handler(CommandHandler('it',it_command))
    
    app.add_handler(CommandHandler('support',support_command))
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    app.add_handler(MessageHandler(filters.TEXT,handle_response))
    app.add_handler(MessageHandler(filters.TEXT , time))

    app.run_polling(poll_interval=3)
