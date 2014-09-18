#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Magnitude
# Generated: Wed Sep 17 21:48:58 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser

class magnitude(gr.top_block):

    def __init__(self, trace_filename="0", mag_filename="0", threshold=-42):
        gr.top_block.__init__(self, "Magnitude")

        ##################################################
        # Parameters
        ##################################################
        self.trace_filename = trace_filename
        self.mag_filename = mag_filename
        self.threshold = threshold

        ##################################################
        # Blocks
        ##################################################
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, trace_filename, False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, mag_filename, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(threshold, 900e-3, 1, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.analog_pwr_squelch_xx_0, 0))


# QT sink close method reimplementation

    def get_trace_filename(self):
        return self.trace_filename

    def set_trace_filename(self, trace_filename):
        self.trace_filename = trace_filename
        self.blocks_file_source_0.open(self.trace_filename, False)

    def get_mag_filename(self):
        return self.mag_filename

    def set_mag_filename(self, mag_filename):
        self.mag_filename = mag_filename
        self.blocks_file_sink_0.open(self.mag_filename)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.analog_pwr_squelch_xx_0.set_threshold(self.threshold)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--trace-filename", dest="trace_filename", type="string", default="0",
        help="Set trace_filename [default=%default]")
    parser.add_option("", "--mag-filename", dest="mag_filename", type="string", default="0",
        help="Set mag_filename [default=%default]")
    parser.add_option("", "--threshold", dest="threshold", type="intx", default=-42,
        help="Set threshold [default=%default]")
    (options, args) = parser.parse_args()
    tb = magnitude(trace_filename=options.trace_filename, mag_filename=options.mag_filename, threshold=options.threshold)
    tb.start()
    tb.wait()

