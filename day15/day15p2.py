#!/usr/bin/env python3

import collections
import json
import queue
import re

run_sample = False

if run_sample:
  range_limit = 20
  verbose = True
  filename = 'sample.txt'
else:
  range_limit = 4000000
  verbose = False
  filename = 'input.txt'
with open(filename, 'r') as f:
  lines = f.read().splitlines()

sensors = list()
beacons = list()
intercepts = list()
for line in lines:
  m = re.match('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
  assert m
  sensor = (int(m.group(1)), int(m.group(2)), None)
  beacon = (int(m.group(3)), int(m.group(4)))

  radius = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
  sensor = (sensor[0], sensor[1], radius)

  sensors.append(sensor)
  beacons.append(beacon)

def check_loc(x, y, sensor_index):
  if (x >= 0 and x <= range_limit and
      y >= 0 and y <= range_limit):
    found = False
    for j in range(sensor_index, len(sensors)):
      s2 = sensors[j]
      if abs(s2[0] - x) + abs(s2[1] - y) <= s2[2]:
        found = True
        break
    if found == False:
      print('Not covered!')
      print((x, y))
      print(x * range_limit + y)
      print('Not covered!')
      return None
    return j
  return 0

if run_sample:
  board = list()
  for y in range(range_limit+1):
    board.append(list())
    for x in range(range_limit+1):
      coverage = check_loc(x, y, 0)
      if coverage is not None:
        board[-1].append(chr(ord('a') + coverage))
      else:
        board[-1].append('.')
  print('\n'.join([''.join(b) for b in board]), end='\n\n')

for i in range(len(sensors)):
  print(f'checking perimeter of sensor {i}')
  s1 = sensors[i]
  print(s1)
  for span in range(-s1[2] - 1, s1[2] + 2):
    x = s1[0] + span
    y = s1[1] + s1[2] + 1 - abs(span)
    coverage = check_loc(x, y, 0)
    if run_sample:
      if (x >= 0 and x <= range_limit and
          y >= 0 and y <= range_limit):
        if board[y][x] == '.':
          board[y][x] = '?'
        else:
          board[y][x] = board[y][x].upper()
    y = s1[1] - (s1[2] + 1 - abs(span))
    coverage = check_loc(x, y, 0)
    if run_sample:
      if (x >= 0 and x <= range_limit and
          y >= 0 and y <= range_limit):
        if board[y][x] == '.':
          board[y][x] = '?'
        else:
          board[y][x] = board[y][x].upper()

if run_sample:
  print('\n'.join([''.join(b) for b in board]), end='\n\n')

