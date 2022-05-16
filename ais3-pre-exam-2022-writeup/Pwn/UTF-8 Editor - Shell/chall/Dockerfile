FROM debian:bullseye

RUN apt-get update && apt-get install xinetd -y

WORKDIR /app
COPY chall .
COPY flag.txt .
COPY crash-flag.txt .
COPY run.sh .
COPY xinetd /etc/xinetd.d/chall

RUN useradd -ms /bin/bash ctf
USER ctf
EXPOSE 6003
CMD ["/usr/sbin/xinetd", "-dontfork"]
