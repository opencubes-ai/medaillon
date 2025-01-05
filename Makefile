install:
	pip install ./

install-with-dbks:
	pip install './[databricks]'

dev:
	pip install -e './[pulumi, polars, spark, dev, azure, aws, gcp]'

test:
	pytest --junitxml=junit/test-results.xml --cov=laktory --cov-report=xml --cov-report=html tests

coverage:
	open htmlcov/index.html

build:
	pip install build hatch
	python -m build

publish:
	pip install build hatch twine
	python -m build
	twine upload dist/*

publishdoc:
	pip install 'mkdocs<1.6' mkdocstrings[python] mkdocs-material mkdocs-video
	mkdocs gh-deploy --force