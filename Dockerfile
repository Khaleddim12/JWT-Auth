# pull official base image
FROM python:3.10-slim

# Set up Django project directory
WORKDIR /django

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies

COPY requirements.txt /django/requirements.txt

# Install packages
RUN pip install --upgrade pip
RUN pip install  -r /django/requirements.txt

# copy project
COPY . .