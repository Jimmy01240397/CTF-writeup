FROM python:3.10

RUN apt-get update && apt-get install socat -y
RUN pip install pycryptodome

WORKDIR /app
COPY server.py .

RUN useradd -ms /bin/bash ctf
USER ctf
EXPOSE 6007
ENTRYPOINT ["socat", "TCP-LISTEN:6007,fork,reuseaddr", "EXEC:'python server.py',stderr"]
