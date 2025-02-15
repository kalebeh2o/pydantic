# Instruções de Execução

## 1. Configuração do Ambiente Virtual

1. Crie o ambiente virtual:

   ```bash
   python -m venv venv
   ```

2. Ative o ambiente:

   ```bash
   .\venv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## 2. Configuração do Ambiente Virtual

1. tenha instalado o docker.

2. Suba o container `PostgreSQL`:

   ```bash
   docker-compose up -d
   ```
   - Caso não tenha o docker, você pode mudar o .env `DATABASE_URL` para o seu banco postgresql!
## 3. Rodando a Aplicação

1. Execute:

    ```bash
    python init_db.py
    ```

2. Execute:

    ```bash
    uvicorn main:app --reload
    ```
   - Acesse em http://127.0.0.1:8000. 
   - Acesse o Swagger em http://127.0.0.1:8000/docs
## 4. Rodando testes

1. Execute os testes com:

    ```bash
    pytest -s
    ```