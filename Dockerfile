FROM ubuntu:18.04

# Soar dependencies
RUN apt-get update
RUN apt-get install -y build-essential swig openjdk-8-jdk git software-properties-common

# Setup dev environment
RUN apt-get install -y vim 
RUN echo "set -o vi" >> ~/.bashrc

# Python 3 dependencies
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.8
RUN apt-get install -y python3-distutils python3-dev

WORKDIR /root/

RUN git clone --depth 1 https://github.com/SoarGroup/Soar.git
WORKDIR /root/Soar
# Build
RUN python3.8 scons/scons.py all --python=/usr/bin/python3
WORKDIR /root/Soar/out
RUN echo "export SOAR_HOME=~/Soar/out" >> ~/.bashrc
# Ensure that addition to bashrc is loaded
SHELL ["/bin/bash","-c"] 

WORKDIR /root/

# Setup pysoarlib
RUN echo "export PYTHONPATH=${PYTHONPATH}:~/Soar/out" >> ~/.bashrc
RUN git clone https://github.com/amininger/pysoarlib
RUN mv pysoarlib/example/* ./

# Keep container alive
ENTRYPOINT ["tail", "-f", "/dev/null"]
