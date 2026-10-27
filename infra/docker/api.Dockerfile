FROM python:3.12-slim

WORKDIR /repo

# Install shared contracts + api
COPY packages/shared/python /repo/packages/shared/python
COPY apps/api /repo/apps/api
COPY pyproject.toml /repo/

RUN pip install --no-cache-dir -e packages/shared/python -e "apps/api[dev]"

EXPOSE 8000
CMD ["sh", "-c", "alembic -c apps/api/alembic.ini upgrade head && uvicorn app.main:app --app-dir apps/api --host 0.0.0.0 --port 8000"]
