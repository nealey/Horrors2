SUPPORT = chapauth.sty
STORIES = stories/*.tex
ART = art/*

horrors2.pdf: horrors2.ltx $(SUPPORT) $(STORIES) $(ART)
	pdflatex $<
	pdflatex $<

publish: horrors2.pdf
	cp horrors2.pdf horrors2.$(shell TZ=UTC date "+%Y-%m-%dT%H:%M:%SZ").pdf

clean:
	rm -f *aux *dvi *log
