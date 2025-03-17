from fastapi import FastAPI, HTTPException
import subprocess
import os

app = FastAPI()

def executar_script():
    """Função para executar o script Python."""
    try:
        result = subprocess.run(['python', 'clubeselenium.py'], capture_output=True, text=True, check=True)
        print("Script executado com sucesso:")
        print(result.stdout)
        if result.stderr:
            print("Erros (stderr):")
            print(result.stderr)
        return "Script executado com sucesso!"
    except subprocess.CalledProcessError as e:
        error_message = f"Erro ao executar o script: {e}\nStdout: {e.stdout}\nStderr: {e.stderr}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Erro: script 'clubeselenium.py' não encontrado")

@app.get('/agendar_script')
async def agendar_endpoint():
    return executar_script()
