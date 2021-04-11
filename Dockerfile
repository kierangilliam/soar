FROM ubuntu:18.04 as builder

# Soar dependencies
RUN apt-get update
RUN apt-get install -y build-essential swig openjdk-8-jdk git software-properties-common

# Python 3 dependencies for building Soar
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.8 python3-distutils python3-dev python3-pip

WORKDIR /root

RUN git clone --depth 1 https://github.com/SoarGroup/Soar.git
WORKDIR /root/Soar
# Build
RUN python3.8 scons/scons.py all --python=/usr/bin/python3


### Other python3 dependencies
# PIL image library for visualizations in part 3
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade notebook Pillow


WORKDIR /root
RUN mkdir src
WORKDIR /root/src


# Setup pysoarlib
RUN echo "export PYTHONPATH=${PYTHONPATH}:~/Soar/out" >> ~/.bashrc
RUN echo "export SOAR_HOME=~/Soar/out" >> ~/.bashrc
# Vim bindings in shell
RUN echo "set -o vi" >> ~/.bashrc
# Ensure that additions to bashrc is loaded
SHELL ["/bin/bash","-c"] 


## Expose 
# 8888: jupyter notebook port
EXPOSE 8888 


FROM builder as dev
## Setup dev environment
RUN apt-get install -y vim 
## Install jupyter dependencies
RUN python3 -m pip install --upgrade jupyter_contrib_nbextensions
# jupyter extensions setup
RUN jupyter contrib nbextension install --user
RUN mkdir -p $(jupyter --data-dir)/nbextensions
# vim bindings
RUN git clone https://github.com/lambdalisue/jupyter-vim-binding $(jupyter --data-dir)/nbextensions/vim_binding
RUN chmod -R go-w $(jupyter --data-dir)/nbextensions/vim_binding
RUN jupyter nbextension enable vim_binding/vim_binding
# code folding
RUN jupyter nbextension enable codefolding/main

# Keep container alive
ENTRYPOINT ["tail", "-f", "/dev/null"]


FROM builder as tutorials
COPY . /root/
WORKDIR /root/src/tutorial
ENTRYPOINT ["tail", "-f", "/dev/null"]