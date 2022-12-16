#!/usr/bin/env python3

import collections
import json
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class Valve(object):
  def __init__(self, name, rate, connections):
    self.name = name
    self.rate = rate
    self.connections = connections

class Configuration(object):
  def __init__(self, current, total, opened, time_remaining):
    self.current = current
    self.total = total
    self.opened = opened
    self.time_remaining = time_remaining

  def key(self):
    return (self.time_remaining, -self.total, self.current)

  def __lt__(self, other):
    return self.key() < other.key()

  def __cmp__(self, other):
    if self.key() < other.key():
      return -1
    if other.key() < other.key():
      return 1
    return 0

  def __repr__(self):
    return (f'Configuration({self.current!r}, {self.total!r}, '
            f'{self.opened!r}, {self.time_remaining!r})')

valves = dict()
for line in lines:
  m = re.match(
      r'^Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)$', line)
  assert m, line
  v = Valve(m.group(1), int(m.group(2)), m.group(3).split(', '))
  valves[v.name] = v

best_configurations = dict()
c = Configuration('AA', 0, (), 30)
best_configurations[('AA', ())] = [c]
q = queue.PriorityQueue()
q.put(c)

def is_candidate(new):
  best = best_configurations.get((new.current, new.opened))
  if best is not None:
    for b in best:
      if b.total >= new.total and b.time_remaining >= new.time_remaining:
        return False
    new_best = list()
    for b in best:
      if new.total >= b.total and new.time_remaining >= b.time_remaining:
        pass
      else:
        new_best.append(b)
    new_best.append(new)
    best_configurations[(new.current, new.opened)] = new_best
    # print(new_best)
  else:
    best_configurations[(new.current, new.opened)] = [new]
  return True

max_total = 0
while not q.empty():
  c = q.get()
  v = valves[c.current]
  if c.time_remaining > 1 and v.rate > 0 and c.current not in c.opened:
    new = Configuration(
        c.current,
        c.total + v.rate * (c.time_remaining-1),
        tuple(sorted(c.opened + tuple([c.current]))),
        c.time_remaining-1)
    if is_candidate(new):
      q.put(new)
      if max_total < new.total:
        max_total = new.total
  if c.time_remaining > 2:
    for other_name in v.connections:
      new = Configuration(other_name, c.total, c.opened, c.time_remaining-1)
      if is_candidate(new):
        q.put(new)
        if max_total < new.total:
          max_total = new.total

print(best_configurations)
# 1827 is too low
print(max_total)


