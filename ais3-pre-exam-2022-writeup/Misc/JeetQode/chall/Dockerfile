FROM python:3.10

RUN apt-get update && apt-get install socat jq -y
RUN pip install dataclasses-json

WORKDIR /app
COPY server.py .
COPY helper.py .
COPY problem.py .
COPY problems problems
COPY flag.txt .

RUN useradd -ms /bin/bash ctf
USER ctf
EXPOSE 6006
ENTRYPOINT ["socat", "TCP-LISTEN:6006,fork,reuseaddr", "EXEC:'python server.py',stderr"]
