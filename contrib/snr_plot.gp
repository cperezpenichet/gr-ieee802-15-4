
DATAFILE = "tst.dat"
set datafile separator ","

set key off
set logscale y
set grid x y

set xlabel "SNR [dB]"
set ylabel "BER"

plot "tst.dat" using 1:5 with linespoints

#
# Use this way of plotting for the old way of exporting the SNR values
#
#plot DATAFILE using (20*log10(30/$1)):5 with linespoints

