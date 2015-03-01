#!/bin/bash

#set -x

if test $# -lt 1
then
echo USAGE:
echo -e \\t$0 OUTPUT_DIR
exit 1
fi

SNR_VALUES=(1 2 3 4 5 6 8 10 12 14 16 20 25 30)

CONTRIB_DIR="."
PCAP_DIR=$1
echo $PCAP_DIR
mkdir --parents $PCAP_DIR

# Prepare the gnuradio top block so that it will stop after processing the trace
TOP_BLOCK=$(tempfile --directory $CONTRIB_DIR/../examples/)
head -n -2 $CONTRIB_DIR/../examples/transceiver_exp.py | \
	cat - tb_autostop_hack.py > $TOP_BLOCK

# Run the block once per SNR value
for SNR in ${SNR_VALUES[@]}; do
	echo "SNR: "$SNR
	python $TOP_BLOCK \
		--trace-filename=$PCAP_DIR/capture.data \
		--snr-db=$SNR \
		--output-dir=$PCAP_DIR \
	> /dev/null
done

# Finally process all generated PCAPs to create the SNR curve
python ber.py $PCAP_DIR > $PCAP_DIR/snr.dat

# Now generate plot
gnuplot -e "DATADIR='$PCAP_DIR'" snr_plot.gp

# Cleanup
rm -f $TOP_BLOCK
exit 0
