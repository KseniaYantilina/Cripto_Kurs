from tkinter import *
from tkinter import  messagebox as mb
from tkinter import ttk
import requests

# Настройки API
API_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_IDS = ["bitcoin", "ethereum", "tether", "binancecoin", "solana",
              "ripple", "cardano", "dogecoin", "polkadot", "polygon"]
CURRENCIES = ["rub", "usd", "eur", "cny", "jpy"]


# Функция для получения данных
def fetch_crypto_data(crypto_id, currency):
    params = {
        "ids": crypto_id,
        "vs_currencies": currency,
        "precision": 6
    }
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        return data
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return None


# Функция для отображения курса
def show_exchange_rate():
    crypto_id = crypto_combobox.get()
    currency = currency_combobox.get()

    if not crypto_id or not currency:
        mb.showerror("Ошибка", "Выберите криптовалюту и валюту!")
        return

    data = fetch_crypto_data(crypto_id, currency)

    if not data or crypto_id not in data:
        mb.showerror("Ошибка", "Не удалось получить данные!")
        return

    rate = data[crypto_id][currency]
    mb.showinfo("Курс обмена", f"1 {crypto_id.capitalize()} = {rate} {currency.upper()}")

cur = {
    'rub': 'Российский рубль',
    'usd': 'Американский доллар',
    'eur': 'Евро',
    'jpy': 'Японская йена',
    'cny': 'Китайский юань',
       }

# Создание графического интерфейса
window = Tk()
window.title("Курсы криптовалют")
window.geometry("400x200")

# Выбор криптовалюты
Label(text="Выберите криптовалюту:").pack(pady=5)
crypto_combobox = ttk.Combobox(values=CRYPTO_IDS, state="readonly")
crypto_combobox.pack(pady=5)

# Выбор валюты
Label(text="Выберите валюту:").pack(pady=5)
currency_combobox = ttk.Combobox(values=CURRENCIES, state="readonly")
currency_combobox.pack(pady=5)

# Кнопка для показа курса
show_button = Button(text="Показать курс", command=show_exchange_rate)
show_button.pack(pady=10)

window.mainloop()
