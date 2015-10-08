ep-py ver. 0.3
=====
Personal graph drawing library with high-level abstraction of python-matplotlib<br>

* Author information
  - Young H. Oh.
  - SungKyunKwan Univ, Suwon, Korea.<br>
  - Parallel Architecture and Parallel Language(PAPL) Lab<br>


* Dependent package: numpy, matplotlib
```
apt-get install python-numpy python-matplotlib
```

Mac may already have built-in python binary and matplotlib

* Library constitution
  1. Front-end Parser
  2. Middle-end specifier
  3. Back-end plotter

## ep.py::
Top(or test) module to draw graphs using ep.py APIs
User should denote specification of data layout and graph's layout.

* Supported graph type<br>
  1) Line (line-key, line-raw, line-flat)<br>
  2) Normalized line (line-norm)<br>
  3) Clustered Bar (bar-clustered, bar-key-clustered)<br>
  4) Normalized Clustered Bar (bar-norm-clustered, bar-key-clustered)<br>
  5) Clustered Clustered Bar (bar-key-cc)<br>
  6) Stacked Bar (bar-stacked, bar-clustacked)<br>
  7) Box (box-key, box-time, box-multi-time)<br>
  8) Clustered Box (jaws-all, jaws)<br>
  9) Pie (jaws-pie)<br>
  10) Multiple subplot (Not yet)<br>
  11) CDF (Not yet)<br>
  12) etc...<br>

ref. "jaws-\*" examples can be also tested with "draw.sh" styles

### Example usages

* ./examples.py -i \[input\] \[attributes ...\]<br>
  1) ./examples.py -i dat/line.dat -s line-key<br>
  2) ./examples.py -i dat/line-norm.dat -s line-norm<br>
  3) ./examples.py -i dat/bar-clustered.dat -s bar-clustered<br>
  4) ./examples.py -i dat/bar-clustered.dat -s bar-norm-clustered<br>
  5) ./examples.py -i dat/bar-key-cc.dat -s bar-key-cc<br>
  6-1) ./examples.py -si atax -s bar-stacked<br>
  6-2) ./examples.py -s bar-clustacked<br>
  7) ./examples.py -i dat/box.dat -s box-key<br>
  8) ./examples.py -i dat/box.dat -s box-time<br>
  9) ./examples.py -i dat/jaws/atax.share.log -s jaws-pie<br>

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
Users must modify this codes to adapt their customized data with helper methods as mentioned.

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
  - BoxPlotter
  - CBoxPlotter
  - BarPlotter
  - CBarPlotter
  - CCBarPlotter
  - SBarPlotter
  - PiePlotter
  - StackBarPlotter

## Prefix of GIT log messages
  - \*: Major version update
  - +: Method or functionality update
  - @: Bug and critical issues
  - none: Minor update
