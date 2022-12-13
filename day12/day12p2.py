#!/usr/bin/env python3

import collections
import queue
import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

class Weights(object):
  def __init__(self, up, down, left, right):
    self.up = up
    self.down = down
    self.left = left
    self.right = right

class Grid(object):
  def __init__(self, lines):
    self.grid = list()
    for line in lines:
      self.grid.append(list(line.strip()))
    self.nrow = len(self.grid)
    self.ncol = len(self.grid[0])
    self.weights = list()
    for r in range(self.nrow):
      self.weights.append([None] * self.ncol)

    for r in range(self.nrow):
      for c in range(self.ncol):
        if self.grid[r][c] == 'S':
          self.grid[r][c] = 'a'
          self.start = (r, c)
        if self.grid[r][c] == 'E':
          self.grid[r][c] = 'z'
          self.end = (r, c)

  def connect(self):
    for r in range(self.nrow):
      for c in range(self.ncol):
        up = None
        down = None
        left = None
        right = None
        if (r-1 < self.nrow and r-1 >= 0 and
            ord(self.grid[r-1][c]) <= ord(self.grid[r][c])+1):
          up = 1
        if (r+1 < self.nrow and r+1 >= 0 and
            ord(self.grid[r+1][c]) <= ord(self.grid[r][c])+1):
          down = 1
        if (c-1 < self.ncol and c-1 >= 0 and
            ord(self.grid[r][c-1]) <= ord(self.grid[r][c])+1):
          left = 1
        if (c+1 < self.ncol and c+1 >= 0 and
            ord(self.grid[r][c+1]) <= ord(self.grid[r][c])+1):
          right = 1
        self.weights[r][c] = Weights(up, down, left, right)

  def bfs(self):
    self.min_weight = list()
    for r in range(self.nrow):
      self.min_weight.append([None] * self.ncol)

    q = queue.PriorityQueue()
    for r in range(self.nrow):
      for c in range(self.ncol):
        if self.grid[r][c] == 'a':
          q.put((0, (r, c)))
          self.min_weight[r][c] = 0

    while not q.empty():
      total_weight, loc = q.get()
      moves = self.weights[loc[0]][loc[1]]
      if moves.up is not None:
        new_loc = (loc[0]-1, loc[1])
        new_weight = total_weight + moves.up
        if (self.min_weight[new_loc[0]][new_loc[1]] is None or
            self.min_weight[new_loc[0]][new_loc[1]] > new_weight):
          self.min_weight[new_loc[0]][new_loc[1]] = new_weight
          q.put((new_weight, new_loc))
      if moves.down is not None:
        new_loc = (loc[0]+1, loc[1])
        new_weight = total_weight + moves.down
        if (self.min_weight[new_loc[0]][new_loc[1]] is None or
            self.min_weight[new_loc[0]][new_loc[1]] > new_weight):
          self.min_weight[new_loc[0]][new_loc[1]] = new_weight
          q.put((new_weight, new_loc))
      if moves.left is not None:
        new_loc = (loc[0], loc[1]-1)
        new_weight = total_weight + moves.left
        if (self.min_weight[new_loc[0]][new_loc[1]] is None or
            self.min_weight[new_loc[0]][new_loc[1]] > new_weight):
          self.min_weight[new_loc[0]][new_loc[1]] = new_weight
          q.put((new_weight, new_loc))
      if moves.right is not None:
        new_loc = (loc[0], loc[1]+1)
        new_weight = total_weight + moves.right
        if (self.min_weight[new_loc[0]][new_loc[1]] is None or
            self.min_weight[new_loc[0]][new_loc[1]] > new_weight):
          self.min_weight[new_loc[0]][new_loc[1]] = new_weight
          q.put((new_weight, new_loc))

g = Grid(lines)
g.connect()
g.bfs()

print(g.min_weight[g.end[0]][g.end[1]])

