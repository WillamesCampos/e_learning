test:
	coverage run --source='.' manage.py test -v2
	coverage report

test_parallel:
	manage.py test --parallel -v2

requirements:
	poetry export --format=requirements.txt --output=requirements.txt --without-hashes

celery:
	docker stop redis || true;
	docker container rm redis || true;
	docker run -d --rm --name redis -p 6379:6379 redis;
	rm celerybeat.pid || true;
	celery -A e_learning.celerybeat-schedule beat --detach;
	celery -A e_learning worker -l INFO;
