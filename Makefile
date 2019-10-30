
run: | build clean
	sudo docker-compose up

deploy: | build clean
	sudo docker-compose up -d

build:
	sudo docker-compose build

clean: kill
	sudo docker-compose rm -f

kill:
	sudo docker-compose down