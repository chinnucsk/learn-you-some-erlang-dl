#!/usr/bin/env python2.7
# coding=utf-8

import os
import hashlib
import urllib2
import re
from pprint import pprint as pp
from sys import exit

BASEURL = 'http://learnyousomeerlang.com/'
CWD = os.path.dirname(os.path.abspath(__file__))
CACHEDIR = os.path.join(CWD, '.cache')
BUILDDIR = os.path.join(CWD, 'build')

if not os.path.exists(CACHEDIR):
    os.mkdir(CACHEDIR)

if os.path.exists(BUILDDIR):
    print 'build dir exists, but should not'
    exit(1)

os.mkdir(BUILDDIR)
os.mkdir(os.path.join(BUILDDIR, 'img'))

def hsh(s):
    return hashlib.sha1(s).hexdigest() + hashlib.md5(s).hexdigest()

def fetch_url(url):
    cfn = hsh(url)
    full_cfn = os.path.join(CACHEDIR, cfn)

    if not os.path.exists(full_cfn):
        f = urllib2.urlopen(url)
        data = f.read()
        f.close()

        fp = open(full_cfn, 'wb')
        fp.write(data)
        fp.close()

    data = open(full_cfn, 'rb').read()
    return data


noscript_re = re.compile('<div class="noscript"><noscript>.+?</noscript></div>', 
    re.MULTILINE+re.DOTALL)
def cleanup_html(h):
    return noscript_re.sub('', h)

total_inner = u''
toc_html = u''

# first download toc
toc = fetch_url(BASEURL+'contents')

# find print css
print_css_re = re.compile('<link rel="stylesheet" type="text/css" href="(.+?)" media="print" />')
for pcss in print_css_re.findall(toc):
    break
else:
    print 'no print css'
    exit(1)

css = fetch_url(pcss).replace('border-top: 1px solid #930;', '')
css += '''
body, div#content, p {
    font-size: 14pt;
    font-family: "PT Sans" !important;
}
div.toc-1 {
}
div.toc-2 {
    margin-left: 20pt;
}
a[name] {
    color: black;
    text-decoration: none;
}
'''
open(os.path.join(BUILDDIR, 'print.css'), 'w').write(css)

toc_section_re = re.compile('<h3><a class="local chapter" href="([^"]+?)">(.+?)</a></h3>')
section_re = re.compile('<h2>(.+?)</h2>')
subsection_re = re.compile('<h3><a.+?name="(.+?)">(.+?)</a></h3>')
img_re = re.compile('<img.+?src="(.+?)".+?(?:title="(.+?)")?.+?>')
aname_re = re.compile('<a.+?name="(.+?)">')
alink_re = re.compile(BASEURL.replace('.', '\\.')+'(.+?)#(.+?)"')
res = toc_section_re.findall(toc)

for link, title in res:
    section_name = os.path.basename(link)
    section = fetch_url(link).decode('utf-8')
    r = section_re.findall(section)
    section_title = r[0]
    toc_html += u'<div class="toc-1"><a href="#{}">{}</a></div>\n'.format(section_name, section_title)

    # find section begin and end positions
    start = section.find('<div id="content">')
    end = section.find('<ul class="navigation">')

    html = cleanup_html(section[start:end] + '</div>')

    # find and download pictures
    images = img_re.findall(section)
    for img_url, img_title in images:
        img_data = fetch_url(img_url)
        img_filename = os.path.basename(img_url)
        open(os.path.join(BUILDDIR, 'img', img_filename), 'wb').write(img_data)

        html = html.replace(img_url, 'img/'+img_filename)

    # correct internal links
    html = aname_re.sub(lambda mo: mo.group(0).replace('name="{}"'.format(mo.group(1)), 'name="{}---{}"'.format(section_name, mo.group(1))), html)
    html = alink_re.sub(lambda mo: '#'+mo.group(1)+'---'+mo.group(2)+'"', html)

    for a,b in subsection_re.findall(html):
        toc_html += u'<div class="toc-2"><a href="#{}">{}</a></div>\n'.format(a, b)

    html = section_re.sub(lambda mo: '<h2><a name="{0}">{1}</a></h2>'.format(section_name, mo.group(1)), html)

    total_inner += html

cover_html = u'''
<h1>Learn You some Erang For Great Good</h1>
<h2>by Fred Hebert</h2>
'''

res = u'''<html><head>
<meta http-equiv="Content-type" content="text/html; charset=UTF-8">
<title>Learn You some Erang For Great Good — Fred Hebert</title>
<link rel="stylesheet" type="text/css" href="print.css">
</head><body>''' + \
    cover_html + \
    toc_html + \
    total_inner + \
'''</body></html>'''

open(os.path.join(BUILDDIR, 'index.html'), 'wb').write(res.encode('utf-8'))
