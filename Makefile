py_sources = raterapid/
target_version = py311
test_files =

check:
	mkdir -p reports
	mypy ${py_sources}
	black --check --diff --target-version=${target_version} ${py_sources}
	flake8 --format=html --htmldir=reports/flake8-report ${py_sources}
	isort --check --diff ${py_sources}

format:
	autoflake --in-place --recursive ${py_sources}
	isort ${py_sources}
	black --target-version=${target_version} ${py_sources}

test:
	coverage erase
	coverage run --concurrency=multiprocessing manage.py test ${test_files} --parallel=2

test-report:
	coverage combine
	coverage report || true
	coverage html || true
	coverage xml || true

deploy:
	docker compose up --build -d

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs

ps:
	docker compose ps

