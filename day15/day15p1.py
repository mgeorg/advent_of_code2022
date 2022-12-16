#!/usr/bin/env python3

import collections
import json
import queue
import re

target = 2000000
# target = 10
verbose = False
with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
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

  extra = radius - abs(sensor[1] - target)
  if extra >= 0:
    target_intercept = (sensor[0] - extra, sensor[0] + extra + 1)
    intercepts.append(target_intercept)

print(sensors)
print(beacons)
print(intercepts)

min_intercept = min([x[0] for x in intercepts])
max_intercept = max([x[1] for x in intercepts])
print((min_intercept, max_intercept))
total = 0
for i in range(min_intercept, max_intercept):
  add = False
  for intercept in intercepts:
    if i >= intercept[0] and i < intercept[1]:
      add = True
      break
  if add:
    if (i, target) not in beacons:
      if verbose:
        print('#', end='')
      total += 1
    else:
      if verbose:
        print('B', end='')
  else:
    if verbose:
      print('.', end='')
print()

print(total)

