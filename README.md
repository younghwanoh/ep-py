ep-py
=====

Personal graph drawing library with python-matplotlib ver. 0.1
SungKyunKwan Univ. Parallel Architecture and Parallel Language(PAPL) Lab

------------------------------------------------------------------------------------------------------

* Dependent package: numpy, matplotlib
For Ubuntu 12.04

```
apt-get install python-numpy python-matplotlib
```

Mac may already have built-in python binary and matplotlib


## graph.py::

  1. Clustered Bar (type1 - table. Please refer example bar.dat)
  2. Clustered Bar (type2 - parseKey with normalized index. Please refer example bar-norm.dat)
  3. Box (ybegin, yend)
  4. Line (x, y)
  5. Line normalized (parseKey with normalized index. Please refer example line-norm.dat)

### Example usages

./graph.py \[input\] \[attributes ...\]
  1. ./graph.py bar.dat -f bar
  2. ./graph.py bar-norm.dat -f bar-norm
  3. ./graph.py box.dat -f box
  4. ./graph.py line.dat -f line
  5. ./graph.py line-norm.dat -f line-norm

sub attribute
-f data format
-o output name
-t title
-xl xlabel
-yl ylabel
-lw figure width
-lh figure height

## multiplot.py::

You have manually specify which type of graphs you want to draw
this python script provides the basic pattern of multiple subplots
Data format is similar to GNUplot by default, which plots each column.

e.g.
<pre>
d1   d2   d3   d4
1    2.4  3    4.1
5.3  2.5  1.2  0.9
</pre>

to

<pre>
plot1: (0, 1),   (1, 5.3)
plot2: (0, 2.4), (1, 2.5) + (0, 3), (1, 1.2) -- two axis on subplot2
plot3: (0, 4,1), (1, 0.9)
</pre>


### Example usages

./multiplot.py \[input1,input2,...\] \[attributes ...\]

  1. ./multiplot.py opt.dat -f subplot -o out.pdf

sub attribute
-f data format
-o output name
