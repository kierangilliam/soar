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

