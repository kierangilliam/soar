docker build --target tutorials -t soar .
docker run -p 8888:8888 --name soar -d soar
docker exec -t -i soar /bin/bash
# Tried a few variants like the following (here and in the dockerfile)
# but kept getting the error "ModuleNotFoundError: No module named 'Python_sml_ClientInterface'"
# which I think has something to do with the SOAR_HOME path? 
# docker exec soar /bin/bash start.sh
# docker exec -t -i soar /bin/bash -c "sh start.sh"