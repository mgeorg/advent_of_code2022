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
  def __init__(self, me_loc, me_time, elph_loc, elph_time, opened, total):
    self.me_loc = me_loc
    self.me_time = me_time
    self.elph_loc = elph_loc
    self.elph_time = elph_time
    if self.me_loc > self.elph_loc or (self.me_loc == self.elph_loc and
                                       self.me_time > self.elph_time):
      self.me_loc, self.elph_loc = self.elph_loc, self.me_loc
      self.me_time, self.elph_time = self.elph_time, self.me_time
    self.opened = opened
    self.total = total

  def state(self):
    return (self.me_loc, self.me_time,
            self.elph_loc, self.elph_time,
            self.opened)

  def key(self):
    return (-self.total, self.me_time + self.elph_time)
    # return (-self.total, self.me_time, self.elph_time)

  def __lt__(self, other):
    return self.key() < other.key()

  def __cmp__(self, other):
    if self.key() < other.key():
      return -1
    if other.key() < other.key():
      return 1
    return 0

  def __repr__(self):
    return (f'Configuration({self.me_loc!r}, {self.me_time!r}, '
            f'{self.elph_loc!r}, {self.elph_time!r}, '
            f'{self.total!r}, {self.opened!r})')

valves = dict()
for line in lines:
  m = re.match(
      r'^Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)$', line)
  assert m, line
  v = Valve(m.group(1), int(m.group(2)), m.group(3).split(', '))
  valves[v.name] = v

valve_map = dict()
for unused, v in valves.items():
  q = queue.PriorityQueue()
  q.put((1, v.name))
  distances = {v.name: 0}
  dist = 1  # include the time to turn on the valve.
  while not q.empty():
    dist, name = q.get()
    for other in valves[name].connections:
      if other not in distances:
        distances[other] = dist+1
        q.put((dist+1, other))
  valve_map[v.name] = distances

# print(valve_map)

pruned_map = dict()
for name, mapping in valve_map.items():
  v = valves[name]
  if name != 'AA' and v.rate == 0:
    continue
  pruned = dict()
  distances = valve_map[v.name]
  for other, dist in distances.items():
    if other != v.name and valves[other].rate != 0:
      pruned[other] = dist
  pruned_map[v.name] = pruned
  
# print(pruned_map)

best_configurations = dict()
c = Configuration('AA', 26, 'AA', 26, (), 0)
best_configurations[c.state()] = c.total
q = queue.PriorityQueue()
q.put(c)

max_total = 0
i = 0

while not q.empty():
  c = q.get()
  if i % 100000 == 0:
    print(f'step {i} and queue has {q.qsize()+1} elements.')
    print(c)
  for other, dist in pruned_map[c.me_loc].items():
    if other not in c.opened and c.me_time > dist:
      new_opened = tuple(sorted(c.opened + tuple([other])))
      new = Configuration(other, c.me_time - dist,
                          c.elph_loc, c.elph_time,
                          new_opened,
                          c.total + (c.me_time - dist) * valves[other].rate)
      best = best_configurations.get(new.state())
      if best is None or best < new.total:
        best_configurations[new.state()] = new.total
        q.put(new)
        if new.total > max_total:
          max_total = new.total
          if max_total >= 2269:
            print(f'#' * 78)
            print(f'new max {max_total}')
            print(f'#' * 78)
  for other, dist in pruned_map[c.elph_loc].items():
    if other not in c.opened and c.elph_time > dist:
      new_opened = tuple(sorted(c.opened + tuple([other])))
      new = Configuration(c.me_loc, c.me_time,
                          other, c.elph_time - dist,
                          new_opened,
                          c.total + (c.elph_time - dist) * valves[other].rate)
      best = best_configurations.get(new.state())
      if best is None or best < new.total:
        best_configurations[new.state()] = new.total
        q.put(new)
        if new.total > max_total:
          max_total = new.total
          if max_total >= 2269:
            print(f'#' * 78)
            print(f'new max {max_total}')
            print(f'#' * 78)
  i += 1

# 2269 too low
# 2714 too high
print(max_total)


