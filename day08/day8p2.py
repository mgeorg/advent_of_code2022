#!/usr/bin/env python3

import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

class tree(object):
  def __init__(self, num):
    self.num = num
    self.visible = False

grid = list()
for line in lines:
  grid.append(list())
  for c in line:
    grid[-1].append(tree(int(c)))

num_row = len(grid)
num_col = len(grid[0])

max_count = 0
for i in range(num_row):
  for j in range(num_col):
    height = grid[i][j].num
    count_up = 0
    count_down = 0
    count_left = 0
    count_right = 0
    for r in range(i-1, -1, -1):
      count_up += 1
      if grid[r][j].num >= height:
        break
    for r in range(i+1, num_row):
      count_down += 1
      if grid[r][j].num >= height:
        break
    for c in range(j-1, -1, -1):
      count_left += 1
      if grid[i][c].num >= height:
        break
    for c in range(j+1, num_col):
      count_right += 1
      if grid[i][c].num >= height:
        break
    cur_count = count_up*count_down*count_left*count_right
    if cur_count > max_count:
      max_count = cur_count
    print((i, j, count_up, count_down, count_left, count_right, cur_count))

print(max_count)


