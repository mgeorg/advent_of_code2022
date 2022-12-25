#!/usr/bin/env python3

import collections
import copy
import json
import queue
import re
import sys

import minmax

filename = 'input.txt'
if len(sys.argv) >= 2:
  filename = sys.argv[1]

with open(filename, 'r') as f:
  lines = f.read().splitlines()

class Board(object):
  def __init__(self, lines):
    self.elves = dict()
    for row, line in enumerate(lines):
      for col, char in enumerate(line):
        if char == '#':
          self.elves[(row, col)] = -1
    self.order_index = 0
    self.order = [3, 1, 2, 0]

  def progress(self):
    order = [
        self.order[self.order_index],
        self.order[(self.order_index + 1) % 4],
        self.order[(self.order_index + 2) % 4],
        self.order[(self.order_index + 3) % 4],
    ]
    self.order_index = (self.order_index + 1) % 4
    moved = dict()
    failed = dict()
    for pos, elf in self.elves.items():
      nw = (pos[0]-1, pos[1]-1) not in self.elves
      nn = (pos[0]-1, pos[1]) not in self.elves
      ne = (pos[0]-1, pos[1]+1) not in self.elves
      ww = (pos[0], pos[1]-1) not in self.elves
      ee = (pos[0], pos[1]+1) not in self.elves
      sw = (pos[0]+1, pos[1]-1) not in self.elves
      ss = (pos[0]+1, pos[1]) not in self.elves
      se = (pos[0]+1, pos[1]+1) not in self.elves
      if nw and nn and ne and ww and ee and sw and ss and se:
        moved[pos] = True
        continue
      new_pos = None
      for d in order:
        if d == 0 and ne and ee and se:  # East
          new_pos = (pos[0], pos[1]+1)
          break
        if d == 2 and nw and ww and sw:  # West
          new_pos = (pos[0], pos[1]-1)
          break
        if d == 1 and sw and ss and se:  # South
          new_pos = (pos[0]+1, pos[1])
          break
        if d == 3 and nw and nn and ne:  # North
          new_pos = (pos[0]-1, pos[1])
          break
      if new_pos:
        if new_pos in failed:
          # Don't move ourself.
          moved[pos] = True
          continue
        if new_pos in moved:
          failed[new_pos] = True
          # Move the other value back.
          moved[moved[new_pos]] = True
          del moved[new_pos]
          # Don't move ourself.
          moved[pos] = True
          continue
        moved[new_pos] = pos
      else:
        moved[pos] = True
    self.elves = moved

  def __str__(self):
    output = list()
    min_row, max_row = minmax.minmax([x[0] for x in self.elves])
    min_col, max_col = minmax.minmax([x[1] for x in self.elves])
    for row in range(min_row, max_row+1):
      cur = list()
      for col in range(min_col, max_col+1):
        if (row, col) in self.elves:
          cur.append('#')
        else:
          cur.append('.')
      output.append(''.join(cur))
    return '\n'.join(output)

b = Board(lines)
print()
print(b)
for i in range(10):
  b.progress()
  print()
  print(b)

print(sum([x == '.' for x in str(b)]))

