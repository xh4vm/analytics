# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	BLACK        := $(shell printf "\033[30m")
	RED          := $(shell printf "\033[91m")
	GREEN        := $(shell printf "\033[92m")
	YELLOW       := $(shell printf "\033[33m")
	BLUE         := $(shell printf "\033[94m")
	PURPLE       := $(shell printf "\033[95m")
	ORANGE       := $(shell printf "\033[93m")
	WHITE        := $(shell printf "\033[97m")
	RESET        := $(shell printf "\033[00m")
else
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	BLUE         := ""
	PURPLE       := ""
	ORANGE       := ""
	WHITE        := ""
	RESET        := ""
endif

define log
	@echo ""
	@echo "${WHITE}----------------------------------------${RESET}"
	@echo "${BLUE}[+] $(1)${RESET}"
	@echo "${WHITE}----------------------------------------${RESET}"
endef

.PHONY: run mongo containers
mongo: run_containers

.PHONY: interactive build mongo cluster
mongo_cfg: config_cluster create_mongo_db create_collections

.PHONY: run docker containers
run_containers:
	$(call log,Run containers)
	sudo docker-compose --profile mongo up

.PHONY: configure the cluster
config_cluster:
	$(call log,Configure the cluster)
	sudo docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
	sudo docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
	sudo docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
	sudo docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
	sudo docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'

.PHONY: create database
create_mongo_db:
	$(call log,Create database)
	sudo docker exec -it mongors1n1 bash -c 'echo "use movies_db" | mongosh'
	sudo docker exec -it mongos1 bash -c 'echo "sh.enableShardZing(\"movies_db\")" | mongosh'

.PHONY: create collections
create_collections:
	$(call log,Create collections)
	sudo docker exec -it mongos1 bash -c 'echo "db.createCollection(\"movies_db.likes_collection\")" | mongosh'
	sudo docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"movies_db.likes_collection\", {\"film_id\": \"hashed\"})" | mongosh'