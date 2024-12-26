run:
	docker run -it -d --restart=unless-stopped --name easy_refer ChertikBot
stop:
	docker stop easy_refer
attach:
	docker attach easy_refer
dell:
	docker rm easy_refer