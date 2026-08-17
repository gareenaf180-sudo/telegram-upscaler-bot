import os
import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
import io

# Token එක Render Environment Variables වලින් ගන්නවා
TOKEN = os.getenv("TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ආයුබෝවන්! මට photo එකක් එවන්න. මම ඒක upscale කරලා දෙන්නම් 🔥")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Photo එක download කරනවා... ටිකක් ඉන්න")
    
    # Photo download කරනවා
    photo_file = await update.message.photo[-1].get_file()
    photo_bytes = await photo_file.download_as_bytearray()
    
    # මෙතන ඔයාගේ Upscale code එක දාන්න
    image = Image.open(io.BytesIO(photo_bytes))
    
    # Example: සරලව resize කරනවා x2
    new_size = (image.width * 2, image.height * 2)
    upscaled_image = image.resize(new_size, Image.LANCZOS)
    
    # ආයෙ Telegram වලට එවනවා
    buf = io.BytesIO()
    upscaled_image.save(buf, format='PNG')
    buf.seek(0)
    
    await update.message.reply_photo(photo=InputFile(buf, filename="upscaled.png"))

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("Bot started...")
    app.run_polling()

if name == "main":
    main()
