tag=$(git rev-parse --short=7 HEAD)
docker build . -t localhost:32000/db-service-$tag
docker push localhost:32000/db-service-$tag
