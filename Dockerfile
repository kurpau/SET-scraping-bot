FROM python:3.10-slim

RUN apt-get update && apt-get install -y ca-certificates curl gnupg git && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    NODE_MAJOR=20 && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install -y nodejs

WORKDIR /app
RUN git clone https://github.com/kurpau/SET-scraping-bot.git .

WORKDIR /app/server
RUN pip install -r requirements.txt

RUN python -m playwright install webkit
RUN python -m playwright install-deps

WORKDIR /app/client
RUN npm install && npm run build

RUN cp -r dist/* ../server/app/static/

WORKDIR /app/server

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

