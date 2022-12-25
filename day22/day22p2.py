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

sections = [
  [
    None,
    [None, None, (2, 0, 2), (3, 0, 1)],
    [(2, 1, 2), (1, 1, 1), None, (3, 0, 0)],
  ],
  [
    None,
    [(0, 2, 3), None, (2, 0, 3), None],
    None,
  ],
  [
    [None, None, (0, 1, 2), (1, 1, 1)],
    [(0, 2, 2), (3, 0, 1), None, None],
    None,
  ],
  [
    [(2, 1, 3), (0, 2, 0), (0, 1, 3), None],
    None,
    None,
  ],
]
if filename == 'input.txt':
  section_size = 50
if filename == 'sample4.txt':
  section_size = 5

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
      self.instructions = re.findall(r'(\d+|R|L|#)', line)
      assert ''.join(self.instructions) == line
      new_inst = list()
      for inst in self.instructions:
        if inst == '#':
          break
        new_inst.append(inst)
      self.instructions = new_inst
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

  def simple_board_val(self, pos):
    if pos[0] < 0 or pos[0] >= self.rows:
      return ' '
    if pos[1] < 0 or pos[1] >= self.cols:
      return ' '
    return self.board[pos[0]][pos[1]]

  def try_move(self, pos, facing):
    try_vals = [pos[0], pos[1], facing, None]
    if facing == 0:  # Right
      try_vals[1] += 1
    if facing == 2:  # Left
      try_vals[1] -= 1
    if facing == 1:  # Down
      try_vals[0] += 1
    if facing == 3:  # Up
      try_vals[0] -= 1
    try_vals[3] = self.simple_board_val(try_vals)
    if try_vals[3] != ' ':
      return try_vals
    # Back to previous values.
    try_vals[0] = pos[0]
    try_vals[1] = pos[1]
    # Find the section we're in.
    section_index = [
        try_vals[0] // section_size,
        try_vals[1] // section_size,
    ]
    section = sections[section_index[0]][section_index[1]][facing]
    print(section)
    assert section
    # Leaving from the...
    if facing == 0:  # Right
      from_left = try_vals[0] % section_size
    elif facing == 2:  # Left
      from_left = section_size - 1 - (try_vals[0] % section_size)
    elif facing == 1:  # Down
      from_left = section_size - 1 - (try_vals[1] % section_size)
    elif facing == 3:  # Up
      from_left = try_vals[1] % section_size
    # Find the new direction.
    facing = (facing + section[2]) % 4
    try_vals[2] = facing
    # Coming in from the
    if facing == 0:  # Right
      try_vals[0] = section[0] * section_size + from_left
      try_vals[1] = section[1] * section_size
    elif facing == 2:  # Left
      try_vals[0] = section[0] * section_size + section_size - 1 - from_left
      try_vals[1] = section[1] * section_size + section_size - 1
    elif facing == 1:  # Down
      try_vals[0] = section[0] * section_size
      try_vals[1] = section[1] * section_size + section_size - 1 - from_left
    elif facing == 3:  # Up
      try_vals[0] = section[0] * section_size + section_size - 1
      try_vals[1] = section[1] * section_size + from_left
    try_vals[3] = self.simple_board_val(try_vals)
    assert try_vals[3] != ' '
    return try_vals

  def follow(self):
    for inst in self.instructions:
      if inst == 'R':
        self.facing = (self.facing + 1) % 4
        print(f'now facing {self.facing}')
        continue
      if inst == 'L':
        self.facing = (self.facing + 3) % 4
        print(f'now facing {self.facing}')
        continue
      step = int(inst)
      for i in range(step):
        if self.simple_board_val(self.pos) in ['>', 'v', '<' '^']:
          self.board[self.pos[0]][self.pos[1]] = 'x'
        if self.simple_board_val(self.pos) == '.':
          if self.facing == 0:
            self.board[self.pos[0]][self.pos[1]] = '>'
          elif self.facing == 1:
            self.board[self.pos[0]][self.pos[1]] = 'v'
          elif self.facing == 2:
            self.board[self.pos[0]][self.pos[1]] = '<'
          elif self.facing == 3:
            self.board[self.pos[0]][self.pos[1]] = '^'
        new_pos = self.try_move(self.pos, self.facing)
        print(new_pos)
        if new_pos[3] == '#':
          break
        self.pos[0] = new_pos[0]
        self.pos[1] = new_pos[1]
        self.facing = new_pos[2]

  def key(self):
    return (self.pos[0]+1) * 1000 + (self.pos[1]+1) * 4 + self.facing

if filename == 'sample4.txt':
  for i in range(4):
    for j in range(3):
      section = sections[i][j]
      if not section:
        continue
      print((i, j))
      b = Board(lines)
      b.pos[0] = i * section_size + 1
      b.pos[1] = j * section_size + 1
      b.facing = 3
      b.instructions = ['3', 'L', '3', 'L', '5']
      b.follow()
      for line in b.board:
        print(''.join(line))
   
  for i in range(4):
    for j in range(3):
      section = sections[i][j]
      if not section:
        continue
      print((i, j))
      b = Board(lines)
      b.pos[0] = i * section_size + 3
      b.pos[1] = j * section_size + 3
      b.facing = 0
      b.instructions = ['3', 'R', '3', 'R', '5']
      b.follow()
      for line in b.board:
        print(''.join(line))

b = Board(lines)
# print(b.instructions)
# for line in b.board:
  # print(''.join(line))

b.follow()
for line in b.board:
  print(''.join(line))
print(b.key())


