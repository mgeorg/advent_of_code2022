#!/usr/bin/env python3

import re
import collections

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

for line in lines:
  q = collections.deque()
  count = 0
  for c in line:
    count += 1
    q.append(c)
    if len(q) >= 5:
      q.popleft()
    if len(q) >= 4 and len(set(q)) == 4:
      break
  print(count)
