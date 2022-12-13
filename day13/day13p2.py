#!/usr/bin/env python3

import collections
import functools
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


packets = list()
for line in lines:
  if line.strip() != '':
    packets.append(json.loads(line))
packets.append([[2]])
packets.append([[6]])

packets.sort(key=functools.cmp_to_key(comp))
print('\n'.join([repr(x) for x in packets]))
total = 1
for i in range(len(packets)):
  if repr(packets[i]) == '[[2]]':
    total *= (i+1)
  if repr(packets[i]) == '[[6]]':
    total *= (i+1)

print(total)

