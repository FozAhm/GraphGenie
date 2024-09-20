sudp docker run --interactive --tty --rm --volume=$HOME/neo4j/versions/5.1.0/data:/data --volume=$HOME/neo4j/versions/5.1.0/backups:/backups neo4j/neo4j-admin:5.1.0-community neo4j-admin database dump neo4j --to-path=/backups
sudo docker run --interactive --tty --rm --volume=$HOME/neo4j/versions/5.1.0/data:/data --volume=$HOME/neo4j/versions/5.1.0/backups:/backups neo4j/neo4j-admin:5.1.0-community neo4j-admin database load --overwrite-destination=true neo4j --from-path=/backups
sudo docker run --interactive --tty --rm --volume=$HOME/neo4j/data:/data --volume=$HOME/neo4j/backups:/backups neo4j/neo4j-admin:5.16.0-bullseye neo4j-admin database load --overwrite-destination=true neo4j --from-path=/backups

sudo docker run --restart always --publish=7474:7474 --publish=7687:7687 --env NEO4J_AUTH=neo4j/mcgill123! --name neo4j -d --volume=$HOME/neo4j/data:/data --volume=$HOME/neo4j/logs:/logs neo4j:5.16.0-bullseye
sudo docker run --restart always --publish=7474:7474 --publish=7687:7687 --env NEO4J_AUTH=neo4j/mcgill123! --name neo4j -d --volume=$HOME/neo4j/versions/5.21.2/data:/data --volume=$HOME/neo4j/versions/5.21.2/logs:/logs neo4j:5.21.2-community
