#!/usr/bin/python

from glob import glob
from os import sep

import pure_pcapy

PCAP_DIR   = '/tmp'
BASE_PCAP  = PCAP_DIR + '/sensor_chips_01.pcap'

TIME_EPS   = 1e-2

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
	b_pcap = pure_pcapy.open_offline(BASE_PCAP)

	error_bits, total_bits = 0, 0
	n_header, n_payload = n_pcap.next()
	b_header, b_payload = b_pcap.next()
	if n_header == None:
		return float("inf"), 0, float("inf")
	n_start, b_start = get_time(n_header), get_time(b_header)
	while n_header != None:
		n_time = get_time(n_header, n_start)
		
		while True:
			b_time = get_time(b_header, b_start)
			if b_header == None or \
			   b_time-n_time > TIME_EPS or \
			   (abs(n_time-b_time) <= TIME_EPS and \
				b_header.getlen() == n_header.getlen()\
			   ):
				break
			b_header, b_payload = b_pcap.next()
		if b_header == None or (abs(n_time - b_time) > TIME_EPS):
			n_header, n_payload = n_pcap.next()
			continue
		
		n_payload = bytearray(n_payload)
		b_payload = bytearray(b_payload)

		total_bits += 8 * len(n_payload)
		for i in range(len(n_payload)):
			error_bits += one_count(n_payload[i]^b_payload[i])

		#print b_time, n_time, error_bits
		n_header, n_payload = n_pcap.next()

	return error_bits, total_bits, float(error_bits)/total_bits

if __name__ == '__main__':
	for pcap in sorted(glob(sep.join((PCAP_DIR, '*_chips_[0-9][0-9].pcap')))):
		print "%s,%s" % (get_num(pcap), ','.join(map(str, compute_BER(pcap))))

