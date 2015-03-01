#!/usr/bin/python

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


from glob import glob
from os import sep
import sys

import pure_pcapy

PCAP_DIR   = '/tmp'

DSSS_THRESHOLD = 6

CHIP_MAPPING = [
        1618456172,
        1309113062,
        1826650030,
        1724778362,
        778887287,
        2061946375,
        2007919840,
        125494990,
        529027475,
        838370585,
        320833617,
        422705285,
        1368596360,
        85537272,
        139563807,
        2021988657]

# Exp 7, 8, 17, 18, 20, 21
#SYMBOLS = (0xA0, 0x11, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF)

# Exp6, 12-16, 22
SYMBOLS = (0xA0, 0x09, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF)

#SYMBOLS = (0xA0, 0x00, 0x0A, 0x00, 0x00)

def get_time(header, start_time=0):
	t = header.getts()
	return t[0] + t[1]*1e-6 - start_time

def one_count(n):
	cnt = 0
	while n > 0:
		cnt += 1
		n &= (n-1)
	return cnt

def get_num(x):
    return ''.join(ele for ele in x if ele.isdigit())

def compute_chip_stats(pcap_file):
	n_pcap = pure_pcapy.open_offline(pcap_file)

	error_bits, total_bits = 0, 0
	error_symbols, total_symbols = 0, 0
	n_header, n_payload = n_pcap.next()
	if n_header == None:
		return float("inf"), 0, float("inf")
	n_start = get_time(n_header)
	while n_header != None:
		if n_header.getlen()-3*8 != len(SYMBOLS)*8:
			n_header, n_payload = n_pcap.next()
			continue
		
		n_time = get_time(n_header, n_start)
		n_payload = bytearray(n_payload)

		total_bits += 8 * (len(n_payload)-3*8)
		total_symbols += (len(n_payload)-3*8)/4

		for i in range(len(SYMBOLS)):
			H, L = CHIP_MAPPING[SYMBOLS[i]>>4], CHIP_MAPPING[SYMBOLS[i]&0x0F]
			tt = ''
			for j in range(8*(i+1)-1,8*i-1,  -1):
				tt += "{:02X}".format(n_payload[j])
				if j%4==0:
					tt += " "
			h, l = map(lambda x: int(x, 16),tt.split())

			bad_bits = one_count((H^h)&0x7FFFFFFE)
			error_bits += bad_bits
			error_symbols += 1 if bad_bits > DSSS_THRESHOLD else 0
			bad_bits = one_count((L^l)&0x7FFFFFFE)
			error_bits += bad_bits
			error_symbols += 1 if bad_bits > DSSS_THRESHOLD else 0
			total_bits -= 4
		#	print n_time, error_bits, total_bits, '{:032b}'.format((H^h)&0x7FFFFFFE), '{:032b}'.format((L^l)&0x7FFFFFFE)
		#print

		n_header, n_payload = n_pcap.next()

	return (error_bits, total_bits, 
	       float(error_bits)/total_bits if total_bits > 0 else float('inf'),
	       error_symbols, total_symbols,
	       float(error_symbols)/total_symbols if total_symbols > 0 else float('inf'))

def compute_byte_stats(pcap_file):
	n_pcap = pure_pcapy.open_offline(pcap_file)

	error_bits, total_bits = 0, 0
	n_header, n_payload = n_pcap.next()
	if n_header == None:
		return float("inf"), 0, float("inf")
	n_start = get_time(n_header)
	while n_header != None:
		if n_header.getlen()-3 != len(SYMBOLS):
			n_header, n_payload = n_pcap.next()
			continue
		
		n_time = get_time(n_header, n_start)
		n_payload = bytearray(n_payload)

		total_bits += 8 * (len(n_payload)-3)

		for i in range(len(SYMBOLS)):
			bad_bits = one_count(SYMBOLS[i]^n_payload[i])
			error_bits += bad_bits

		n_header, n_payload = n_pcap.next()

	return (error_bits, total_bits, 
	       float(error_bits)/total_bits if total_bits > 0 else float('inf'))

if __name__ == '__main__':
	if len(sys.argv) > 0:
		PCAP_DIR = sys.argv[1]
	print "SNR,Chip errors,Total chips,CER,Symbol errors,Total symbols,SER,Bit errors,Total bits,BER"
	for pcap in sorted(glob(sep.join((PCAP_DIR, '*_chips_[0-9][0-9].pcap')))):
		#pcap = "/tmp/sensor_chips_36.pcap"
		snr = int(get_num(pcap.split(sep)[-1]))
		a = sep.join((PCAP_DIR, "sensor_%02d.pcap")) % (snr,)
		b = sep.join((PCAP_DIR, "sensor_chips_%02d.pcap")) % (snr,)
		print "%s,%s,%s" % (snr,
				','.join(map(str, compute_chip_stats(b))),
				','.join(map(str, compute_byte_stats(a))),
				)

