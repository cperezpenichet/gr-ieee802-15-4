#!/usr/bin/python

import pure_pcapy

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
#SYMBOLS = (0xA0, 0x06, 0x01, 0x23, 0x45, 0x67, 0x89, 0x00, 0xD5, 0xF6)

def dump_errors(pcap_file):
	n_pcap = pure_pcapy.open_offline(pcap_file)

	n_header, n_payload = n_pcap.next()
	if n_header == None:
		return 
	while n_header != None:
		if n_header.getlen()-3*8 != len(SYMBOLS)*8:
			n_header, n_payload = n_pcap.next()
			continue
		
		n_payload = bytearray(n_payload)
		for i in range(len(SYMBOLS)):
			H, L = CHIP_MAPPING[SYMBOLS[i]>>4], CHIP_MAPPING[SYMBOLS[i]&0x0F]
			t = "{:08X} {:08X} -> ".format(H, L)
			tt = ''
			for j in range(8*(i+1)-1,8*i-1,  -1):
				tt += "{:02X}".format(n_payload[j])
				if j%4==0:
					tt += " "
			t += tt
			h, l = map(lambda x: int(x, 16),tt.split())
			print i, t, "{:032b}".format(H^h), "{:032b}".format(L^l)
		print
		n_header, n_payload = n_pcap.next()

if __name__ == '__main__':
	pcap = "/home/claro/Downloads/exp9/ID3_Repeater/sensor_chips_25.pcap"
	dump_errors(pcap)

