FROM python:3.11-slim as base
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get update \
    && apt-get install -y \
    nodejs \
    unzip \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip --root-user-action=ignore && \
    pip install --root-user-action=ignore \
    `# prod` \
    openai \
    `# dev` \
    bandit \
    black \
    coverage \
    isort \
    mypy \
    pylint \
    pytest \
    pyupgrade \
    wheel
WORKDIR /app
COPY app/ .
COPY reflex/ reflex/
RUN pip install ./reflex
ENV BUN_INSTALL="/app/.bun"
RUN reflex init
ENTRYPOINT ["reflex", "run"]
CMD ["--env", "prod"]
EXPOSE 3000
EXPOSE 8000
