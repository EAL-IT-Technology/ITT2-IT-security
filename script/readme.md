topics table
==============

Input data
-------------

Input is csv files. One per subject.

It contains two columns, the first is the week number, and the second is the topic of the week


Output
-------------

A .tex file containing a table with the data combined


How to use
---------------

1. copy relevant files .csv files to `data`
2. run `python gen_text_table.py | tee topics.tex | pdflatex --jobname=topics`

    This creates `topics.pdf` and `topics.tex` (for later reference )

3. run `evince topics.pdf` so see the pdf
