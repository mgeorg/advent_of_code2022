#!/usr/bin/env python3

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

def type_to_priority(t):
  if t.islower():
    return ord(t) - ord('a') + 1
  return ord(t) - ord('A') + 27

total = 0
for line in lines:
  p1 = line[:len(line)//2]
  p2 = line[len(line)//2:]
  s1 = set(p1)
  s2 = set(p2)
  for t in s1:
    if t in s2:
      same = t
      break
  print(t)
  p = type_to_priority(t)
  total += p

print(total)
