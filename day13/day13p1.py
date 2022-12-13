#!/usr/bin/env python3

import collections
import json
import queue
import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

pairs = list()

def comp(left, right):
  if isinstance(left, int) and isinstance(right, int):
    if left < right:
      return -1
    if left > right:
      return 1
    return None
  if isinstance(left, int):
    return comp([left], right)
  if isinstance(right, int):
    return comp(left, [right])

  # both are lists
  for i in range(max(len(left), len(right))):
    if i >= len(left):
      return -1
    if i >= len(right):
      return 1
    val = comp(left[i], right[i])
    if val is not None:
      return val

  # both lists are of same length with no differences.
  return None


iter_lines = iter(lines)
index = 1
total = 0
while True:
  line = next(iter_lines)
  left = json.loads(line)
  line = next(iter_lines)
  right = json.loads(line)
  val = comp(left, right)
  if val == -1:
    total += index
  index += 1
  try:
    line = next(iter_lines)
  except StopIteration:
    break

print(total)
