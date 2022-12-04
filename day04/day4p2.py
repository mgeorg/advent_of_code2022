#!/usr/bin/env python3

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

total = 0
for line in lines:
  p1, p2 = line.split(',')
  s1, e1 = [int(x) for x in p1.split('-')]
  s2, e2 = [int(x) for x in p2.split('-')]
  if s1 > e2 or s2 > e1:
    continue
  total += 1

print(total)
