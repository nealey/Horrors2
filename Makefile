PAGES = page*.tex

horrors2.dvi: horrors2.ltx $(PAGES)
	latex $<
	latex $<

horrors2.pdf: horrors2.ltx $(PAGES)
	pdflatex $<
	pdflatex $<
