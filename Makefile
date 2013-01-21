default: clean build

pdf: clean build
	cd build && xhtml2pdf index.html build.pdf && \
	gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=learn-you-some-erlang.pdf build.pdf

clean:
	rm -rf build

build:
	python2.7 dl.py

clean-cache:
	rm -rf .cache
