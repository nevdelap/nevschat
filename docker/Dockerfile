FROM python:3.11-slim as base
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get update \
    && apt-get install -y \
    nodejs \
    unzip \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip --root-user-action=ignore && \
    pip install --root-user-action=ignore \
    deepl==1.18.0 \
    jamdict==0.1a11.post2 \
    jamdict-data==1.5 \
    google-cloud-texttospeech==2.16.3 \
    openai==1.23.2 \
    requests==2.31.0
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
