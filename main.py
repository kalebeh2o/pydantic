from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
import models
import schemas
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base

app = FastAPI(
    title="Api de empresas ",  
    description="Api de exame técnico",
    version="1.0.0", 
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/empresas/", response_model=schemas.Empresa, description="Cria uma nova empresa.")
def create_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = models.Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.get("/empresas/", response_model=List[schemas.Empresa], description="Obtém a lista de todas as empresas cadastradas.")
def read_empresas(db: Session = Depends(get_db)):
    db_empresas = db.query(models.Empresa).all()
    if not db_empresas:
        raise HTTPException(status_code=404, detail="Nenhuma empresa encontrada.")
    return db_empresas

@app.get("/empresas/{empresa_id}", response_model=schemas.Empresa, description="Obtém os dados de uma empresa específica.")
def read_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return db_empresa

@app.put("/empresas/{empresa_id}", response_model=schemas.Empresa, description="Atualiza os dados de uma empresa específica.")
def update_empresa(empresa_id: int, empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    for key, value in empresa.model_dump().items():
        setattr(db_empresa, key, value)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@app.delete("/empresas/{empresa_id}", response_model=schemas.Empresa, description="Deleta uma empresa específica.")
def delete_empresa(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if db_empresa is None:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    db.delete(db_empresa)
    db.commit()
    return db_empresa

@app.post("/obrigacoes_acessorias/", response_model=schemas.ObrigacaoAcessoria, description="Cria uma nova obrigação acessória.")
def create_obrigacao_acessoria(obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.model_dump())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.get("/obrigacoes_acessorias/", response_model=List[schemas.ObrigacaoAcessoria], description="Obtém a lista de todas as obrigações acessórias.")
def read_obrigacoes_acessorias(db: Session = Depends(get_db)):
    db_obrigacoes = db.query(models.ObrigacaoAcessoria).all()
    if not db_obrigacoes:
        raise HTTPException(status_code=404, detail="Nenhuma obrigação acessória encontrada.")
    return db_obrigacoes

@app.get("/obrigacoes_acessorias/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria, description="Obtém os dados de uma obrigação acessória específica.")
def read_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(get_db)):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada.")
    return db_obrigacao

@app.put("/obrigacoes_acessorias/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria, description="Atualiza os dados de uma obrigação acessória específica.")
def update_obrigacao_acessoria(obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaCreate, db: Session = Depends(get_db)):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada.")
    for key, value in obrigacao.model_dump().items():
        setattr(db_obrigacao, key, value)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

@app.delete("/obrigacoes_acessorias/{obrigacao_id}", response_model=schemas.ObrigacaoAcessoria, description="Deleta uma obrigação acessória específica.")
def delete_obrigacao_acessoria(obrigacao_id: int, db: Session = Depends(get_db)):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if db_obrigacao is None:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada.")
    db.delete(db_obrigacao)
    db.commit()
    return db_obrigacao
