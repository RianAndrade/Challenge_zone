# Challenge Zone 

**Challenge Zone** é uma API de gerenciamento de propriedades para hospedagem.  
Ele permite cadastrar imóveis (com endereço, capacidade, preço por noite), consultar, atualizar e excluir propriedades via API REST, além de gerenciar reservas.

---

## 🚀 Tecnologias Utilizadas

- [Python 3.12](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) — framework web para criação da API
- [PostgreSQL 16](https://www.postgresql.org/) — banco de dados relacional
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Alembic](https://alembic.sqlalchemy.org/) — controle de migrações
- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) — containerização e orquestração

---

## 📦 Dependências

O único pré-requisito é possuir **Docker** e **Docker Compose** instalados.

---

## 🔧 Como rodar o projeto


1. Clone este repositório:
```bash
   git clone git@github.com:RianAndrade/Challenge_zone.
```


2. Crie um arquivo .env na raiz (mesma pasta que o docker-compose.yml) com base no exemplo:

```bash
    POSTGRES_DB=appdb
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    DB_HOST=db
    DB_PORT=5432
```

3. Certifique-se de que essas portas estejam livres antes de rodar os containers.

As portas Utilizadas são:


| Porta | Serviço         |
|-------|-----------------|
| 8000  | Backend FastAPI |
| 5432  | PostgreSQL      |



4. Suba os containers:

```bash
    docker compose up --build
```

## 👉 Como acessar o projeto

A API estará disponível em:

```bash
    http://localhost:8000
```

A documentação interativa (Swagger UI) pode ser acessada em:

```bash
    http://localhost:8000/docs
```

