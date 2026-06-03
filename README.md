# TODO-API

Proyecto simple de ejemplo con Flask y PostgreSQL.

Instrucciones de ejecución:

- Con Docker (recomendado):

```bash
docker-compose up --build
```

La API estará en http://localhost:5000

- Sin Docker (entorno virtual):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DB_HOST=localhost
export DB_NAME=tododb
export DB_USER=todouser
export DB_PASSWORD=todopass
export DB_PORT=5432
python app.py
```

Ejemplo de petición:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"title":"Comprar leche"}' http://localhost:5000/todos
```

