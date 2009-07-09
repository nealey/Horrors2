PAGES = part*.tex

horrors2.dvi: horrors2.ltx $(PAGES)
	latex $<
	latex $<

horrors2.pdf: horrors2.ltx $(PAGES)
	pdflatex $<
	pdflatex $<

publish: horrors2.pdf
	cp horrors2.pdf horrors2.$(shell TZ=UTC date "+%Y-%m-%dT%H:%M:%SZ").pdf

clean:
	rm -f *aux *dvi *log
