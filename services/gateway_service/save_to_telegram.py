import requests
import os

def send_message_to_telegram(order_info):
    BOT_ID = os.getenv("BOT_ID")
    CHAT_ID = os.getenv("CHAT_ID")
    bot_token = BOT_ID
    chat_id = CHAT_ID
    density = str(order_info["density"]).replace('.', '\.')
    yuan_rub = str(order_info["yuan_rub"]).replace('.', '\.')
    yuan_usd = str(order_info["yuan_usd"]).replace('.', '\.')
    total_price = str(order_info["total_price"]).replace('.', '\.')
    message = f"Новый заказ:\n\nПользователь: [{order_info['user_name']}]({order_info['user_link']})\nПлотность: {density}\nКурс юань/рубль: {yuan_rub}\nКурс юань/доллар: {yuan_usd}\nТип товара: {order_info['cargo_type']}\nСтоимость: {total_price}"
    print(message)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    print(url)
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "MarkdownV2"
    }

    response = requests.post(url, json=payload)
