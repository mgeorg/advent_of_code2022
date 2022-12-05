#!/usr/bin/env python3

import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

stacks = None
iter_lines = iter(lines)
for line in iter_lines:
  if stacks is None:
    stacks = [list() for i in range((len(line)+1) // 4)]
  if line == '':
    break
  for i in range((len(line)+1)//4):
    c = line[i*4 + 1]
    if c == ' ' or (ord(c) >= ord('0') and ord(c) <= ord('9')):
      continue
    stacks[i].insert(0, line[i*4 + 1])

for line in iter_lines:
  m = re.match(r'move (\d+) from (\d+) to (\d+)$', line)
  assert m
  num = int(m.group(1))
  source = int(m.group(2)) - 1
  dest = int(m.group(3)) - 1
  for i in range(num):
    stacks[dest].append(stacks[source].pop())

print(stacks)

print(''.join([x[-1] for x in stacks]))
