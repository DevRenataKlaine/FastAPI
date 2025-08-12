FROM python:3.13-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install streamlit

RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8501
CMD ['streamlit', 'run', 'app.py', '--server.port=8501', '--server.adress=0.0.0.0']
