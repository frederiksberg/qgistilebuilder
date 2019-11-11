
deploy: | build clean
	sudo docker-compose up -d

run: | build clean
	sudo docker-compose up

build:
	sudo docker-compose build

clean: kill
	sudo docker-compose rm -f

kill:
	sudo docker-compose down

re-ftp:
	sudo docker-compose rm -f -s ftp
	sudo docker-compose up -d ftp

logs:
	sudo docker-compose logs -f

ls-cron:
	sudo docker exec tiler crontab -l
