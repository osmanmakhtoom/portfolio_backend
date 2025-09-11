FROM ubuntu:24.10

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH=/opt/portfolio

RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    libpq-dev \
    curl \
    git \
    python3.12 \
    python3.12-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3.12 -m venv $VENV_PATH
RUN $VENV_PATH/bin/pip install --upgrade pip
RUN $VENV_PATH/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="$VENV_PATH/bin:$PATH"

EXPOSE 8000

CMD ["sh", "-c", "$VENV_PATH/bin/python manage.py collectstatic --noinput && \
                  $VENV_PATH/bin/python manage.py makemigrations && \
                  $VENV_PATH/bin/python manage.py migrate && \
                  exec $VENV_PATH/bin/gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 4"]

