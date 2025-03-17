from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from time import sleep
from datetime import datetime
import requests  #

# Configurar o WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executar sem abrir o navegador (opcional)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def enviaWhatsApp(mensagem): 
    try: 
        # URL do servidor Node.js
        url = "https://nodejs-production-f2ff.up.railway.app/send-message"
        #url = "http://localhost:3000/send-message"

        # Número do destinatário no formato internacional
        numero = "555484411121"  # Exemplo: +55 11 99999-9999 (sem o +)

        # Mensagem a ser enviada
        #mensagem = "Olá!  Esta é uma mensagem enviada pelo Python via railway.com."

        # Criando o payload
        data = {
            "number": numero,
            "message": mensagem
        }

        # Enviando a requisição POST para o servidor Node.js
        response = requests.post(url, json=data)

        # Mostrando a resposta
        print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar mensagem para o WhatsApp: {e}")
    except Exception as error:
        print(f"❌ Erro ao iniciar o WhatsApp: {error}")





# Exibir data e hora atual
now = datetime.now()
print("Data e hora inicial:", now.strftime("%d-%m-%Y %H:%M:%S"))

text_1_bkp = ''
completo = (f'Sequencia Clube do dia {now.strftime("%d-%m")} das {now.strftime("%H")}')
try:
    contagem = 0
    while contagem < 57 :
        # Acessar o site específico de Brasília
        driver.get("https://www.clube.fm/brasilia")
        sleep(40)

        # Esperar o carregamento completo da página
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        #print("Título da página:", driver.title)

        # Capturar o body do HTML
        #body_html = driver.find_element(By.TAG_NAME, "body").get_attribute("outerHTML")
        now = datetime.now()
        # Salvar o HTML em um arquivo
        text_1 = driver.find_element(By.CLASS_NAME, "sc-1aab1d33-4.fbUEHW").text
        text_2 = driver.find_element(By.CLASS_NAME, "sc-1aab1d33-6.gkLYzf").text
        hora = now.strftime("%d-%m-%Y %H:%M")
        horaarq = now.strftime('%d-%m-%Y %H')
        print(f"musica: {text_1} - artista: {text_2}")
        #print("Texto da classe 'sc-1aab1d33-4 fbUEHW':", text_1)
        #print("Texto da classe 'sc-1aab1d33-6 gkLYzf':", text_2)
        
        if text_1 != text_1_bkp:

                if text_2.startswith("Com ") or text_2.startswith("CLUBE"):
                    print("não é musica")

                else:
                    with open(f"clube_fm_{horaarq}.html", "a", encoding="utf-8") as file:
                        file.write(f"\nmusica: {text_1} do ")
                        file.write(f"artista: {text_2}")
                        print("Gravou")
                        completo = completo + (f"\nmusica: {text_1} - artista: {text_2}")
                        #print(f"HTML salvo em clube_fm_{now.strftime('%d-%m %H:%M')}.html")



                if text_1 == 'DISK RECAÍDA':
                    with open(f"DISK RECAÍDA {horaarq}.html", "a", encoding="utf-8") as file1:
                        file1.write(f"\nmusica: {text_1} - ")
                        file1.write(f"artista: {text_2} - ")
                        file1.write(f"Data e Hora: {hora}")
                    print("TOCOU':", text_1)
        else:
            print(f"Música já registrada ou era programação: {text_1}")

        text_1_bkp = text_1
        
        contagem = contagem+1
        sleep(20)
        
        if contagem >= 55:
            print("Contador de iterações':", contagem)
        

    
finally:
 # Fechar o navegador
 now = datetime.now()
 print("Data e hora final:", now.strftime("%d-%m-%Y %H:%M:%S"))
 print(completo)

 enviaWhatsApp(completo)

 driver.quit()
