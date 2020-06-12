# https://docs.docker.com/engine/reference/builder/#from
# https://github.com/phusion/baseimage-docker
FROM phusion/baseimage:0.11
# Ubuntu is too big 
#FROM ubuntu:latest

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disk (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# https://docs.docker.com/engine/reference/builder/#run
RUN apt-get update && \
    apt-get install -y \
# text editing
               vim \
               python3 \
               python3-pip \
               python3-dev \
#               python2.7 \
#               python-pip \
# documentation generation
               python3-sphinx \
               build-essential  \
# generate pictures of graphs using dot
               graphviz \
    && rm -rf /var/lib/apt/lists/*

# https://docs.docker.com/engine/reference/builder/#copy
# requirements.txt contains a list of the Python packages needed for the PDG
COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR       /home/appuser/app
USER appuser

COPY templates     /home/appuser/app/templates
COPY static        /home/appuser/app/static
COPY compute.py \
     config.py \
     controller.py \
     Makefile \
     /home/appuser/app/

USER root
RUN chown -R appuser /home/appuser/app && chgrp -R appuser /home/appuser/app

USER appuser
RUN echo "alias python=python3" > /home/appuser/.bashrc
RUN bash -l /home/appuser/.bashrc

# An ENTRYPOINT allows you to configure a container that will run as an executable.
ENTRYPOINT ["python3"]

# There can only be one CMD instruction in a Dockerfile
# The CMD instruction should be used to run the software contained by your image, along with any arguments. 
CMD ["/home/appuser/app/controller.py"]

