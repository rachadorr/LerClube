from flask import Flask, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from time import sleep
from datetime import datetime
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def executar_script_selenium():
    # Configurar o WebDriver (remova a opção headless para visualizar durante o desenvolvimento)
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    log_output = []

    try:
        now = datetime.now()
        log_output.append(f"Data e hora inicial: {now.strftime('%d-%m-%Y %H:%M:%S')}<br>")

        text_1_bkp = ''
        completo = (f'Sequencia Clube do dia {now.strftime("%d-%m")} das {now.strftime("%H")}<br>')
        contagem = 0
        while contagem < 3:  # Reduzi para teste, você pode voltar para 57
            driver.get("https://www.clube.fm/brasilia")
            sleep(10)  # Reduzi para teste

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            now = datetime.now()
            text_1 = driver.find_element(By.CLASS_NAME, "sc-1aab1d33-4.fbUEHW").text
            text_2 = driver.find_element(By.CLASS_NAME, "sc-1aab1d33-6.gkLYzf").text
            hora = now.strftime("%d-%m-%Y %H:%M")
            horaarq = now.strftime('%d-%m-%Y %H')
            log_output.append(f"musica: {text_1} - artista: {text_2}<br>")
            logger.info(f"musica: {text_1} - artista: {text_2}")

            if text_1 != text_1_bkp:
                if not (text_2.startswith("Com ") or text_2.startswith("CLUBE")):
                    with open(f"clube_fm_{horaarq}.html", "a", encoding="utf-8") as file:
                        file.write(f"\nmusica: {text_1} do ")
                        file.write(f"artista: {text_2}")
                        logger.info("Gravou")
                    completo += (f"musica: {text_1} - artista: {text_2}<br>")

                if text_1 == 'DISK RECAÍDA':
                    with open(f"DISK RECAÍDA {horaarq}.html", "a", encoding="utf-8") as file1:
                        file1.write(f"\nmusica: {text_1} - ")
                        file1.write(f"artista: {text_2} - ")
                        file1.write(f"Data e Hora: {hora}")
                        logger.info(f"TOCOU': {text_1}")
            else:
                log_output.append(f"Música já registrada ou era programação: {text_1}<br>")
                logger.info(f"Música já registrada ou era programação: {text_1}")

            text_1_bkp = text_1
            contagem += 1
            sleep(5) # Reduzi para teste

            if contagem >= 55:
                logger.info(f"Contador de iterações': {contagem}")

        log_output.append(f"Data e hora final: {now.strftime('%d-%m-%Y %H:%M:%S')}<br>")
        log_output.append(completo)

    except Exception as e:
        log_output.append(f"Ocorreu um erro: {e}<br>")
        logger.error(f"Ocorreu um erro: {e}", exc_info=True)

    finally:
        driver.quit()
        return "".join(log_output)

@app.route('/ler')
def ler_pagina():
    log_resultado = executar_script_selenium()
    return f"<h1>Resultado da Execução:</h1><pre>{log_resultado}</pre>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
