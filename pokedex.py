import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window-size=1920,1080")
options.add_argument("--incognito")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 15)

pokemon = "pikachu"

driver.get(f"http://www.pokemon.com/br/pokedex/{pokemon}")

try:
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".pokedex-pokemon-pagination-title")
        )
    )

    altura = driver.find_element(
        By.XPATH, "//span[cotain(text() altura)], followigs-siblins::span"
    )

    peso = driver.find_element(
        By.XPATH, "//span[cotain(text() peso)], followigs-siblins::span"
    )

    tipos_elementos = driver.find_elements(By.CSS_SELECTOR, ".dtm-type ul li a")
    tipos = [t.text for t in tipos_elementos]

    print("DADOS COLETADOS:")
    print(f"Altura: {altura}")
    print(f"Peso: {peso}")
    print(f"Tipo(s): {', '.join(tipos)}")

except TimeoutException:
    print(
        "Erro: O Pokémon não apareceu.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

finally:
    time.sleep(5)
    driver.quit()
    print("Navegador fechado. Teste finalizado.")
