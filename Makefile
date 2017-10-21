dev:
	pipenv install --dev

test:
	pipenv run trial txrwlock

doc:
	pipenv run python setup.py build_sphinx
