FROM python:3.10-slim-buster

# Install dependencies for building SQLite from source
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install SQLite 3.36.0 (or a newer version)
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3460100.tar.gz && \
    tar xzvf sqlite-autoconf-3460100.tar.gz && \
    cd sqlite-autoconf-3460100 && \
    ./configure && \
    make && \
    make install

# Ensure that SQLite libraries are correctly linked
RUN ldconfig

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

RUN python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'contact@example.com', 'root')"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]