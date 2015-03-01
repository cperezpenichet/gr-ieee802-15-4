#!/bin/bash

if test $# -lt 1
then
echo USAGE:
echo -e \\t$0 TRACE_FILE
exit 1
fi

if [ ! -f $1 ];
then
echo ERROR!
echo -e \\tTrace file not found!: $1
exit 1
fi

SNR_VALUES=(1 2 4 6 8 10 12 14 15)

CONTRIB_DIR="."
DATA_DIR=$(dirname $1)
FILE_NAME=$(basename $1)
PCAP_DIR=$DATA_DIR/$FILE_NAME.d
mkdir --parents $PCAP_DIR

# Prepare the gnuradio top block so that it will stop after processing the trace
TOP_BLOCK=$(tempfile --directory $CONTRIB_DIR/../examples/)
head -n -2 $CONTRIB_DIR/../examples/transceiver_exp.py | \
	cat - tb_autostop_hack.py > $TOP_BLOCK

# Run the block once per SNR value
for SNR in ${SNR_VALUES[@]}; do
	echo "SNR: "$SNR
	python $TOP_BLOCK \
		--trace-filename=$1 \
		--snr-db=$SNR \
		--output-dir=$PCAP_DIR \
	> /dev/null
done

# Finally process all generated PCAPs to create the SNR courve
python ber.py $PCAP_DIR > $PCAP_DIR/snr.dat

# Cleanup
rm -f $TOP_BLOCK
exit 0
