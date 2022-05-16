FROM debian:bullseye

RUN apt-get update && apt-get install socat -y

WORKDIR /app
COPY chall .
COPY flag.txt .
COPY crash-flag.txt .
COPY run.sh .

RUN useradd -ms /bin/bash ctf
USER ctf
EXPOSE 6008
ENTRYPOINT ["socat", "TCP-LISTEN:6008,fork,reuseaddr", "EXEC:'./run.sh',stderr"]
