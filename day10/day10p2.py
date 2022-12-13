#!/usr/bin/env python3

import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

class crt(object):
  def __init__(self, instructions):
    self.x = 1
    self.instructions = instructions
    self.screen = [' '] * 240

  def execute(self):
    inst_index = 0
    inst_cycle_count = 0

    for cycle in range(240):
      sprite = ['.'] * 40
      if self.x >= 0 and self.x < 40:
        sprite[self.x] = '#'
      if self.x-1 >= 0 and self.x-1 < 40:
        sprite[self.x-1] = '#'
      if self.x+1 >= 0 and self.x+1 < 40:
        sprite[self.x+1] = '#'
      self.screen[cycle] = sprite[cycle % 40]

      inst = self.instructions[inst_index]
      inst_cycle_count += 1
      if inst[0] == 'noop':
        inst_index += 1
        inst_cycle_count = 0
      if inst[0] == 'addx':
        if inst_cycle_count == 2:
          self.x += inst[1]
          inst_index += 1
          inst_cycle_count = 0

  def show(self):
    sprite = ['.'] * 40
    sprite[self.x] = '#'
    if self.x-1 >= 0:
      sprite[self.x-1] = '#'
    if self.x+1 < 40:
      sprite[self.x+1] = '#'
    print(''.join(sprite))
    print()
    print(''.join(self.screen[0:40]))
    print(''.join(self.screen[40:80]))
    print(''.join(self.screen[80:120]))
    print(''.join(self.screen[120:160]))
    print(''.join(self.screen[160:200]))
    print(''.join(self.screen[200:240]))

instructions = list()
for line in lines:
  if line == 'noop':
    instructions.append(('noop', ))
    continue
  m = re.match(r'^addx (-?\d+)$', line)
  if m:
    instructions.append(('addx', int(m.group(1))))
    continue

p = crt(instructions)
p.execute()
p.show()

