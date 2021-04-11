docker build --target dev -t soar .
docker run -p 8888:8888 --name soar -v "$(pwd)/src":/root/src -d soar

# notes
# docker build --target tutorials -t soar .
# docker tag soar docker.pkg.github.com/kierangilliam/soar/soar-tutorial
# docker push docker.pkg.github.com/kierangilliam/soar/soar-tutorial:latest