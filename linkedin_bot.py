from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from Credentials.credenciais import EMAIL, SENHA

print("""
    📘 CLT ATIVADO
    > Buscando trabalho...
    > Enviando Curriculos...
""")

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")


driver.find_element(By.ID, "username").send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys(SENHA)
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

time.sleep(2)

# Verifica erros de login
try:
    errorUsername = driver.find_element(By.ID, 'error-for-username').text.strip()
except NoSuchElementException:
    errorUsername = ""

try:
    errorPassword = driver.find_element(By.ID, 'error-for-password').text.strip()
except NoSuchElementException:
    errorPassword = ""

if errorUsername != "" or errorPassword != "":
    print('❌ Erro ao tentar realizar o login!')
    print('Erro username:', errorUsername)
    print('Erro password:', errorPassword)
    driver.quit()
    exit()

print("🔐 Login enviado, aguardando 2 minutos para confirmação no celular...")
time.sleep(120)

print("✅ Login confirmado, continuando o script...")

driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4236817524&distance=25&f_AL=true&f_E=3&f_WT=2%2C3&geoId=106057199&keywords=Front-End%20J%C3%BAnior&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&spellCorrectionEnabled=true")
time.sleep(6)


for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 4))


vagas = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search-results__list > li")
print(f"🔎 Encontradas {len(vagas)} vagas com filtro Júnior.")

if len(vagas) == 0:
    print("⚠️ Nenhuma vaga na lista. Tentando clicar na vaga atual visível...")
    try:
        vaga_atual = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.jobs-search__job-details--wrapper"))
        )
        vaga_atual.click()
        time.sleep(3)
        vagas = [vaga_atual]
    except TimeoutException:
        print("❌ Não foi possível encontrar ou clicar na vaga visível.")
        driver.quit()
        exit()

# Itera sobre as vagas e tenta se candidatar
for vaga in vagas:
    try:
        vaga.click()
        time.sleep(random.uniform(3, 5))

        # Espera o botão de candidatura aparecer
        try:
            botao = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Candidatura simplificada')]"))
            )
            botao.click()
            print("✅ Botão de candidatura simplificada clicado.")

            # Depois tenta enviar candidatura
            try:
                enviar = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Enviar candidatura']"))
                )
                enviar.click()
                print("✅ Candidatura enviada com sucesso.")
                time.sleep(random.uniform(2, 4))
            except TimeoutException:
                print("ℹ️ Botão 'Enviar candidatura' não encontrado, talvez não precise enviar.")
            
            time.sleep(random.uniform(2, 4))

        except TimeoutException:
            print("⚠️ Botão 'Candidatura simplificada' não encontrado para esta vaga. Pulando...")

    except Exception as e:
        print("❌ Erro ao tentar se candidatar:", e)
        continue

driver.quit()
print("🏁 Script finalizado.")
