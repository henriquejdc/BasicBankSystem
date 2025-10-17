# Desafio: API Bancária Assíncrona com FastAPI

Neste desafio, você irá projetar e implementar uma API RESTful assíncrona usando FastAPI para gerenciar operações bancárias de depósitos e saques, vinculadas a contas correntes. Este desafio irá lhe proporcionar a experiência de construir uma aplicação backend moderna e eficiente que utiliza autenticação JWT e práticas recomendadas de design de APIs.

## Objetivos e Funcionalidades

O objetivo deste desafio é desenvolver uma API com as seguintes funcionalidades:

- **Cadastro de Transações:** Permita o cadastro de transações bancárias, como depósitos e saques.
- **Exibição de Extrato:** Implemente um endpoint para exibir o extrato de uma conta, mostrando todas as transações realizadas.
- **Autenticação com JWT:** Utilize JWT (JSON Web Tokens) para garantir que apenas usuários autenticados possam acessar os endpoints que exigem autenticação.

## Requisitos Técnicos

Para a realização deste desafio, você deve atender aos seguintes requisitos técnicos:

- **FastAPI:** Utilize FastAPI como framework para criar sua API. Aproveite os recursos assíncronos do framework para lidar com operações de I/O de forma eficiente.
- **Modelagem de Dados:** Crie modelos de dados adequados para representar contas correntes e transações. Garanta que as transações estão relacionadas a uma conta corrente, e que contas possam ter múltiplas transações.
- **Validação das operações:** Não permita depósitos e saques com valores negativos, valide se o usuário possui saldo para realizar o saque.
- **Segurança:** Implemente autenticação usando JWT para proteger os endpoints que necessitam de acesso autenticado.
- **Documentação com OpenAPI:**  Certifique-se de que sua API esteja bem documentada, incluindo descrições adequad
as para cada endpoint, parâmetros e modelos de dados.

## Instalação e Execução

1. Clone o repositório:
   ```bash
   git clone <repo-url>
   cd bank-fastapi
   ```
2. Instale as dependências:
   ```bash
   pip install poetry
   poetry install
   ```
3. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:
   ```env
   DATABASE_URL=sqlite:///./bank.db
   ENVIRONMENT=development
   JWT_SECRET=sua-chave-secreta
   JWT_ALGORITHM=HS256
   CORS_ORIGINS=http://localhost,http://127.0.0.1
   ```
4. Execute as migrações:
   ```bash
   poetry run alembic upgrade head
   ```
5. Inicie a aplicação:
   ```bash
   poetry run uvicorn src.main:app --reload
   ```

## Variáveis de Ambiente

- `DATABASE_URL`: URL de conexão com o banco de dados.
- `ENVIRONMENT`: Ambiente de execução (`development`, `production`, etc).
- `JWT_SECRET`: Chave secreta para geração dos tokens JWT.
- `JWT_ALGORITHM`: Algoritmo do JWT (ex: HS256).
- `CORS_ORIGINS`: Lista de origens permitidas para CORS, separadas por vírgula.

## Exemplos de Uso

### Criar Conta
```http
POST /accounts/
Content-Type: application/json
Authorization: Bearer <token>

{
  "user_id": 123,
  "balance": 100.0
}
```

### Listar Contas
```http
GET /accounts/?limit=10&skip=0
Authorization: Bearer <token>
```

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "user_id": 123
}
```

### Resposta de Login
```json
{
  "access_token": "<jwt-token>"
}
```
