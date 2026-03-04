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
        with open(DB_FILE, "r", encoding='utf-8') as f:
            content = f.read().strip()
            return int(''.join(filter(str.isdigit, content)))
    return 37


def save_current_count(count):
    with open(DB_FILE, "w") as f:
        f.write(str(count))


def check_databricks_sessions():
    try:
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        import re
        results_element = soup.find(string=re.compile(r'Results'))

        if results_element:
            match = re.search(r'\((\d+)\)', str(results_element))
            if match:
                return int(match.group(1))

        return None
    except Exception as e:
        print(f"Erro na extração: {e}")
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
