#!/usr/bin/env python3

import collections
import json
import queue
import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

class Regolith(object):
  def __init__(self, min_x, max_x, min_y, max_y):
    self.x_offset = min_x - 1
    self.max_x = max_x - self.x_offset + 1
    self.max_y = max_y + 1
    self.board = list()
    for y in range(self.max_y + 1):
      self.board.append(['.'] * (self.max_x+1))

  def show(self):
    for row in self.board:
      print(''.join(row))

  def sand(self):
    x = 500-self.x_offset
    y = 0
    assert self.board[y][x] == '.'
    while True:
      if y >= max_y:
        return False
      if self.board[y+1][x] == '.':
        y += 1
        continue
      if self.board[y+1][x-1] == '.':
        y += 1
        x -= 1
        continue
      if self.board[y+1][x+1] == '.':
        y += 1
        x += 1
        continue
      self.board[y][x] = 'o'
      break
    return True

  def all_sand(self):
    count = 0
    while self.sand():
      count += 1
    return count

min_x = None
max_x = None
min_y = None
max_y = None
for line in lines:
  parts = line.split(' -> ')
  for part in parts:
    x, y = [int(item) for item in part.split(',')]
    if min_x is None or min_x > x:
      min_x = x
    if max_x is None or max_x < x:
      max_x = x
    if min_y is None or min_y > y:
      min_y = y
    if max_y is None or max_y < y:
      max_y = y

print((min_x, max_x, min_y, max_y))

r = Regolith(min_x, max_x, min_y, max_y)
print('---')
r.show()

for line in lines:
  parts = line.split(' -> ')
  last_x = None
  last_y = None
  for part in parts:
    x, y = [int(item) for item in part.split(',')]
    if last_x == x:
      for i in range(min(last_y, y), max(last_y, y) + 1):
        r.board[i][x-r.x_offset] = '#'
    if last_y == y:
      for i in range(min(last_x, x), max(last_x, x) + 1):
        r.board[y][i-r.x_offset] = '#'
    last_x = x
    last_y = y

print('---')
r.show()

count = r.all_sand()
print('---')
r.show()
print('---')
print(count)

