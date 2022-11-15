.PHONY: start start_build stop unit_tests check_typing unit_tests_local

UNIT_TESTS=pytest tests --asyncio-mode=strict
CHECK_LINT=/bin/sh -c "mypy . \
    && isort --check-only . \
    && black --check . \
	&& flake8 app models tests"

start:
	@docker-compose up -d

start_build:
	@docker-compose up --build -d

stop:
	@docker-compose down

unit_tests_ci:
	@docker-compose exec -T app-test \
	$(UNIT_TESTS)

unit_tests:
	@docker-compose exec app-test \
	$(UNIT_TESTS)

unit_tests_local:
	@$(UNIT_TESTS)

check_lint_ci:
	@docker-compose exec -T app-test $(CHECK_LINT)

check_lint:
	@docker-compose exec app-test $(CHECK_LINT)

fix_lint:
	@docker-compose exec app-test /bin/sh -c "isort . && black ."
