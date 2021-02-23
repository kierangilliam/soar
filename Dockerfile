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
RUN apt-get install -y python3-distutils python3-dev python3-pip

WORKDIR /root

RUN git clone --depth 1 https://github.com/SoarGroup/Soar.git
WORKDIR /root/Soar
# Build
RUN python3.8 scons/scons.py all --python=/usr/bin/python3
RUN echo "export SOAR_HOME=~/Soar/out" >> ~/.bashrc
# Ensure that addition to bashrc is loaded
SHELL ["/bin/bash","-c"] 

# Install jupyter dependencies
RUN pip3 install notebook jupyter_contrib_nbextensions
# jupyter extensions setup
RUN jupyter contrib nbextension install --user
RUN mkdir -p $(jupyter --data-dir)/nbextensions
# vim bindings
RUN git clone https://github.com/lambdalisue/jupyter-vim-binding $(jupyter --data-dir)/nbextensions/vim_binding
RUN chmod -R go-w $(jupyter --data-dir)/nbextensions/vim_binding
# code folding
RUN jupyter nbextension enable codefolding/main


WORKDIR /root
RUN mkdir src
WORKDIR /root/src

# Setup pysoarlib
RUN echo "export PYTHONPATH=${PYTHONPATH}:~/Soar/out" >> ~/.bashrc

# Expose jupyter notebook port
EXPOSE 8888

# Dev tools
# vim bindings in bash
RUN set -o vi

# Keep container alive
ENTRYPOINT ["tail", "-f", "/dev/null"]
