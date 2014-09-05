# Timeline plot
# ./ep.py -s jaws-all -i dat/jaws/atax.share.log -o atax.share.all.pdf
# ./ep.py -s jaws-all -i dat/jaws/syrk.share.log -o syrk.share.all.pdf
# ./ep.py -s jaws-all -i dat/jaws/gemm.share.log -o gemm.share.all.pdf
#
# ./ep.py -s jaws-all -i dat/jaws/atax.noshare.log -o atax.noshare.all.pdf
# ./ep.py -s jaws-all -i dat/jaws/syrk.noshare.log -o syrk.noshare.all.pdf
# ./ep.py -s jaws-all -i dat/jaws/gemm.noshare.log -o gemm.noshare.all.pdf

# Pie plot
# ./ep.py -s jaws-pie -i dat/jaws/atax.share.log -o atax.share.pie.pdf
# ./ep.py -s jaws-pie -i dat/jaws/syrk.share.log -o syrk.share.pie.pdf
# ./ep.py -s jaws-pie -i dat/jaws/gemm.share.log -o gemm.share.pie.pdf
#
# ./ep.py -s jaws-pie -i dat/jaws/atax.noshare.log -o atax.noshare.pie.pdf
# ./ep.py -s jaws-pie -i dat/jaws/syrk.noshare.log -o syrk.noshare.pie.pdf
# ./ep.py -s jaws-pie -i dat/jaws/gemm.noshare.log -o gemm.noshare.pie.pdf

# Stacked Bar plot
./ep.py -s bar-stacked -si atax -o atax.bar.pdf
./ep.py -s bar-stacked -si syrk -o syrk.bar.pdf
./ep.py -s bar-stacked -si gemm -o gemm.bar.pdf

# convert atax.bar.pdf atax.png
# convert syrk.bar.pdf syrk.png
# convert gemm.bar.pdf gemm.png
