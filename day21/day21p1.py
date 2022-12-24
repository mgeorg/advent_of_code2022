#!/usr/bin/env python3

import collections
import copy
import json
import queue
import re
import sys

filename = 'input.txt'
if len(sys.argv) >= 2:
  filename = sys.argv[1]

with open(filename, 'r') as f:
  lines = f.read().splitlines()

class System(object):
  def __init__(self):
    self.monkeys

class Monkey(object):
  def __init__(self, line):
    m = re.match('^(.{4}): (\d+)$', line)
    if m:
      self.id = m.group(1)
      self.num = int(m.group(2))
      return
    m = re.match('^(.{4}): (.{4}) ([/*+\-]) (.{4})$', line)
    assert m
    self.id = m.group(1)
    self.num = None
    self.left = m.group(2)
    self.op = m.group(3)
    self.right = m.group(4)

  def compute(self, monkeys):
    if self.num is None:
      l = monkeys[self.left].num
      r = monkeys[self.right].num
      if l is not None and r is not None:
        if self.op == '/':
          self.num = l / r
        elif self.op == '*':
          self.num = l * r
        elif self.op == '+':
          self.num = l + r
        elif self.op == '-':
          self.num = l - r
        else:
          raise ValueError(f'{self.op} not understood.')

monkeys = dict()
for line in lines:
  monkey = Monkey(line)
  monkeys[monkey.id] = monkey

root_value = None
while root_value is None:
  for monkey_id, monkey in monkeys.items():
    monkey.compute(monkeys)
    if monkey.id == 'root' and monkey.num is not None:
      root_value = monkey.num
      break
print(root_value)

