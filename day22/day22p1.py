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

class Board(object):
  def __init__(self, lines):
    self.board = list()
    for line in lines:
      m = re.match(r'[ \.#]+$', line)
      if m:
        self.board.append([x for x in line])
        continue
      if line.strip() == '':
        continue
      self.instructions = re.findall(r'(\d+|R|L)', line)
      assert ''.join(self.instructions) == line
    self.rows = len(self.board)
    self.cols = len(self.board[0])
    for line in self.board:
      if len(line) > self.cols:
        self.cols = len(line)
    print(f'num rows: {self.rows}')
    print(f'num cols: {self.cols}')
    for i in range(len(self.board)):
      self.board[i] = self.board[i] + [' ']*(self.cols - len(self.board[i]))
    self.pos = [0, 0]
    while self.board[self.pos[0]][self.pos[1]] == ' ':
      self.pos[1] += 1
    self.facing = 0  # right

  def board_val(self):
    if self.pos[0] < 0 or self.pos[0] >= self.rows:
      return ' '
    if self.pos[1] < 0 or self.pos[1] >= self.cols:
      return ' '
    return self.board[self.pos[0]][self.pos[1]]

  def loop(self):
    if self.facing == 0:  # Right
      while self.board_val() == ' ':
        self.pos[1] += 1
    if self.facing == 2:  # Left
      while self.board_val() == ' ':
        self.pos[1] -= 1
    if self.facing == 1:  # Down
      while self.board_val() == ' ':
        self.pos[0] += 1
    if self.facing == 3:  # Up
      while self.board_val() == ' ':
        self.pos[0] -= 1

  def move(self):
    if self.facing == 0:  # Right
      self.pos[1] += 1
      if self.board_val() == ' ':
        self.pos[1] = 0
        self.loop()
    if self.facing == 2:  # Left
      self.pos[1] -= 1
      if self.board_val() == ' ':
        self.pos[1] = self.cols-1
        self.loop()
    if self.facing == 1:  # Down
      self.pos[0] += 1
      if self.board_val() == ' ':
        self.pos[0] = 0
        self.loop()
    if self.facing == 3:  # Up
      self.pos[0] -= 1
      if self.board_val() == ' ':
        self.pos[0] = self.rows-1
        self.loop()

  def follow(self):
    for inst in self.instructions:
      if inst == 'R':
        self.facing = (self.facing + 1) % 4
        continue
      if inst == 'L':
        self.facing = (self.facing + 3) % 4
        continue
      step = int(inst)
      for i in range(step):
        cur = [self.pos[0], self.pos[1]]
        if self.board_val() in ['>', 'v', '<' '^']:
          self.board[self.pos[0]][self.pos[1]] = 'x'
        if self.board_val() == '.':
          if self.facing == 0:
            self.board[self.pos[0]][self.pos[1]] = '>'
          elif self.facing == 1:
            self.board[self.pos[0]][self.pos[1]] = 'v'
          elif self.facing == 2:
            self.board[self.pos[0]][self.pos[1]] = '<'
          elif self.facing == 3:
            self.board[self.pos[0]][self.pos[1]] = '^'
        self.move()
        if self.board_val() == '#':
          self.pos = cur
          break

  def key(self):
    return (self.pos[0]+1) * 1000 + (self.pos[1]+1) * 4 + self.facing

b = Board(lines)
print(b.instructions)
# for line in b.board:
  # print(''.join(line))

b.follow()
for line in b.board:
  print(''.join(line))
print(b.key())

# 95310 is too low.

