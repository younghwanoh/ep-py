#!/usr/bin/python

import epic as ep

num = 10
color = ep.tGenGradient("#CBCA01", num)

a = []
for i in range(num):
    a.append(ep.Group(None, [0], [0.5], color=color.pop()))

BP = ep.BoxPlotter()
BP.draw(*a)
BP.saveToPdf("output.pdf")
