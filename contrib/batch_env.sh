#!/bin/bash

#Copyright (C) 2015 Claro Noda <noda@complexperiments.net>
#                   Carlos Pérez Penichet <cperezpenichet@gmail.com>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


PCAP_DIR=$1

SQUELSH_THR=-42

dd if="$PCAP_DIR/capture.data" of="$PCAP_DIR/capture_hist.data" count=800000 bs=1k


CONTRIB_DIR="."
TOP_BLOCK=$CONTRIB_DIR/../examples/magnitude.py

python $TOP_BLOCK \
	--trace-filename=$PCAP_DIR/capture_hist.data \
	--mag-filename=$PCAP_DIR/envelope.dat \
	--threshold=$SQUELSH_THR \
> /dev/null

hexdump -v -e '1/4 "%10f "' -e '"\n"' $PCAP_DIR/envelope.dat > $PCAP_DIR/envelope.txt

# replace comma for dot
cat $PCAP_DIR/envelope.txt | sed s/,/\\./g > $PCAP_DIR/envelope_dot.txt

# downsample the file n times
awk 'NR % 10 == 0' $PCAP_DIR/envelope_dot.txt > $PCAP_DIR/envelope_s.dat

python hist.py $PCAP_DIR/envelope_s.dat $PCAP_DIR/signal_histogram.dat
