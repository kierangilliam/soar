docker build -t soar .
docker run --name soar -d soar
docker exec -t -i soar /bin/bash

python3 run_agent.py


docker kill soar && docker rm soar
