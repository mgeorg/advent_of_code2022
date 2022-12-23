#!/usr/bin/env python3

import collections
import json
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

cubes = set()
for line in lines:
  x, y, z = [int(item) for item in line.split(',')]
  cubes.add((x,y,z))

total = 0
for x,y,z in cubes:
  sides = 6
  if (x-1, y, z) in cubes:
    sides -= 1
  if (x+1, y, z) in cubes:
    sides -= 1
  if (x, y-1, z) in cubes:
    sides -= 1
  if (x, y+1, z) in cubes:
    sides -= 1
  if (x, y, z-1) in cubes:
    sides -= 1
  if (x, y, z+1) in cubes:
    sides -= 1
  total += sides

print(total)

