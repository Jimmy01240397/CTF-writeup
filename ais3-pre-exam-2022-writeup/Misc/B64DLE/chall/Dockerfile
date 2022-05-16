FROM python:3.10

RUN apt-get update && apt-get install socat -y
RUN pip install pycryptodome

WORKDIR /app
COPY server.py .
COPY b64dle.py .
COPY five_letter_words.txt .

RUN useradd -ms /bin/bash ctf
USER ctf
EXPOSE 6000
ENTRYPOINT ["socat", "TCP-LISTEN:6000,fork,reuseaddr", "EXEC:'python server.py',stderr"]
