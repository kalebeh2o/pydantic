from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import schemas
import service
import database
from typing import List

app = FastAPI(
    title="API de Empresas",
    description="API de exame técnico",
    version="1.0.0"
)

@app.post("/empresas/", response_model=schemas.Empresa, description="Cria uma nova empresa.")
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(database.get_db)):
    return service.create_empresa(db, empresa)

@app.get("/empresas/", response_model=List[schemas.Empresa], description="Obtém a lista de todas as empresas cadastradas.")
def read_empresas(db: Session = Depends(database.get_db)):
    return service.get_empresas(db)

@app.get("/empresas/{empresa_id}", response_model=schemas.Empresa, description="Obtém os dados de uma empresa específica.")
def read_empresa(empresa_id: int, db: Session = Depends(database.get_db)):
    return service.get_empresa(db, empresa_id)

@app.put("/empresas/{empresa_id}", response_model=schemas.Empresa, description="Atualiza os dados de uma empresa específica.")
def update_empresa(empresa_id: int, empresa: schemas.EmpresaCreate, db: Session = Depends(database.get_db)):
    return service.update_empresa(db, empresa_id, empresa)

@app.delete("/empresas/{empresa_id}", response_model=schemas.Empresa, description="Deleta uma empresa específica.")
def delete_empresa(empresa_id: int, db: Session = Depends(database.get_db)):
    return service.delete_empresa(db, empresa_id)

@app.post("/obrigacoes_acessorias/", response_model=schemas.ObrigacaoAcessoria, description="Cria uma nova obrigação acessória.")
def create_obrigacao_acessoria(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(database.get_db)):
    return service.create_obrigacao_acessoria(db, obrigacao)

@app.get("/obrigacoes_acessorias/", response_model=List[schemas.ObrigacaoAcessoria], description="Obtém a lista de todas as obrigações acessórias.")
def read_obrigacoes_acessorias(db: Session = Depends(database.get_db)):
    return service.get_obrigacoes_acessorias(db)

@app.get("/obrigacoes_acessorias/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria, description="Obtém os dados de uma obrigação acessória específica.")
def read_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(database.get_db)):
    return service.get_obrigacao_acessoria(db, obrigacao_id)

@app.put("/obrigacoes_acessorias/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria, description="Atualiza os dados de uma obrigação acessória específica.")
def update_obrigacao_acessoria(obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(database.get_db)):
    return service.update_obrigacao_acessoria(db, obrigacao_id, obrigacao)

@app.delete("/obrigacoes_acessorias/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria, description="Deleta uma obrigação acessória específica.")
def delete_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(database.get_db)):
    return service.delete_obrigacao_acessoria(db, obrigacao_id)
