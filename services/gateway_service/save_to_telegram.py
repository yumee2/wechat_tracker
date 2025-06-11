import requests
import os

def send_message_to_telegram(order_info):
    BOT_ID = os.getenv("BOT_ID")
    CHAT_ID = os.getenv("CHAT_ID")
    bot_token = BOT_ID
    chat_id = CHAT_ID
    density = str(order_info["density"]).replace('.', '\.')
    weight = str(order_info["weight"]).replace('.', '\.')
    total_price = str(order_info["total_price"]).replace('.', '\.')
    if order_info["boxes_amount"] != None:
        message = f"Новый заказ:\n\nПользователь: [{order_info['user_name']}]({order_info['user_link']})\nПлотность: {density}\nТип товара: {order_info['cargo_type']}\nКоличество коробок: {order_info['boxes_amount']}\nВес: {weight}\nСтоимость кг\м3 : {total_price}"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        print(url)
        print(message)
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "MarkdownV2"
        }

        response = requests.post(url, json=payload)
    else:
        message = f"Новый заказ:\n\nПользователь: [{order_info['user_name']}]({order_info['user_link']})\nПлотность: {density}\nТип товара: {order_info['cargo_type']}\nСтоимость кг\м3 : {total_price}"
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        print(url)
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "MarkdownV2"
        }
        print(message)
        response = requests.post(url, json=payload)
