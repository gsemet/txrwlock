.PHONY: build doc

dev:
	pipenv install --dev

test:
	pipenv run trial txrwlock

doc:
	pipenv run python setup.py build_sphinx

pylint:
	pipenv run pylint --rcfile .pylintrc txrwlock
