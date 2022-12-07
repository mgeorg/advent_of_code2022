#!/usr/bin/env python3

import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

class Directory(object):
  def __init__(self, parent, name):
    self.parent = parent
    self.name = name
    self.initialized = False
    self.files = []
    self.dirs = {}
    self.size = None

  def add_dir(self, d):
    self.initialized = True
    self.dirs[d.name] = d

  def add_file(self, size, f):
    self.initialized = True
    self.files.append((size, f))


base = Directory(None, '')
cur = None

i = 0
while i < len(lines):
  line = lines[i]
  m = re.match(r'^\$ cd (.*)$', line)
  if m:
    d = m.group(1)
    if d == '/':
      cur = base
    elif d == '..':
      cur = cur.parent
    else:
      cur = cur.dirs[d]
  elif line == '$ ls':
    while True:
      i += 1
      if i >= len(lines) or lines[i][0:2] == '$ ':
        i -= 1
        break
      m = re.match(r'^dir (.*)$', lines[i])
      if m:
        cur.add_dir(Directory(cur, m.group(1)))
      m = re.match(r'^(\d+) (.*)$', lines[i])
      if m:
        cur.add_file(int(m.group(1)), m.group(2))
        continue
  i += 1

grand_total = 0
delete_size = 6975962
target_size = None


def set_sizes(cur):
  global grand_total
  global delete_size
  global target_size
  total = 0
  assert cur.initialized
  for f in cur.files:
    total += f[0]
  for name, d in cur.dirs.items():
    total += set_sizes(d)
  print(f'{cur.name}: {total}')
  if total <= 100000:
    grand_total += total
  if total >= delete_size and (target_size is None or total < target_size):
    target_size = total
  return total

set_sizes(base)
print(grand_total)

print(target_size)

