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

class Blizzard(object):
  def __init__(self, board, row, col, direction):
    self.board = board
    self.row = row
    self.col = col
    self.dir = direction

  def move(self):
    if self.dir == '#':
      return
    if self.dir == '>':
      self.col += 1
      if self.col == self.board.num_cols-1:
        self.col = 1
      return
    if self.dir == '<':
      self.col -= 1
      if self.col == 0:
        self.col = self.board.num_cols-2
      return
    if self.dir == '^':
      self.row -= 1
      if self.row == 0:
        self.row = self.board.num_rows-2
      return
    if self.dir == 'v':
      self.row += 1
      if self.row == self.board.num_rows-1:
        self.row = 1
      return


class Possibility(object):
  def __init__(self, board, row, col):
    self.board = board
    self.row = row
    self.col = col

  def move(self):
    possib = [
        Possibility(self.board, self.row, self.col+1),  # Right
        Possibility(self.board, self.row+1, self.col),  # Down
        Possibility(self.board, self.row, self.col-1),  # Left
        Possibility(self.board, self.row-1, self.col),  # up
        self  # Stay here
    ]
    if self.row == 0:
      del possib[3]  # Don't go up
    remove = list()
    for b in self.board.blizzards:
      for i, p in enumerate(possib):
        if p.row == b.row and p.col == b.col:
          remove.append(i)
      if remove:
        new = list()
        for i in range(len(possib)):
          if i not in remove:
            new.append(possib[i])
        possib = new
        remove = list()
        if not possib:
          break
    return possib


class Board(object):
  def __init__(self, lines):
    self.board = list()
    self.blizzards = list()
    for row, line in enumerate(lines):
      for col, char in enumerate(line):
        if char == '.':
          continue
        self.blizzards.append(Blizzard(self, row, col, char))
    self.possib = {(0, 1): Possibility(self, 0, 1)}
    self.num_rows = len(lines)
    self.num_cols = len(lines[0])

  def progress(self):
    for b in self.blizzards:
      b.move()
    new_possib = dict()
    for p in self.possib.values():
      more = p.move()
      for m in more:
        new_possib[(m.row, m.col)] = m
    self.possib = new_possib
    if (self.num_rows-1, self.num_cols-2) in self.possib:
      return True
    return False

  def __str__(self):
    output = list()
    # print(f'self.num_rows = {self.num_rows}')
    # print(f'self.num_cols = {self.num_cols}')
    for row in range(self.num_rows):
      output.append(['.'] * self.num_cols)
    for b in self.blizzards:
      # print(b.row, b.col)
      if output[b.row][b.col] == '.':
        output[b.row][b.col] = b.dir
      elif output[b.row][b.col] in ['>', '<', '^', 'v']:
        output[b.row][b.col] = '2'
      else:
        output[b.row][b.col] = str(int(output[b.row][b.col])+1)
    for b in self.possib.values():
      assert output[b.row][b.col] == '.'
      output[b.row][b.col] = 'x'
    return '\n'.join([''.join(x) for x in output])

b = Board(lines)
print(f'{b}\n')
num_rounds = 0
done = False
while not done:
  done = b.progress()
  num_rounds += 1
  print(f'num_rounds = {num_rounds}')
  print(f'{b}\n')

print(f'num_rounds = {num_rounds}')

