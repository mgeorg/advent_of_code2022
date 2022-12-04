#!/usr/bin/env python3

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

total = 0
for line in lines:
  p1, p2 = line.split(',')
  s1, e1 = [int(x) for x in p1.split('-')]
  s2, e2 = [int(x) for x in p2.split('-')]
  if s1 <= s2 and e1 >= e2:
    print(line)
    total += 1
    continue
  if s2 <= s1 and e2 >= e1:
    print(line)
    total += 1
    continue

# 575 too high
print(total)
