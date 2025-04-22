# The dockerfile to package the ASGI service

# Necessary environment variables
# MYSQL_USER=${USER}
# MYSQL_PASSWORD Set whatever you want
# MYSQL_DATABASE = "db"
# MYSQL_HOST="database" # for Docker container orchestration

ARG DISTRIBUTION=ghcr.io/astral-sh/uv:debian-slim
FROM $DISTRIBUTION
LABEL maintainer="Barman Roy, Swagato <swagatopablo@aol.com>"

WORKDIR /app

# Copy the necessary scripts and files
COPY *.sh ./
COPY src/*.py src/
COPY src/config.ini src/
COPY pyproject.toml ./

RUN chmod +x *.sh
# Fire up the service at container boot time.
CMD ["./run_asgi.sh"]