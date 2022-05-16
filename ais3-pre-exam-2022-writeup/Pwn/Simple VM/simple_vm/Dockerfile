FROM ubuntu:20.04
MAINTAINER u1f383

RUN apt-get update && \
    DEBAIN_FRONTEND=noninteractive apt-get install -qy xinetd

RUN useradd -m simple_vm
RUN chown -R root:root /home/simple_vm
RUN chmod -R 755 /home/simple_vm

CMD ["/usr/sbin/xinetd", "-dontfork"]