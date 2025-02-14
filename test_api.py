import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Empresa, ObrigacaoAcessoria
from schemas import EmpresaCreate, ObrigacaoAcessoriaCreate
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def db_session():
    db = SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def create_empresa(db_session):
    empresa_data = EmpresaCreate(
        nome="Empresa Teste",
        cnpj="12345678000100",
        endereco="Rua Teste, 123",
        email="empresa@teste.com",
        telefone="1234567890"
    )
    empresa = Empresa(**empresa_data.model_dump())
    db_session.add(empresa)
    db_session.commit()
    db_session.refresh(empresa)
    print(f"Empresa criada: {empresa.id} - {empresa.nome}")
    return empresa

@pytest.fixture
def create_obrigacao(db_session, create_empresa):
    obrigacao_data = ObrigacaoAcessoriaCreate(
        nome="Obrigação Teste",
        periodicidade="Mensal",
        empresa_id=create_empresa.id
    )
    obrigacao = ObrigacaoAcessoria(**obrigacao_data.model_dump())
    db_session.add(obrigacao)
    db_session.commit()
    db_session.refresh(obrigacao)
    print(f"Obrigação criada: {obrigacao.id} - {obrigacao.nome}")
    return obrigacao

def test_create_empresa(db_session):
    empresa_data = {
        "nome": "Nova Empresa",
        "cnpj": "98765432000100",
        "endereco": "Av. Exemplo, 456",
        "email": "nova@empresa.com",
        "telefone": "9876543210"
    }
    print(f"Enviando dados para criar a empresa: {empresa_data}")
    response = client.post("/empresas/", json=empresa_data)
    print(f"Resposta da criação da empresa: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert response.json()["nome"] == empresa_data["nome"]

def test_read_empresas(db_session, create_empresa):
    print("Buscando empresas...")
    response = client.get("/empresas/")
    print(f"Resposta da busca por empresas: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    empresas = response.json()
    assert len(empresas) > 0
    assert empresas[0]["id"] == create_empresa.id

def test_update_empresa(db_session, create_empresa):
    updated_data = {
        "nome": "Empresa Atualizada",
        "cnpj": "98765432000101",
        "endereco": "Rua Atualizada, 789",
        "email": "atualizada@empresa.com",
        "telefone": "9876543212"
    }
    print(f"Enviando dados para atualizar a empresa {create_empresa.id}: {updated_data}")
    response = client.put(f"/empresas/{create_empresa.id}", json=updated_data)
    print(f"Resposta da atualização da empresa: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert response.json()["nome"] == updated_data["nome"]
    assert response.json()["cnpj"] == updated_data["cnpj"]

def test_delete_empresa(db_session, create_empresa):
    print(f"Deletando a empresa {create_empresa.id}...")
    response = client.delete(f"/empresas/{create_empresa.id}")
    print(f"Resposta da exclusão da empresa: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == create_empresa.id

def test_create_obrigacao(db_session, create_empresa):
    obrigacao_data = {
        "nome": "Nova Obrigação",
        "periodicidade": "Anual",
        "empresa_id": create_empresa.id
    }
    print(f"Enviando dados para criar a obrigação: {obrigacao_data}")
    response = client.post("/obrigacoes_acessorias/", json=obrigacao_data)
    print(f"Resposta da criação da obrigação: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert response.json()["nome"] == obrigacao_data["nome"]

def test_read_obrigacoes(db_session, create_obrigacao):
    print("Buscando obrigações acessórias...")
    response = client.get("/obrigacoes_acessorias/")
    print(f"Resposta da busca por obrigações: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    obrigacoes = response.json()
    assert len(obrigacoes) > 0
    assert obrigacoes[0]["id"] == create_obrigacao.id

def test_update_obrigacao(db_session, create_obrigacao):
    updated_data = {
        "nome": "Obrigação Atualizada",
        "periodicidade": "Mensal",
        "empresa_id": create_obrigacao.empresa_id
    }
    print(f"Enviando dados para atualizar a obrigação {create_obrigacao.id}: {updated_data}")
    response = client.put(f"/obrigacoes_acessorias/{create_obrigacao.id}", json=updated_data)
    print(f"Resposta da atualização da obrigação: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert response.json()["nome"] == updated_data["nome"]
    assert response.json()["periodicidade"] == updated_data["periodicidade"]
    assert response.json()["empresa_id"] == updated_data["empresa_id"]

def test_delete_obrigacao(db_session, create_obrigacao):
    print(f"Deletando a obrigação {create_obrigacao.id}...")
    response = client.delete(f"/obrigacoes_acessorias/{create_obrigacao.id}")
    print(f"Resposta da exclusão da obrigação: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == create_obrigacao.id
