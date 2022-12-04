#!/usr/bin/env python3

with open('input1.txt', 'r') as f:
  lines = f.read().splitlines()

class Pack(object):
  def __init__(self):
    self.packs = list()
    self.total = 0

  def add(self, val):
    self.packs.append(val)
    self.total += val

packs = [Pack()]

for line in lines:
  line = line.strip()
  if line == '':
    packs.append(Pack())
    continue
  val = int(line)
  packs[-1].add(val)

big = None

for pack in packs:
  if big is None or big.total < pack.total:
    big = pack

print(big.total)


