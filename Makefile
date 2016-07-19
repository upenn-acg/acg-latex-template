# TODO: rename paper.tex to something meaningful
PAPER=paper

.PHONY: $(PAPER).pdf clean over

$(PAPER).pdf: $(PAPER).tex
	latexmk -pdf -pdflatex="pdflatex -file-line-error" $(PAPER).tex | tee .log
	-@grep -InE --color=always "LaTeX Warning:.*" .log
#	open $(PAPER).pdf

clean:
	latexmk -C $(PAPER.tex)

over:
	latexmk -gg $(PAPER.tex)
