# 🤖 Bot de Candidatura Automática no LinkedIn

Este projeto automatiza o processo de candidatura em vagas do LinkedIn usando **Python + Selenium**.  
O script faz login, pesquisa vagas, percorre a lista e tenta clicar no botão **Candidatura simplificada**.

---

## 🚀 Requisitos

- Python 3.9+
- Google Chrome instalado
- [ChromeDriver](https://chromedriver.chromium.org/) compatível com a sua versão do Chrome

---

## 📦 Instalação

Crie um ambiente virtual (`venv`) e instale as dependências:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install selenium
```

## ⚙️ Configuração

Crie um arquivo chamado Credentials/credenciais.py com seu login:

EMAIL = "seu_email_aqui"
SENHA = "sua_senha_aqui"

▶️ Executando

Ative o ambiente virtual e rode o script:

- source venv/bin/activate
- python3 linkedin_bot.py

## ⚠️ Aviso Legal

<span style="color:red">

Use este projeto **apenas para fins educacionais**.
Automatizar candidaturas pode **violar os termos de uso do LinkedIn**.
Você é **responsável pelo uso deste código**.
</span>
