# Se utiliza de base imagen de python con python 3.6
FROM ubuntu:18.04
# Agregamos los requerimientos a la imagen
ADD requirements.txt /app/requirements.txt

# update repos
RUN apt-get update -y && apt-get upgrade -y

# instalar deps
RUN apt-get install -y build-essential libpq-dev \
	python3-dev python libffi-dev python3-pip wget \
	pkg-config libpng-dev git python-dev

RUN pip3 install --upgrade setuptools

WORKDIR /app/

# Instalar dependencias de python
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN export LC_ALL=es_ES.UTF-8

# Crear usuario sin privilegios
RUN adduser --disabled-password --gecos '' app
RUN chown -R app:app /app && chmod -R 755 /app

ENV HOME /home/app
USER app