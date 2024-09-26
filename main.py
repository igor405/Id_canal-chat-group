import os
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение конфигурационных данных из окружения
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Инициализация клиента Telethon
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Обработчик пересланных сообщений
@bot.on(events.NewMessage)
async def handler(event):
    if event.message.is_forwarded:
        # Получение информации о пересланном сообщении
        forward_info = event.message.forward
        if forward_info.chat:
            chat = forward_info.chat
            chat_info = f"Chat ID: {chat.id}\n" \
                        f"Title: {chat.title}\n" \
                        f"Username: {chat.username}\n" \
                        f"Type: {chat.type}"
            await event.reply(chat_info)
        else:
            await event.reply("Перешлите сообщение из канала, группы или чата.")
    else:
        await event.reply("Пожалуйста, пересланное сообщение должно быть из канала или чата.")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.run_until_disconnected()
