FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Donne les droits d’exécution au script
RUN chmod +x start.sh

EXPOSE 5000

RUN apt-get update && apt-get install -y jq

CMD ["./start.sh"]
