ep-py ver. 0.1
=====
Personal graph drawing library with high-level abstraction of python-matplotlib<br>

* Author information
  - Young H. Oh.
  - SungKyunKwan Univ, Suwon, Korea.<br>
  - Parallel Architecture and Parallel Language(PAPL) Lab<br>


* Dependent package: numpy, matplotlib
For Ubuntu 12.04

```
apt-get install python-numpy python-matplotlib
```

Mac may already have built-in python binary and matplotlib

* Library construction
  1. Front-end Parser
  2. Middle-end specifier
  3. Back-end plotter

## ep.py::
Top(or test) module to draw graphs using ep.py APIs
User should denote specification of data layout and graph's layout.

* Supported graph type
  1. Clustered Bar (...ing)
  2. Clustered Bar (...ing)
  3. Box (...ing)
  4. Line (line-key, line-raw, line-flat)
  5. Line normalized (line-norm)
  6. Multiple subplot (Not yet)
  7. CDF (Not yet)
  8. etc...

### Example usages

* ./ep.py -i \[input\] \[attributes ...\]
  1. ./ep.py -i dat/bar.dat -s bar-flat
  2. ./ep.py -i dat/bar-norm.dat -s bar-norm
  3. ./ep.py -i dat/box.dat -s box-key
  4. ./ep.py -i dat/line.dat -s line-key
  5. ./ep.py -i dat/line-norm.dat -s line-norm

* Sub attributes
  - -f data format
  - -o output name
  - -t title
  - -xl xlabel
  - -yl ylabel
  - -lw figure width
  - -lh figure height

## parser.py
Front-end parser class module. <b>PatternParser</b> class parses data with row(\n:newline) and col(denoted key). The class receives raw text string as an input of the constructor.<br>
And then, ParseKeyWith and ParseWith methods parses data and special key respectively. Special key is used as a identifier when grouping correlated data with <b>tools.py</b>.

## tools.py
Some of data manipulation tools are defined in this file.
To draw graph, user must inform the program of specific information,
say, postion of xlabel, which row's data be used as legend, and so on.
This kind of meta data can be abstracted with <b>Group</b> class
in <b>tools.py</b>. Middle-end data specification process can be written by these tools.

## plotter.py
<b>Set of graph drawing class</b> with grouped meta data which mid-end specified already.
Because, program cannot know which of graph styles the programmer wants to draw,
all styles of classes must be defined case by case. Here are the list of classes.

  - LinePlotter
  - BoxPlotter (...ing)
  - BarPlotter (...ing)
  - ClusteredBarPlotter (...ing)
  - CCBarPlotter (Not yet)
  - MultiPlotter (Not yet)

## Prefix of GIT log messages
  - \*: Major version update
  - +: Method or functionality update
  - @: Bug and critical issues
  - none: Minor update
