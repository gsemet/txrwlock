.PHONY: build doc

all: dev requirements test dists doc

dev:
	pipenv install --dev

test:
	pipenv run trial txrwlock

coverage:
	pipenv run trial --coverage txrwlock

doc:
	pipenv run python setup.py build_sphinx

pylint:
	pipenv run pylint --rcfile .pylintrc txrwlock

yapf:
	pipenv run yapf --recursive -i txrwlock

dists:
	python setup.py sdist bdist bdist_wheel

requirements:
	pipenv run pipenv_to_requirements

clean:
	pipenv --rm
