FROM python:3.12-slim

ARG PROJECT=app

RUN groupadd --gid 1000 user &&  adduser --disabled-password --gecos '' --uid 1000 --gid 1000 user
USER user

WORKDIR /home/user

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/user/.local/bin:${PATH}"

COPY --chown=user:user requirements.lock ./
COPY --chown=user:user .env ./
RUN --mount=type=cache,target=/root/.cache pip install -r ./requirements.lock

COPY --chown=user:user ./$PROJECT ./$PROJECT

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
