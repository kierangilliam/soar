# Introduction

TODO eaters demo

## What is Soar?
## What is a cognitive architecture?
## How is this different than Deep Learning?

## What is this?

This is a quick way to get started with Soar.
It includes a Dockerfile with Soar, pysoarlib, and jupyter-notebook.

There are tutorials included in the form of notebooks.
These follow closely the tutorials provided by the [Soar team](https://soar.eecs.umich.edu/downloads/Documentation/SoarTutorial/).
They have done the heavy-lifting of creating robust content that covers the many facets of Soar.
The tutorials included in this repo heavily paraphrase the official tutorials, often taking direct quotes where appropriate.
I aim to hit an audience with a similar background as myself (beginner AI knowledge, any level of programming knowledge, zero knowledge of Soar).

### Installation

Download docker [here](https://docs.docker.com/get-docker/).

    Note: If you're on linux, apt-get/snap/etc docker versions may be out of date. I recommend just using the link above and following Docker's recommended download flow. 

### Setup

From the root directory, run `sh setup.sh`.

Jump into the docker container with `sh into.sh`.

Inside of the container, you can run the simple agent script by doing:

```
python3 -m scratch.run_agent
```

### Teardown

Use the teardown script (`sh teardown.sh`) in the root directory to stop the docker container.


### Tutorials

While in the docker container, go to `~/src/tutorial` and run 

`jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --NotebookApp.token=''`


In your browser navigate to `127.0.0.1:8888`.


### jupyter-notebook vim

Go here: `http://127.0.0.1:8888/tree/tutorial#nbextensions_configurator`. 
Uncheck `disable configuration...` and then check the vim plugin.

