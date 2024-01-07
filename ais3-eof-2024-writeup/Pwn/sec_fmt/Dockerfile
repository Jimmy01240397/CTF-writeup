FROM ubuntu@sha256:bbf3d1baa208b7649d1d0264ef7d522e1dc0deeeaaf6085bf8e4618867f03494
MAINTAINER YingMuo

ENV DEBIAN_FRONTEND noninteractive

RUN dpkg --add-architecture i386
RUN apt-get update && apt-get install xinetd -qy
RUN apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386 -qy
RUN useradd -m sec_fmt
RUN chown -R root:root /home/sec_fmt
RUN chmod -R 755 /home/sec_fmt

CMD ["/usr/sbin/xinetd","-dontfork"]
