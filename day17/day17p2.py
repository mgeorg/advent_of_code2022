#!/usr/bin/env python3

import collections
import json
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

pieces = [
    ['####'],
    ['.#.',
     '###',
     '.#.'],
    ['..#',
     '..#',
     '###'],
    ['#',
     '#',
     '#',
     '#'],
    ['##',
     '##'],
]

class Board(object):
  def __init__(self, pattern):
    self.pattern = pattern
    self.cur = 0
    self.board = ['#######']
    self.cur_piece_index = 0
    self.last_height = 0
    self.num_rocks = 0

  def can_move(self, piece, height, pos):
    cur_height = height
    for part in piece:
      if cur_height < len(self.board):
        for i, char in enumerate(part):
          if char == '#':
            if self.board[cur_height][pos + i] == '#':
              return False
      cur_height -= 1
    return True

  def add_to_board(self):
    for part_i in range(len(self.piece)-1, -1, -1):
      part = self.piece[part_i]
      if self.height - part_i < len(self.board):
        line = list(self.board[self.height - part_i])
        for i, char in enumerate(part):
          if char == '#':
            line[i + self.pos] = '#'
        self.board[self.height - part_i] = ''.join(line)
      else:
        line = ['.'] * 7
        for i, char in enumerate(part):
          if char == '#':
            line[i + self.pos] = '#'
        self.board.append(''.join(line))
    
  def drop(self):
    self.num_rocks += 1
    self.piece = pieces[self.cur_piece_index]
    self.cur_piece_index = (self.cur_piece_index + 1) % len(pieces)
    self.pos = 2
    self.height = 2 + len(self.piece) + len(self.board)
    while True:
      # gust
      gust = self.pattern[self.cur]
      self.cur = (self.cur + 1 ) % len(self.pattern)
      if self.cur == 0:
        print(self.num_rocks,
              self.cur_piece_index,
              len(self.board) - self.last_height)
        self.last_height = len(self.board)

      skip = False
      new_pos = None
      if gust == '<':
        if self.pos > 0:
          new_pos = self.pos - 1
      elif gust == '>':
        if self.pos + len(self.piece[0]) < 7:
          new_pos = self.pos + 1
      else:
        assert False, gust
      if new_pos is not None:
        if self.can_move(self.piece, self.height, new_pos):
          self.pos = new_pos
      # print(gust)
      # print(self)
      # drop
      if self.can_move(self.piece, self.height - 1, self.pos):
        self.height -= 1
      else:
        self.add_to_board()
        self.piece = None
        break
      # print('drop')
      # print(self)
    # print('final')
    # print(self)

  def __str__(self):
    output = list()
    top = max(self.height+1, len(self.board))
    bottom = max(self.height - 20, 0)
    for h in range(top-1, bottom-1, -1):
      if h >= len(self.board):
        line = ['.'] * 7
      else:
        line = list(self.board[h])
      piece_i = self.height - h
      if self.piece is not None and piece_i >= 0 and piece_i < len(self.piece):
        for i, char in enumerate(self.piece[piece_i]):
          if char == '#':
            line[self.pos + i] = '@'
      output.append(''.join(line))
    return '\n'.join(output)
    
  def __repr__(self):
    return str(self)
      


assert len(lines) == 1
b = Board(lines[0].strip())
for i in range(len(b.pattern) * 20):
  b.drop()

print('pattern length: ' + str(len(b.pattern)))

############
# For sample
############

rocks = 1000000000000
# rocks = 2022
initial_rocks = 9 + 35
rocks -= initial_rocks
period_height = 8 + 14 + 12 + 10 + 9
period_rocks = 35
# period = len(b.pattern) * 5

print(rocks)

b = Board(lines[0].strip())
for i in range(initial_rocks):
  b.drop()
for i in range(rocks % period_rocks):
  b.drop()
print(len(b.board)-1)
print(len(b.board) - 1 + period_height * (rocks // period_rocks))

############
# For input
############

rocks = 1000000000000
initial_rocks = 3441
rocks -= initial_rocks
period_height = 2620
period_rocks = 1710

print(rocks)

b = Board(lines[0].strip())
for i in range(initial_rocks):
  b.drop()
for i in range(rocks % period_rocks):
  b.drop()
print(len(b.board)-1)
print(len(b.board) - 1 + period_height * (rocks // period_rocks))




