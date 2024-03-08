FROM python:3.10-slim

RUN apt-get update && apt-get install -y ca-certificates curl gnupg git && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    NODE_MAJOR=20 && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install -y nodejs

WORKDIR /app
RUN git clone https://github.com/kurpau/SET-scraping-bot.git .

WORKDIR /app/server
RUN python3.10 -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt

RUN . .venv/bin/activate && \
    playwright install webkit && \
    playwright install-deps

WORKDIR /app/client
RUN npm install && npm run build

RUN cp -r dist/* ../server/app/static/

WORKDIR /app/server

EXPOSE 8000

WORKDIR /app/server
CMD ["/bin/bash", "-c", "source .venv/bin/activate && python wsgi.py"]


