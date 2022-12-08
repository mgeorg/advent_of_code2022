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

for i in range(num_row):
  height = -1
  for j in range(num_col):
    if height < grid[i][j].num:
      grid[i][j].visible = True
      height = max(height, grid[i][j].num)

for i in range(num_row):
  height = -1
  for j in range(num_col - 1, -1, -1):
    if height < grid[i][j].num:
      grid[i][j].visible = True
      height = max(height, grid[i][j].num)

for j in range(num_col):
  height = -1
  for i in range(num_row):
    if height < grid[i][j].num:
      grid[i][j].visible = True
      height = max(height, grid[i][j].num)

for j in range(num_col):
  height = -1
  for i in range(num_row-1, -1, -1):
    if height < grid[i][j].num:
      grid[i][j].visible = True
      height = max(height, grid[i][j].num)

count = 0
for i in range(num_row):
  print('')
  for j in range(num_col):
    if grid[i][j].visible:
      print('v', end='')
      count += 1
    else:
      print('x', end='')

# not 1052
print(count)

