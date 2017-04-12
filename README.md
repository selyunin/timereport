TimeReport: Generate Timereport in LaTeX
============================================

### Description & Quick Start

Repository to generate a time report (TU Wien style) 
using `python` & `LaTeX`. Information about daily activities is stored
in the XML files in the corresponding XML folder. A small command line
interface is used to read/write XML files, parse them, calculate total &
absence hours, and finally generate a time report in a TeX format for a 
corresponding month:

1. `./edit_timereport.py` -- launch the python script

1. `create_month [1-12] [20**]` (e.g. `create_month 4 2017`) -- month description is stored in an XML file 
in `xml` folder, for each month before filling in you need to create it first;

2. `set_month [1-12] [20**]` (e.g. `set_month 4 2017`) -- set the month to edit;

3. `edit_day [1-31]` -- edit (or fill in) the specific *date* in the month XML entry;

4. `gen_latex` -- create a TeX file of the month that is currently set (i.e. in the command prompt)

5. `make feb_2017` -- invoke `pdflatex` to create PDF file (edit Makefile to add months/targets you need)

This project needs improvement. For suggestions/questions/comments please contact
[Konstantin Selyunin](http://selyunin.com/), selyunin [dot] k [dot] v [at] gmail [dot] com
