default: clean build

pdf: clean build
	cd build && xhtml2pdf index.html learn-you-some-erlang.pdf

clean:
	rm -rf build

build:
	python2.7 dl.py

clean-cache:
	rm -rf .cache
