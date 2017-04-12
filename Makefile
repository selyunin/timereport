TARGET := timereport
MAKE := Makefile

all:
	pdflatex $(TARGET).tex
	pdflatex $(TARGET).tex

nov_2014:
	pdflatex 2014_November.tex

dec_2014:
	pdflatex 2014_December.tex

jan_2015:
	pdflatex 2015_January.tex

feb_2015:
	pdflatex 2015_February.tex

mar_2015:
	pdflatex 2015_March.tex

apr_2015:
	pdflatex 2015_April.tex

may_2015:
	pdflatex 2015_May.tex

jun_2015:
	pdflatex 2015_June.tex

jul_2015:
	pdflatex 2015_July.tex

aug_2015:
	pdflatex 2015_August.tex

sep_2015:
	pdflatex 2015_September.tex

oct_2015:
	pdflatex 2015_October.tex

nov_2015:
	pdflatex 2015_November.tex

dec_2015:
	pdflatex 2015_December.tex

jan_2016:
	pdflatex 2016_January.tex

feb_2016:
	pdflatex 2016_February.tex

mar_2016:
	pdflatex 2016_March.tex

apr_2016:
	pdflatex 2016_April.tex

may_2016:
	pdflatex 2016_May.tex

jun_2016:
	pdflatex 2016_June.tex

jul_2016:
	pdflatex 2016_July.tex

aug_2016:
	pdflatex 2016_August.tex

sep_2016:
	pdflatex 2016_September.tex

oct_2016:
	pdflatex 2016_October.tex

nov_2016:
	pdflatex 2016_November.tex

dec_2016:
	pdflatex 2016_December.tex

jan_2017:
	pdflatex 2017_January.tex

feb_2017:
	pdflatex 2017_February.tex

mar_2017:
	pdflatex 2017_March.tex

apr_2017:
	pdflatex 2017_April.tex

may_2017:
	pdflatex 2017_May.tex

jun_2017:
	pdflatex 2017_June.tex

jul_2017:
	pdflatex 2017_July.tex

aug_2017:
	pdflatex 2017_August.tex

view:
	@evince $(TARGET).pdf &

.PHONY: clean cleanall
cleanall:
	@rm -f $(TARGET).log $(TARGET).aux $(TARGET).pdf $(TARGET).out $(TARGET).bbl $(TARGET).blg $(TARGET).toc

clean:
	@rm -f $(TARGET).log $(TARGET).aux $(TARGET).out $(TARGET).bbl $(TARGET).blg $(TARGET).toc $(TARGET).nav $(TARGET).snm 
	@rm -f *.log *.aux *.out 

cleanbackup:
	@rm -f $(TARGET).tex.backup $(TARGET).tex~ $(MAKE)~
	@rm -f .$(TARGET)*~ .$(MAKE)*~
