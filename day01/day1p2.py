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

  def __str__(self):
    return str(self.total)

  def __repr__(self):
    return repr(self.total)

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

packs.sort(key=lambda x: -x.total)

print(packs)
print(packs[0:3])

print(packs[0].total + packs[1].total + packs[2].total)


