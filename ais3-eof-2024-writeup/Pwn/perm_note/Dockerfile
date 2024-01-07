FROM ubuntu:20.04@sha256:bac6081102aae54ba4bcc714695b8f637e42768c7f376f374c428bab043ddc0f
MAINTAINER YingMuo

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install xinetd -qy
RUN useradd -m perm_note
RUN chown -R root:root /home/perm_note
RUN chmod -R 755 /home/perm_note

CMD ["/usr/sbin/xinetd","-dontfork"]
