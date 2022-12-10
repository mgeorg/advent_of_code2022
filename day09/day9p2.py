#!/usr/bin/env python3

import re

with open('input.txt', 'r') as f:
# with open('sample2.txt', 'r') as f:
  lines = f.read().splitlines()

class board(object):
  def __init__(self):
    self.rope = [(0, 0) for x in range(10)]
    self.tail_visited = set([self.rope[-1]])

  def adjust_tail(self):
    for i in range(len(self.rope) - 1):
      # double diagonal
      if (self.rope[i][0] <= self.rope[i+1][0] - 2 and
          self.rope[i][1] <= self.rope[i+1][1] - 2):
        self.rope[i+1] = (self.rope[i][0] + 1, self.rope[i][1] + 1)
      elif (self.rope[i][0] <= self.rope[i+1][0] - 2 and
          self.rope[i][1] >= self.rope[i+1][1] + 2):
        self.rope[i+1] = (self.rope[i][0] + 1, self.rope[i][1] - 1)
      elif (self.rope[i][0] >= self.rope[i+1][0] + 2 and
          self.rope[i][1] <= self.rope[i+1][1] - 2):
        self.rope[i+1] = (self.rope[i][0] - 1, self.rope[i][1] + 1)
      elif (self.rope[i][0] >= self.rope[i+1][0] + 2 and
          self.rope[i][1] >= self.rope[i+1][1] + 2):
        self.rope[i+1] = (self.rope[i][0] - 1, self.rope[i][1] - 1)
      # Single motions
      elif self.rope[i][0] <= self.rope[i+1][0] - 2:
        self.rope[i+1] = (self.rope[i][0] + 1, self.rope[i][1])
      elif self.rope[i][0] >= self.rope[i+1][0] + 2:
        self.rope[i+1] = (self.rope[i][0] - 1, self.rope[i][1])
      elif self.rope[i][1] <= self.rope[i+1][1] - 2:
        self.rope[i+1] = (self.rope[i][0], self.rope[i][1] + 1)
      elif self.rope[i][1] >= self.rope[i+1][1] + 2:
        self.rope[i+1] = (self.rope[i][0], self.rope[i][1] - 1)
    if self.rope[-1] not in self.tail_visited:
      self.tail_visited.add(self.rope[-1])

  def move(self, offset, num):
    for i in range(num):
      self.rope[0] = (self.rope[0][0] + offset[0], self.rope[0][1] + offset[1])
      self.adjust_tail()
      # print('')
      # self.show()

  def show(self):
    min_x = min([x for x,y in sorted(self.tail_visited) + self.rope])
    max_x = max([x for x,y in sorted(self.tail_visited) + self.rope])
    min_y = min([y for x,y in sorted(self.tail_visited) + self.rope])
    max_y = max([y for x,y in sorted(self.tail_visited) + self.rope])
    for x in range(min_x, max_x+1):
      for y in range(min_y, max_y+1):
        if (x, y) in self.tail_visited:
          print('X', end='')
        elif (x, y) == self.rope[0]:
          print('H', end='')
        elif (x, y) == self.rope[1]:
          print('1', end='')
        elif (x, y) == self.rope[2]:
          print('2', end='')
        elif (x, y) == self.rope[3]:
          print('3', end='')
        elif (x, y) == self.rope[4]:
          print('4', end='')
        elif (x, y) == self.rope[5]:
          print('5', end='')
        elif (x, y) == self.rope[6]:
          print('6', end='')
        elif (x, y) == self.rope[7]:
          print('7', end='')
        elif (x, y) == self.rope[8]:
          print('8', end='')
        elif (x, y) == self.rope[9]:
          print('9', end='')
        else:
          print('.', end='')
      print('')

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


b.show()
print(sorted(b.tail_visited))

# 2736 too low
print(len(b.tail_visited))


