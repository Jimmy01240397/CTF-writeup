FROM archlinux:base

RUN pacman -Syyu --noconfirm
RUN pacman -S coreutils xinetd --noconfirm
RUN useradd -m ctf

CMD ["/usr/sbin/xinetd", "-dontfork"]
