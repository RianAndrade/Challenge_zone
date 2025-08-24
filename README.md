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

## 💻 Pré-requisitos

Antes de começar, verifique se você atende aos seguintes requisitos:

- 🐋 Docker

- 🚪 Portas: 8000 (api), 5432 (postgres).

---

### 🧰 Variáveis de ambiente



O formato das variáveis de ambiente encontra-se no arquivo `.env.copy` e também mais abaixo neste documento .

| Variavel           | Descricao                                 |
|--------------------|-------------------------------------------|
| `POSTGRES_DB`      | Nome do banco de dados utilizado pela app |
| `POSTGRES_USER`    | Usuario do banco de dados                 |
| `POSTGRES_PASSWORD`| Senha do usuario do banco                 |
| `DB_HOST`          | Host onde o banco esta rodando (servico)  |
| `DB_PORT`          | Porta do banco de dados PostgreSQL        |


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

---

## 👉 Como acessar o projeto

Depois de que todos os containers subirem a API estará disponível em:

[http://localhost:8000](http://localhost:8000)


A documentação interativa (Swagger UI) pode ser acessada em:

[http://localhost:8000/docs](http://localhost:8000/docs)


