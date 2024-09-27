start:
	poetry run uvicorn src.app.main:app --reload

generate-migration: message
	poetry run alembic revision --autogenerate -m "$(message)"

migrate:
	poetry run alembic upgrade head

rollback:
	poetry run alembic downgrade -1