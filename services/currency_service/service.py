import requests
from bs4 import BeautifulSoup

'''Парсинг CNY/RUB с сайта Мосбиржи'''
async def get_cny_price():
    url = "https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities/CNYRUB_TOM.json?iss.meta=off&marketdata.columns=LAST"

    response = requests.get(url)
    moex_data = response.json()
    cny_data = moex_data["marketdata"]["data"][0]

    if cny_data[0] is not None:
        cny_price = cny_data[0]
        print(f"CNY/RUB exchange rate: {cny_price}")
        return cny_price
    else:
        cny_sec_data = moex_data["securities"]["data"][0]
        cny_price = cny_sec_data[14]
        print(f"CNY/RUB exchange security rate: {cny_price}")
        return cny_price

'''Парсинг CNY/USD с сайта Китайского банка (Bank of China)'''
async def get_usd_price() -> float:
    base_url = "https://www.bankofchina.com/sourcedb/whpj/enindex_1619"
    headers = {"User-Agent": "Mozilla/5.0"}

    for i in range(1, 5):  # попробуем первые 4 страницы
        url = f"{base_url}_{i}.html" if i > 1 else f"{base_url}.html"
        print(f"🔎 Проверяем страницу: {url}")

        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")

        tables = soup.find_all("table", attrs={"width": "600"})
        for table in tables:
            if "Currency Name" in table.get_text():
                rows = table.find_all("tr")[1:]
                for row in rows:
                    cols = [td.get_text(strip=True) for td in row.find_all("td")]
                    if cols and cols[0] == "USD":
                        rate = float(cols[1]) / 100
                        print(f"💵 Найден курс USD: {rate}")
                        return  1 / rate

    print("❌ Не удалось найти курс USD.")
    return None  # или raise HTTPException(...)