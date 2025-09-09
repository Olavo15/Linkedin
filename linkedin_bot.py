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
    > Enviando Currículos...
""")

# Inicializa o navegador
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")

# Login
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
# time.sleep(120)  # descomenta se usar 2FA

print("✅ Login confirmado, continuando o script...")

# Página de vagas
driver.get("https://www.linkedin.com/jobs/search/?distance=25&f_AL=true&f_E=3&f_WT=2%2C3&geoId=106057199&keywords=Front-End%20Júnior&refresh=true")
time.sleep(6)

# Scroll para carregar mais vagas
for _ in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 4))

# Coleta as vagas
vagas = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search-results__list > li")
print(f"🔎 Encontradas {len(vagas)} vagas com filtro Júnior.")

if len(vagas) == 0:
    print("⚠️ Nenhuma vaga na lista. Tentando clicar na vaga atual visível...")
    try:
        vaga_atual = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.jobs-search__job-details--wrapper"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", vaga_atual)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", vaga_atual)
        time.sleep(3)
        vagas = [vaga_atual]
    except TimeoutException:
        print("❌ Não foi possível encontrar ou clicar na vaga visível.")
        driver.quit()
        exit()

# Itera sobre as vagas e tenta se candidatar
for vaga in vagas:
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", vaga)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", vaga)
        time.sleep(random.uniform(3, 5))

        # Tenta localizar o botão "Candidatura simplificada"
        try:
            botao_candidatura = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "jobs-apply-button-id"))
            )

            if "Candidatura simplificada" in botao_candidatura.text:
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", botao_candidatura)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", botao_candidatura)
                except:
                    driver.execute_script("arguments[0].click();", botao_candidatura)

                print("✅ Botão 'Candidatura simplificada' encontrado e clicado.")

                # Fluxo de múltiplas etapas (botão "Avançar")
                while True:
                    try:
                        avancar = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Avançar para próxima etapa']"))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", avancar)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", avancar)
                        print("➡️ Cliquei em 'Avançar' para próxima etapa...")
                        time.sleep(2)
                    except TimeoutException:
                        print("ℹ️ Nenhum botão 'Avançar' visível. Tentando enviar candidatura...")
                        break

                # Agora tenta localizar o botão de enviar candidatura
                try:
                    enviar = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Enviar candidatura']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", enviar)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", enviar)
                    print("✅ Candidatura enviada com sucesso.")
                except TimeoutException:
                    print("❌ Não foi possível enviar a candidatura (pode exigir upload ou perguntas adicionais).")

            else:
                print("⚠️ Botão encontrado, mas não é 'Candidatura simplificada'. Pulando...")

        except TimeoutException:
            print("❌ Nenhum botão de 'Candidatura simplificada' nesta vaga. Indo para a próxima...")

    except Exception as e:
        print("⚠️ Erro ao tentar abrir vaga:", e)
        continue

driver.quit()
print("🏁 Script finalizado.")
