#!/usr/bin/env python3

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

def type_to_priority(t):
  if t.islower():
    return ord(t) - ord('a') + 1
  return ord(t) - ord('A') + 27

iter_lines = iter(lines)
total = 0
try:
  while True:
    l1 = next(iter_lines)
    l2 = next(iter_lines)
    l3 = next(iter_lines)
    r = set(l1).intersection(set(l2)).intersection(set(l3))
    print(r)
    p = type_to_priority(sorted(r)[0])
    total += p
except StopIteration:
  print('done with lines')

print(total)
