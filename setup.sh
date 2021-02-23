docker build -t soar .
docker run --name soar -v "$(pwd)/src":/root/src -d soar

