TODO eaters demo

> In development for thirty years, Soar is a general cognitive architecture that integrates knowledge-intensive reasoning, reactive execution, hierarchical reasoning, planning, and learning from experience, with the goal of creating a general computational system that has the same cognitive abilities as humans. In contrast, most AI systems are designed to solve only one type of problem, such as playing chess, searching the Internet, or scheduling aircraft departures. Soar is both a software system for agent development and a theory of what computational structures are necessary to support human-level agents. Over the years, both software system and theory have evolved. This book offers the definitive presentation of Soar from theoretical and practical perspectives, providing comprehensive descriptions of fundamental aspects and new components.

- [MIT Press](https://mitpress.mit.edu/books/soar-cognitive-architecture#:~:text=In%20development%20for%20thirty%20years,same%20cognitive%20abilities%20as%20humans.)

## What is this repository?

This is a quick way to get started with Soar.
It includes a Dockerfile with Soar and pysoarlib. 
Pysoarlib is a way to interface with the Soar runtime using Python.

There are also tutorials included in the form of notebooks.
These follow closely the tutorials provided by the [Soar team](https://soar.eecs.umich.edu/downloads/Documentation/SoarTutorial/).
They have done the heavy-lifting of creating robust content that covers the many facets of Soar.
The tutorials included in this repo heavily paraphrase the official tutorials, often taking direct quotes where appropriate.
I aim to hit an audience with a similar background as myself (beginner AI knowledge, any level of programming knowledge, zero knowledge of Soar).


## Soar Tutorials

### Docker

Download docker [here](https://docs.docker.com/get-docker/).

> Note: If you're on linux, apt-get/snap/etc docker versions may be out of date. I recommend just using the link above and following Docker's recommended download flow. 

### Tutorials only

You can get setup with the Soar tutorials by executing the following commands.

```
docker run -p 8888:8888 --name soar-tutorial -d docker.pkg.github.com/kierangilliam/soar/soar-tutorial:latest
docker exec -t -i soar-tutorial /bin/bash
# In container
sh start.sh
```

Then open `127.0.0.1:8888`.

Stop the Jupyter Notebook process with `control-c`. 
Then type `exit` to leave the container. 
Finally, kill the container process with `docker rm -f soar-tutorial`.

These are a work in progress.
Feedback on explanations, grammar, etc, is appreciated.

### Dev mode

I use a slightly larger image for working on the tutorials. 
If you want to build Soar from source and modify the tutorials, do the following.

Clone this repo.

```
git clone https://github.com/kierangilliam/soar
```

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

`sh start.sh`

`jupyter notebook --allow-root --no-browser --ip=0.0.0.0 --NotebookApp.token=''`


In your browser navigate to `127.0.0.1:8888`.


### jupyter-notebook vim

If you are a vim user, you can enable vim shortcuts in jupyter notebook.

To do so, first go to: `http://127.0.0.1:8888/tree/tutorial#nbextensions_configurator`. 

Uncheck `disable configuration...` and then check the vim plugin.

