# Pages per signature
SIGSIZE = 24

SUPPORT = chapauth.sty praise.tex
STORIES = stories/*.tex
ART = art/*

horrors2-book.pdf: horrors2-book.ps
	ps2pdf $< $@

horrors2-book.ps: horrors2.ps
	pstops -p letter "$(shell ./enbook $(SIGSIZE))" $< > $@

horrors2.ps: horrors2.pdf
	pdftops $<

horrors2.pdf: horrors2.ltx $(SUPPORT) $(STORIES) $(ART)
	pdflatex $<
	pdflatex $<

publish: horrors2.pdf
	cp horrors2.pdf horrors2.$(shell TZ=UTC date "+%Y-%m-%dT%H:%M:%SZ").pdf

clean:
	rm -f *aux *dvi *log
