#!/usr/bin/env python3

import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

class processor(object):
  def __init__(self, instructions):
    self.x = 1
    self.cycle = 1
    self.instructions = instructions

  def execute(self):
    self.total = 0
    signal_cycle = [20, 60, 100, 140, 180, 220]
    for inst in self.instructions:
      if inst[0] == 'noop':
        self.cycle += 1
        if self.cycle in signal_cycle:
          self.total += self.cycle * self.x
        continue
      if inst[0] == 'addx':
        if self.cycle+1 in signal_cycle:
          self.total += (self.cycle+1) * self.x
        self.x += inst[1]
        self.cycle += 2
        if self.cycle in signal_cycle:
          self.total += self.cycle * self.x
        continue

instructions = list()
for line in lines:
  if line == 'noop':
    instructions.append(('noop', ))
    continue
  m = re.match(r'^addx (-?\d+)$', line)
  if m:
    instructions.append(('addx', int(m.group(1))))
    continue

p = processor(instructions)
p.execute()
print(p.total)

