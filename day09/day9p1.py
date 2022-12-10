#!/usr/bin/env python3

import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

class board(object):
  def __init__(self):
    self.head = (0, 0)
    self.tail = (0, 0)
    self.tail_visited = set([(0,0)])

  def adjust_tail(self):
    if self.head[0] <= self.tail[0] - 2:
      self.tail = (self.head[0] + 1, self.head[1])
    elif self.head[0] >= self.tail[0] + 2:
      self.tail = (self.head[0] - 1, self.head[1])
    elif self.head[1] <= self.tail[1] - 2:
      self.tail = (self.head[0], self.head[1] + 1)
    elif self.head[1] >= self.tail[1] + 2:
      self.tail = (self.head[0], self.head[1] - 1)
    if self.tail not in self.tail_visited:
      self.tail_visited.add(self.tail)

  def move(self, offset, num):
    for i in range(num):
      self.head = (self.head[0] + offset[0], self.head[1] + offset[1])
      self.adjust_tail()

b = board()

for line in lines:
  d, num = line.split(' ')
  num = int(num)
  if d == 'L':
    b.move((0, -1), num)
  elif d == 'R':
    b.move((0, +1), num)
  elif d == 'U':
    b.move((-1, 0), num)
  elif d == 'D':
    b.move((+1, 0), num)

print(sorted(b.tail_visited))
print(len(b.tail_visited))

