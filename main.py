import re
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Функция для извлечения ID и сообщения из ссылки
def parse_tg_link(link):
    match = re.match(r'https://t.me/(?P<username>.+)/(?P<msg_id>\d+)', link)
    if match:
        return match.group('username'), int(match.group('msg_id'))
    return None, None

# Обработчик новых сообщений
@bot.on(events.NewMessage)
async def handler(event):
    message = event.message

    # Проверка на наличие ссылки в сообщении
    if message.message and 't.me' in message.message:
        link = message.message.strip()
        username, msg_id = parse_tg_link(link)

        if username and msg_id:
            try:
                entity = await bot.get_entity(username)
                chat_id = entity.id
                await event.reply(f"Chat ID: {chat_id}\nMessage ID: {msg_id}")
            except Exception as e:
                await event.reply(f"Ошибка: {e}")
        else:
            await event.reply("Неправильная ссылка на сообщение.")
    
    # Обработка пересланных сообщений
    elif message.fwd_from:
        forward_info = message.fwd_from
        if forward_info.from_id:
            chat_id = forward_info.from_id.channel_id or forward_info.from_id.chat_id
            await event.reply(f"Chat ID: {chat_id}")
        else:
            await event.reply("Не удалось получить информацию о чате.")
    else:
        await event.reply("Пожалуйста, пересланное сообщение должно быть из канала или чата.")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.run_until_disconnected()