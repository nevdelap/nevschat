FROM python:3.11-slim as base
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get update && apt-get install -y \
    nodejs \
    unzip \
    && rm -rf /var/lib/apt/lists/*
RUN pip install wheel
WORKDIR /app
COPY webui .
RUN pip install -r requirements.txt
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
ENV BUN_INSTALL="/app/.bun"
RUN reflex init
ENV OPENAI_API_KEY="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"
CMD ["reflex", "run" , "--env", "prod"]
EXPOSE 3000
EXPOSE 8000
