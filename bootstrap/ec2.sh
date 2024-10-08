sudo apt-get update
sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs

ssh-keygen -t rsa -b 4096 -C "fozail.i.ahmad@gmail.com"
cat ~/.ssh/id_rsa.pub

mkdir neo4j
cd neo4j/
mkdir versions
cd versions/
mkdir 5.1.0
mkdir 5.4.0
mkdir 5.20.0
mkdir 5.21.2
cd 5.1.0/
mkdir backups
mkdir data
mkdir logs
cd ../5.4.0/
mkdir backups
mkdir data
mkdir logs
cd ../5.20.0/
mkdir backups
mkdir data
mkdir logs
cd ../5.21.2/
mkdir backups
mkdir data
mkdir logs
cd /$HOME
mkdir dev
cd dev/
git clone git@github.com:neo4j-graph-examples/recommendations.git
git clone git@github.com:FozAhm/GraphGenie.git

cp ~/dev/recommendations/data/recommendations-50.dump ~/neo4j/versions/5.1.0/backups/recommendations-50.dump
cp ~/neo4j/versions/5.1.0/backups/recommendations-50.dump ~/neo4j/versions/5.1.0/backups/neo4j.dump
cp ~/dev/recommendations/data/recommendations-50.dump ~/neo4j/versions/5.4.0/backups/recommendations-50.dump
cp ~/neo4j/versions/5.4.0/backups/recommendations-50.dump ~/neo4j/versions/5.4.0/backups/neo4j.dump
cp ~/dev/recommendations/data/recommendations-50.dump ~/neo4j/versions/5.20.0/backups/recommendations-50.dump
cp ~/neo4j/versions/5.20.0/backups/recommendations-50.dump ~/neo4j/versions/5.20.0/backups/neo4j.dump
cp ~/dev/recommendations/data/recommendations-50.dump ~/neo4j/versions/5.21.2/backups/recommendations-50.dump
cp ~/neo4j/versions/5.21.2/backups/recommendations-50.dump ~/neo4j/versions/5.21.2/backups/neo4j.dump

sudo docker pull neo4j/neo4j-admin:5.1.0-community
sudo docker pull neo4j/neo4j-admin:5.4.0-community
sudo docker pull neo4j/neo4j-admin:5.20.0-community
sudo docker pull neo4j/neo4j-admin:5.21.2-community
sudo docker pull neo4j:5.1.0-community
sudo docker pull neo4j:5.4.0-community
sudo docker pull neo4j:5.20.0-community
sudo docker pull neo4j:5.21.2-community


