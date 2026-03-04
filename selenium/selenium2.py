import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TARGET_URL = "https://www.databricks.com/dataaisummit/agenda"
DB_FILE = "last_count.txt"


def get_last_count():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return int(f.read().strip())
    return 37


def save_current_count(count):
    with open(DB_FILE, "w") as f:
        f.write(str(count))


def check_databricks_sessions():
    try:
        # User-Agent ajuda a não ser bloqueado como "robô" simples
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # IMPORTANTE: Você precisará confirmar se a classe é 'session-count'
        # inspecionando o elemento no navegador (F12)
        session_element = soup.find("span", {"class": "session-count"})

        if session_element:
            return int(''.join(filter(str.isdigit, session_element.text)))
        return None
    except Exception as e:
        print(f"Erro ao raspar dados: {e}")
        return None


def send_notification(count):
    message = f"O número de sessões aumentou para: {count}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


last_known = get_last_count()
current = check_databricks_sessions()

if current and current > last_known:
    send_notification(current)
    save_current_count(current)
    print(f"Novo valor detectado: {current}. Notificação enviada.")
else:
    print(f"Sem alterações. Último: {last_known}, Atual: {current}")
