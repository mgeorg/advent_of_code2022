#!/usr/bin/env python3

import collections
import copy
import json
import queue
import re
import sys

filename = 'input.txt'
if len(sys.argv) >= 2:
  filename = sys.argv[1]

with open(filename, 'r') as f:
  lines = f.read().splitlines()

def snafu_to_dec(snafu):
  place = 1
  num = 0
  for i, char in enumerate(reversed(snafu)):
    if char == '=':
      num -= 2 * place
    elif char == '-':
      num -= place
    else:
      num += int(char) * place
    place *= 5
  return num
  
def dec_to_snafu(dec):
  base5 = list()
  num = dec
  while num > 0:
    base5.append(num % 5)
    num = num // 5
  for i in range(len(base5)):
    if base5[i] > 2:
      if base5[i] == 3:
        base5[i] = '='
      elif base5[i] == 4:
        base5[i] = '-'
      elif base5[i] == 5:
        base5[i] = 0
      base5[i+1] += 1
  return ''.join([str(x) for x in reversed(base5)])

class Snafu(object):
  def __init__(self, dec, snafu):
    self.dec = dec
    self.snafu = snafu
    if self.dec is None:
      self.dec = snafu_to_dec(self.snafu)
    if self.snafu is None:
      self.snafu = dec_to_snafu(self.dec)

total = 0
for line in lines:
  dec = snafu_to_dec(line)
  print(dec)
  total += dec
print(total)
print(dec_to_snafu(total))
