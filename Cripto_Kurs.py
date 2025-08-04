import tkinter as tk
from tkinter import ttk, messagebox
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
        messagebox.showerror("Ошибка", "Выберите криптовалюту и валюту!")
        return

    data = fetch_crypto_data(crypto_id, currency)

    if not data or crypto_id not in data:
        messagebox.showerror("Ошибка", "Не удалось получить данные!")
        return

    rate = data[crypto_id][currency]
    messagebox.showinfo(
        "Курс обмена",
        f"1 {crypto_id.capitalize()} = {rate} {currency.upper()}"
    )


# Создание графического интерфейса
root = tk.Tk()
root.title("Курсы криптовалют")
root.geometry("400x200")

# Выбор криптовалюты
tk.Label(root, text="Выберите криптовалюту:").pack(pady=5)
crypto_combobox = ttk.Combobox(root, values=CRYPTO_IDS, state="readonly")
crypto_combobox.pack(pady=5)

# Выбор валюты
tk.Label(root, text="Выберите валюту:").pack(pady=5)
currency_combobox = ttk.Combobox(root, values=CURRENCIES, state="readonly")
currency_combobox.pack(pady=5)

# Кнопка для показа курса
show_button = tk.Button(root, text="Показать курс", command=show_exchange_rate)
show_button.pack(pady=10)

root.mainloop()