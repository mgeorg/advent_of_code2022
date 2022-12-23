#!/usr/bin/env python3

import collections
import json
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class Cube(object):
  def __init__(self, x, y, z):
    self.pos = (x, y, z)
    

cubes = set()
for line in lines:
  x, y, z = [int(item) for item in line.split(',')]
  cubes.add((x,y,z))

max_x = max([item[0] for item in cubes])
max_y = max([item[1] for item in cubes])
max_z = max([item[2] for item in cubes])

print('initializing grid')
grid = dict()
for x in range(-1, max_x+2):
  for y in range(-1, max_y+2):
    for z in range(-1, max_z+2):
      if x == -1 or x == max_x+1:
        grid[(x,y,z)] = True
      elif y == -1 or y == max_y+1:
        grid[(x,y,z)] = True
      elif z == -1 or z == max_z+1:
        grid[(x,y,z)] = True
      else:
        grid[(x,y,z)] = False

change = 1
while change > 0:
  change = 0
  for x in range(max_x+1):
    for y in range(max_y+1):
      for z in range(max_z+1):
        if not grid[(x,y,z)] and (x,y,z) not in cubes and grid[(x,y,z-1)]:
          change += 1
          grid[(x,y,z)] = True
      for z in range(max_z, -1, -1):
        if not grid[(x,y,z)] and (x,y,z) not in cubes and grid[(x,y,z+1)]:
          change += 1
          grid[(x,y,z)] = True
  for x in range(max_x+1):
    for z in range(max_z+1):
      for y in range(max_y+1):
        if not grid[(x,y,z)] and (x,y,z) not in cubes and grid[(x,y-1,z)]:
          change += 1
          grid[(x,y,z)] = True
      for y in range(max_y, -1, -1):
        if not grid[(x,y,z)] and (x,y,z) not in cubes and grid[(x,y+1,z)]:
          change += 1
          grid[(x,y,z)] = True
  for y in range(max_y+1):
    for z in range(max_z+1):
      for x in range(max_x+1):
        if not grid[(x,y,z)] and (x,y,z) not in cubes and grid[(x-1,y,z)]:
          change += 1
          grid[(x,y,z)] = True
      for x in range(max_x, -1, -1):
        if not grid[(x,y,z)] and (x,y,z) not in cubes and grid[(x+1,y,z)]:
          change += 1
          grid[(x,y,z)] = True
  print(f'iteration completed reached {change} grid points.')

total = 0
for x,y,z in cubes:
  sides = 0
  if grid[(x-1, y, z)]:
    sides += 1
  if grid[(x+1, y, z)]:
    sides += 1
  if grid[(x, y-1, z)]:
    sides += 1
  if grid[(x, y+1, z)]:
    sides += 1
  if grid[(x, y, z-1)]:
    sides += 1
  if grid[(x, y, z+1)]:
    sides += 1
  total += sides

print(total)

