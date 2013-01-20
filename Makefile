default: clean build

clean:
	rm -rf build

build:
	python2.7 dl.py

clean-cache:
	rm -rf .cache
