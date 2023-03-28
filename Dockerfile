FROM python:3.10-slim
WORKDIR /task_manager
RUN pip install poetry
COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install
COPY task_manager/ .
CMD poetry run gunicorn -b 0.0.0.0:8000 task_manager.wsgi --workers=2 --threads=2