from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import ConfigDict

class EmpresaBase(BaseModel):
    nome: str
    cnpj: str
    endereco: Optional[str] = None
    email: Optional[EmailStr] = None  
    telefone: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Empresa Exemplo",
                "cnpj": "12345678000100",
                "email": "contato@empresa.com",
                "endereco": "Rua das Flores, 123",
                "telefone": "(11) 1234-5678"
            }
        }
    )

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "Empresa Exemplo",
                "cnpj": "12345678000100",
                "email": "contato@empresa.com",
                "endereco": "Rua das Flores, 123",
                "telefone": "(11) 1234-5678"
            }
        }
    )

class ObrigacaoAcessoriaBase(BaseModel):
    nome: str
    periodicidade: str  

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "Declaração de Impostos",
                "periodicidade": "mensal",
                "empresa_id": 1
            }
        }
    )

class ObrigacaoAcessoriaCreate(ObrigacaoAcessoriaBase):
    empresa_id: int

class ObrigacaoAcessoria(ObrigacaoAcessoriaBase):
    id: int
    empresa_id: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "Declaração de Impostos",
                "periodicidade": "mensal",
                "empresa_id": 1
            }
        }
    )
