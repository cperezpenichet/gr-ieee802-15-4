#!/usr/bin/python

from glob import glob
from os import sep

import pure_pcapy

PCAP_DIR   = '/tmp'

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

SYMBOLS = (0xA0, 0x09, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF)

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

def compute_BER(pcap_file):
	n_pcap = pure_pcapy.open_offline(pcap_file)

	error_bits, total_bits = 0, 0
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

		for i in range(len(SYMBOLS)):
			H, L = CHIP_MAPPING[SYMBOLS[i]>>4], CHIP_MAPPING[SYMBOLS[i]&0x0F]
			tt = ''
			for j in range(8*(i+1)-1,8*i-1,  -1):
				tt += "{:02X}".format(n_payload[j])
				if j%4==0:
					tt += " "
			h, l = map(lambda x: int(x, 16),tt.split())
		
			error_bits += one_count((H^h)&0x7FFFFFFE)
			error_bits += one_count((L^l)&0x7FFFFFFE)
			total_bits -= 4
		#	print n_time, error_bits, total_bits, '{:032b}'.format((H^h)&0x7FFFFFFE), '{:032b}'.format((L^l)&0x7FFFFFFE)
		#print

		n_header, n_payload = n_pcap.next()

	return error_bits, total_bits, float(error_bits)/total_bits if total_bits > 0 else float('inf')

if __name__ == '__main__':
	for pcap in sorted(glob(sep.join((PCAP_DIR, '*_chips_[0-9][0-9].pcap')))):
		#pcap = "/tmp/sensor_chips_36.pcap"
		print "%s,%s" % (get_num(pcap), ','.join(map(str, compute_BER(pcap))))

