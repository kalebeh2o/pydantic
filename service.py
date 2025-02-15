from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas
from fastapi import HTTPException

def create_empresa(db: Session, empresa: schemas.EmpresaCreate):
    try:
        db_empresa = models.Empresa(**empresa.model_dump())
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado. Utilize outro CNPJ.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar empresa: {str(e)}")

def get_empresas(db: Session):
    empresas = db.query(models.Empresa).all()
    if not empresas:
        raise HTTPException(status_code=404, detail="Nenhuma empresa encontrada.")
    return empresas

def get_empresa(db: Session, empresa_id: int):
    empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return empresa

def update_empresa(db: Session, empresa_id: int, empresa: schemas.EmpresaCreate):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    try:
        for key, value in empresa.model_dump().items():
            setattr(db_empresa, key, value)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado. Utilize outro CNPJ.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar empresa: {str(e)}")

def delete_empresa(db: Session, empresa_id: int):
    db_empresa = db.query(models.Empresa).filter(models.Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    db.delete(db_empresa)
    db.commit()
    return db_empresa

def create_obrigacao_acessoria(db: Session, obrigacao: schemas.ObrigacaoAcessoriaCreate):
    db_obrigacao = models.ObrigacaoAcessoria(**obrigacao.model_dump())
    db.add(db_obrigacao)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

def get_obrigacoes_acessorias(db: Session):
    obrigacoes = db.query(models.ObrigacaoAcessoria).all()
    if not obrigacoes:
        raise HTTPException(status_code=404, detail="Nenhuma obrigação acessória encontrada.")
    return obrigacoes

def get_obrigacao_acessoria(db: Session, obrigacao_id: int):
    obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if not obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada.")
    return obrigacao

def update_obrigacao_acessoria(db: Session, obrigacao_id: int, obrigacao: schemas.ObrigacaoAcessoriaCreate):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if not db_obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada.")
    for key, value in obrigacao.model_dump().items():
        setattr(db_obrigacao, key, value)
    db.commit()
    db.refresh(db_obrigacao)
    return db_obrigacao

def delete_obrigacao_acessoria(db: Session, obrigacao_id: int):
    db_obrigacao = db.query(models.ObrigacaoAcessoria).filter(models.ObrigacaoAcessoria.id == obrigacao_id).first()
    if not db_obrigacao:
        raise HTTPException(status_code=404, detail="Obrigação não encontrada.")
    db.delete(db_obrigacao)
    db.commit()
    return db_obrigacao
