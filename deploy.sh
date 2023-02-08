cd /home/deploy/estatex-db-service
git fetch --all
git reset --hard origin/main

tag=$(git rev-parse --short=7 HEAD)
sudo sh build_docker_and_register.sh
cd /home/deploy/infra/workers/db-service/dev

git fetch --all
git reset --hard origin/main

sed -e "s/\${tag}/$tag/" template.yaml > deployment.yaml
git add deployment.yaml
git commit -m "deployed db-service to dev with tag $tag"
git push

sudo microk8s kubectl apply -f deployment.yaml
