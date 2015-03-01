
set terminal pdfcairo rounded

if (!exists("DATADIR")) DATADIR='.'
set datafile separator ","

set key autotitle columnhead
#set key off

set logscale y
set grid x y
set xlabel "SNR [dB]"

set output DATADIR."/CER.pdf"
set ylabel "CER"
plot DATADIR."/snr.dat" using 1:4 with linespoints

set output DATADIR."/SER.pdf"
set ylabel "SER"
plot DATADIR."/snr.dat" using 1:7 with linespoints

set output DATADIR."/BER.pdf"
set ylabel "BER"
plot DATADIR."/snr.dat" using 1:10 with linespoints

#pause -1
