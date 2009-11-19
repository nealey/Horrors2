# Pages per signature
SIGSIZE = 24

SUPPORT = chapauth.sty praise.tex
STORIES = stories/*.tex
ART = art/*

all: pdf epub
pdf: horrors2-book.pdf 
epub: book.epub

horrors2-book.pdf: horrors2-book.ps
	ps2pdf $< $@

horrors2-book.ps: horrors2.ps
	pstops -p letter "$(shell ./enbook $(SIGSIZE))" $< > $@

horrors2.ps: horrors2.pdf
	pdftops $<

horrors2.pdf: horrors2.ltx $(SUPPORT) $(STORIES) $(ART)
	pdflatex $<
	pdflatex $<

horrors2.mdwn: horrors2.ltx $(STORIES)
	./toxhtml.py > $@

horrors2.xhtml: horrors2.mdwn head.xhtml foot.xhtml
	cat head.xhtml > $@
	markdown $< >> $@
	cat foot.xhtml >> $@

book.epub: horrors2.xhtml
	./mkepub


publish: horrors2.pdf
	cp horrors2.pdf horrors2.$(shell TZ=UTC date "+%Y-%m-%dT%H:%M:%SZ").pdf

clean:
	rm -f *aux *dvi *log
	rm -f horrors2.xhtml horrors2.mdwn book.epub
	rm -f epub/art/*
