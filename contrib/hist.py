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

import sys
import numpy

bin_width = 0.0001

if (len(sys.argv) != 3)
   print "please provide filenames data and hist\n"
   sys.exit(1)

file_data = sys.argv[1]
file_hist = sys.argv[2]
 

data_lines = numpy.fromfile(file_data, sep='\n')

print len(data_lines)
num_bins = int((data_lines.max() - data_lines.min())/bin_width)
print "\n"


hist, val = numpy.histogram(data_lines, num_bins)
a = zip(val.tolist(), hist.tolist()[:-1])
numpy.savetxt(file_hist, numpy.array(a), delimiter=',')


print "number of bins is " + str(num_bins) + "\n"
print "done!\n"

sys.exit(0)
