FROM ubuntu:20.04
MAINTAINER LJP-TW

ENV DEBIAN_FRONTEND noninteractive

RUN dpkg --add-architecture arm64

RUN sed -i "s/deb h/deb [arch=amd64] h/g" /etc/apt/sources.list

## add arm64's repos
RUN echo "# arm64 repositories" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal main restricted" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal-updates main restricted" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal universe" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal-updates universe" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal multiverse" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal-updates multiverse" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal-backports main restricted universe multiverse" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal-security main restricted" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal-security universe" >> /etc/apt/sources.list
RUN echo "deb [arch=arm64] http://ports.ubuntu.com/ubuntu-ports focal-security multiverse" >> /etc/apt/sources.list

RUN apt-get update

RUN apt-get install xinetd -y
RUN apt-get install qemu-user qemu-user-static -y
RUN apt-get install libc6:arm64 libc6-dbg:arm64 -y
RUN useradd -m give_me_sc
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/give_me_sc
CMD ["/usr/sbin/xinetd","-dontfork"]