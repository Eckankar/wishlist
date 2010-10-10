#!/usr/bin/python3.1
from yaml import load
from subprocess import call
from os import chdir

def getWishlist():
    f = open('wishlist.yaml', 'r')
    return load(f)

def prepareTex():
    f = open('template.tex', 'r')
    t = open('output/wishlist.tex', 'w')
    print(f.read(), file=t)
    return t

def handleCategory(category, tex):
    print(r'\section*{', category['category'], '}', sep='', file=tex)
    for item in category['items']:
        handleItem(item, tex)

def handleItem(item, tex):
    print(r'\begin{framed}', file=tex) # TODO: framed allows pagebreaks = bad. alternative?
    print(r'\begin{center}\Large ', item['name'], r'\end{center} \par', sep='', file=tex)
    print(r'\begin{minipage}[b]{.24\textwidth}', file=tex)
    if 'image' in item:
        print(r'\includegraphics[width=\textwidth]{../images/', item['image'],'}', sep='', file=tex)
    else:
        pass # TODO: box of same size.
    print(r'\end{minipage}', file=tex)
    print(r'\begin{minipage}{.75\textwidth}', file=tex)
    if 'author' in item:
        print(r'\textbf{Author:}', item['author'], r'\par', file=tex)
    if 'maker' in item:
        print(r'\textbf{Made by:}', item['maker'], r'\par', file=tex)
    if 'isbn' in item:
        print(r'\textbf{ISBN:}', item['isbn'], r'\par', file=tex)
    if 'note' in item:
        print(item['note'], file=tex)
    print(r'\end{minipage} \par', file=tex)
    if 'links' in item:
        print(r'\begin{description}', file=tex)
        for link in item['links']:
            print(r'\item[', link['title'], r'] { \url{', link['url'], r'} }', sep='', file=tex)
        print(r'\end{description}', file=tex)
    print(r'\end{framed}', file=tex)

tex = prepareTex()
wishlist = getWishlist()
for category in wishlist['wishes']:
    handleCategory(category, tex)

print(r'\end{document}', file=tex)
tex.close()
call('pdflatex -interaction=batchmode wishlist.tex >/dev/null 2>/dev/null', cwd='output', shell=True)
