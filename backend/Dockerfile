FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client ca-certificates \
  && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 -s /usr/sbin/nologin appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

#Garantir que o Sql esta pronto para receber as migraations do alembic
#Tirar echos depois de terminar

RUN printf '%s\n' \
'#!/bin/sh' \
'set -eu' \
'echo "⏳ Aguardando Postgres ${DB_HOST:-db}:${DB_PORT:-5432}..."' \
'until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${POSTGRES_USER:-user}" >/dev/null 2>&1; do sleep 1; done' \
'echo "--- Postgres pronto"' \
'echo "--- Executando alembic upgrade head"' \
'alembic upgrade head' \
'echo "---Iniciando aplicação"' \
'exec "$@"' \
> /usr/local/bin/docker-entrypoint.sh \
 && chmod 0755 /usr/local/bin/docker-entrypoint.sh

USER appuser
EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
