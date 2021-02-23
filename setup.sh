docker build -t soar .
docker run -p 8888:8888 --name soar -v "$(pwd)/src":/root/src -d soar

