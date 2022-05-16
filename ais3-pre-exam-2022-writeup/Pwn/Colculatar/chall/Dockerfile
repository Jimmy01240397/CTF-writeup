FROM ubuntu:20.04
MAINTAINER u1f383

RUN apt-get update && \
    DEBAIN_FRONTEND=noninteractive apt-get install -qy xinetd

RUN useradd -m colculatar
RUN chown -R root:root /home/colculatar
RUN chmod -R 755 /home/colculatar

CMD ["/usr/sbin/xinetd", "-dontfork"]