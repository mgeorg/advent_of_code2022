#!/usr/bin/env python3

import re
import collections

u = 14

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

for line in lines:
  q = collections.deque()
  count = 0
  for c in line:
    count += 1
    q.append(c)
    if len(q) > u:
      q.popleft()
    if len(q) >= u and len(set(q)) == u:
      break
  print(count)
