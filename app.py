from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List


class Mensagem(BaseModel):
    id: int
    conteudo: str

app = FastAPI()

def carregar_dados():
    with open('db.json', 'r') as f:
        return json.load(f)


def salvar_dados(dados):
    with open('db.json', 'w') as f:
        json.dump(dados, f, indent=4)

@app.post("/mensagens", response_model=Mensagem)
def criar_mensagem(mensagem: Mensagem):
    dados = carregar_dados()
    dados['mensagens'].append(mensagem.dict())
    salvar_dados(dados)
    return mensagem

@app.get("/mensagens", response_model=List[Mensagem])
def listar_mensagens():
    dados = carregar_dados()
    return dados['mensagens']

@app.get("/mensagens/{id}", response_model=Mensagem)
def obter_mensagem(id: int):
    dados = carregar_dados()
    mensagem = next((m for m in dados['mensagens'] if m['id'] == id), None)
    if mensagem is None:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return mensagem

@app.put("/mensagens/{id}", response_model=Mensagem)
def atualizar_mensagem(id: int, mensagem: Mensagem):
    dados = carregar_dados()
    for m in dados['mensagens']:
        if m['id'] == id:
            m['conteudo'] = mensagem.conteudo
            salvar_dados(dados)
            return m
    raise HTTPException(status_code=404, detail="Mensagem não encontrada")

@app.delete("/mensagens/{id}")
def deletar_mensagem(id: int):
    dados = carregar_dados()
    for m in dados['mensagens']:
        if m['id'] == id:
            dados['mensagens'].remove(m)
            salvar_dados(dados)
            return {"message": "Mensagem deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Mensagem não encontrada")
