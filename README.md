learn-you-some-erlang-dl
========================

experimental lyse downloader

converting to PDF
=================

Open generated web page (build/index.html) in Chrome and print to A5 PDF file.

OR issue command (debian/ubuntu package `python-pisa` required, resulting pdf will be placed
to the directory `build`, file named `learn-you-some-erlang.pdf`)

    make pdf

Unfortunately, pdf created by this command does not contain embedded fonts.
