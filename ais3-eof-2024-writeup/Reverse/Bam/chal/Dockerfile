FROM ubuntu:22.04
MAINTAINER ice1187

RUN apt update && apt install -y openssh-server xxd
RUN mkdir /var/run/sshd
EXPOSE 22

RUN useradd -ms /bin/bash ais3
RUN sed -i.bak -E 's/^ais3:!:/ais3:$1337$717Z2K4469HmvUWx65555449597y97m23wi35r3664Yfi72j$U79ct7Sd21h1ef04id7p351Ge3rdkbf9RfQtfMa3nbGd0do9:/g' /etc/shadow

RUN  cp /usr/lib/x86_64-linux-gnu/security/pam_unix.so /usr/lib/x86_64-linux-gnu/security/pam_unix.so.bak
COPY ./pam_unix.so /usr/lib/x86_64-linux-gnu/security/pam_unix.so
#COPY ./flag.txt /home/ais3/flag.txt

CMD ["/usr/sbin/sshd", "-D"]
