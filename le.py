from flask import Flask, render_template_string, request # Esse 'request' é para passar o parametro pelo URL
import requests
import json
from time import sleep
import datetime
import pytz
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enviaWhatsApp(mensagem): 
    try: 
        # URL do servidor Node.js
        url = "https://nodejs-production-f2ff.up.railway.app/send-message"
        #url = "http://localhost:3000/send-message"

        # Número do destinatário no formato internacional
        numero = "555484411121"  # Exemplo: +55 11 99999-9999 (sem o +)

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


def obter_musica_clube_fm():
    url = "https://aovivo.clube.fm/clube.json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para status de erro
        data = response.json()
        singer = data['Pulsar']['OnAir']['media']['singer']
        song = data['Pulsar']['OnAir']['media']['song']
        return song, singer
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar o JSON: {e}")
        return None, None
    except (KeyError, json.JSONDecodeError) as e:
        logger.error(f"Erro ao processar o JSON: {e}")
        return None, None

def formatar_hora_brasil():
    now_utc = datetime.datetime.utcnow()
    timezone_brasil = pytz.timezone('America/Sao_Paulo')
    now_brasil = now_utc.astimezone(timezone_brasil)
    return now_brasil.strftime("%d-%m-%Y / %H:%M")

def executar_monitoramento(loops):
    log_completo = []
    lista = []
    ultima_musica = None
    inicio = formatar_hora_brasil()
    log_completo.append(f"===========INICIO==========={inicio}<br>")
    
    contagem = 0
    output = []
    while contagem < loops:  # Reduzi para teste, você pode voltar para 60
        url = "https://aovivo.clube.fm/clube.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            singer = data['Pulsar']['OnAir']['media']['singer']
            song = data['Pulsar']['OnAir']['media']['song']
            hora = formatar_hora_brasil().split(" / ")[1] # Pega só a hora

            if song != ultima_musica:
                if singer.startswith("Com ") or singer.startswith("CLUBE"):
                    logger.info(f"NÃO É MUSICA - Música: {song} - Artista: {singer} - Hora: {hora}")
                else:
                    log_completo.append(f"Música: {song} - Artista: {singer} - Hora: {hora}<br>")
                    lista.append(f"Música: {song} - Artista: {singer}\n")
                    logger.info(f"Música: {song} - Artista: {singer} - Hora: {hora}")
                    ultima_musica = song
                if song == 'DISK RECAÍDA':
                    log_completo.append(f"<strong style='color:red;'>TOCOU A Música: {song} DO Artista: {singer} ÀS {hora}</strong><br>")
                    logger.warning(f"TOCOU A Música: {song} DO Artista: {singer} ÀS {hora}")
            else:
                #log_completo.append(f"Música repetida ou sem alteração: {song} - Hora: {hora}<br>")
                logger.info(f"Música repetida ou sem alteração: {song} - Hora: {hora}")
            f"<pre>Música: {song} - Artista: {singer} - Hora: {hora}<br></pre>"

        except requests.exceptions.RequestException as e:
            error_msg = f"Erro ao acessar o JSON: {e}<br>"
            log_completo.append(error_msg)
            logger.error(error_msg)
        except (KeyError, json.JSONDecodeError) as e:
            error_msg = f"Erro ao processar o JSON: {e}<br>"
            log_completo.append(error_msg)
            logger.error(error_msg)

        sleep(50) # Reduzi para teste, você pode voltar para 30 ou a sua lógica original
        contagem += 1

    fim = formatar_hora_brasil()
    log_completo.append(f"============FIM============{fim}<br>")
    return "".join(log_completo), "".join(lista)

@app.route('/ler')
def ler_pagina():
    loops = int(request.args.get('loops', 90)) # Padrão: 90 loops
    resultado = ''
    resultado, lista = executar_monitoramento(loops)
    logger.info(lista)
    enviaWhatsApp(lista)
    return f"<h1>Sequência Clube FM:</h1><pre>{resultado}</pre>"

@app.route('/escrito')
def pagina_escrito():
    return "<h1>Esta acessando...</h1>"

@app.route('/')
def home():
    return "<h1>BEM VINDO A LEITURA DA CLUBE</h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
