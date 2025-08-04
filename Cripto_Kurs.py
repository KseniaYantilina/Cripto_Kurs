from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests

# Настройки API
API_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_IDS = ["bitcoin", "ethereum", "tether", "binancecoin", "solana",
              "ripple", "cardano", "dogecoin", "polkadot", "polygon"]
CURRENCIES = ["rub", "usd", "eur", "cny", "jpy"]

# Словарь с названиями валют
CURRENCY_NAMES = {
    'rub': 'Российский рубль',
    'usd': 'Американский доллар',
    'eur': 'Евро',
    'jpy': 'Японская йена',
    'cny': 'Китайский юань',
}

def update_cry_label(event):
    """Обновление метки выбранной криптовалюты"""
    selected = crypto_combobox.get()
    cry_label.config(text=selected.capitalize())


def update_cur_label(event):
    """Обновление метки выбранной валюты"""
    selected = currency_combobox.get()
    cur_label.config(text=f"Валюта: {CURRENCY_NAMES.get(selected, selected)}")


def fetch_crypto_data(crypto_id, currency):
    """Получение данных о курсе криптовалюты"""
    params = {
        "ids": crypto_id,
        "vs_currencies": currency,
        "precision": 3  # Точность отображения - 3 знака после запятой
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return None


def show_exchange_rate():
    """Отображение текущего курса"""
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
    crypto_name = crypto_id.capitalize()
    currency_name = CURRENCY_NAMES.get(currency, currency.upper())

    mb.showinfo(
        "Курс обмена",
        f"1 {crypto_name} = {rate} {currency_name}\n"
        f"({CURRENCY_NAMES.get(currency, '')})"
    )


    """Создаем графический интерфейс"""
window = Tk()
window.title("Курсы криптовалют")
window.geometry("450x300")
window.configure(bg='pink')

# Стилизация
style = ttk.Style()
style.configure('TCombobox', padding=5)
style.configure('TLabel',background='violet', font=('Arial', 10))
style.configure('TButton', background='green', font=('Arial', 10))

# Выбор криптовалюты
ttk.Label(window, text="Выберите криптовалюту:").pack(pady=5)
crypto_combobox = ttk.Combobox(window, values=CRYPTO_IDS, state="readonly")
crypto_combobox.pack(pady=5)
crypto_combobox.bind("<<ComboboxSelected>>", update_cry_label)

cry_label = ttk.Label()
cry_label.pack(pady=5)

# Выбор валюты
ttk.Label(window, text="Выберите валюту:").pack(pady=5)
currency_combobox = ttk.Combobox(window, values=CURRENCIES, state="readonly")
currency_combobox.pack(pady=5)
currency_combobox.bind("<<ComboboxSelected>>", update_cur_label)  # Исправлено: привязка к currency_combobox

cur_label = ttk.Label()
cur_label.pack(pady=5)

# Кнопка для показа курса
show_button = ttk.Button(window, text="Показать курс", command=show_exchange_rate)
show_button.pack(pady=15)

# Запуск основного цикла
window.mainloop()