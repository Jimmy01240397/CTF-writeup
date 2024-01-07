FROM ubuntu@sha256:bbf3d1baa208b7649d1d0264ef7d522e1dc0deeeaaf6085bf8e4618867f03494
MAINTAINER YingMuo

RUN apt-get update && \
    DEBAIN_FRONTEND=noninteractive apt-get install -qy xinetd

RUN useradd -m jackpot
RUN chown -R root:root /home/jackpot
RUN chmod -R 755 /home/jackpot

CMD ["/usr/sbin/xinetd", "-dontfork"]
