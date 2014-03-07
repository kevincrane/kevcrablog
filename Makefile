.PHONY: docs test

APP_NAME = thekevincrane

help:
	@echo "$(APP_NAME) Makefile"
	@echo "  env    create a development environment using virtualenv (NOTE: doesn't really work, I like virtualenvwrapper better)"
	@echo "  deps   install dependencies using pip"
	@echo "  clean  remove unwanted files like .pyc's"
	@echo "  lint   check style with flake8"
	@echo "  test   run all your tests using py.test"

#env:
#	sudo easy_install pip && \
		pip install virtualenvwrapper && \
		mkvirtualenv $(APP_NAME) && \
		workon $(APP_NAME) && \
		make deps

deps:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;

lint:
	flake8 --exclude=env .

test:
	py.test tests
