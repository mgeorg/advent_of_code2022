#!/usr/bin/env python3

import re

with open('input.txt', 'r') as f:
# with open('sample.txt', 'r') as f:
  lines = f.read().splitlines()

iter_lines = iter(lines)

class Monkey(object):
  def __init__(self):
    self.items = list()
    self.index = None
    self.operation = None
    self.val1 = None
    self.val2 = None
    self.cond = None
    self.branch_true = None
    self.branch_false = None
    self.monkeys = None
    self.inspect_count = 0

  def do_operation(self, worry):
    if self.val1 == 'old':
      v1 = worry
    else:
      v1 = int(self.val1)
    if self.val2 == 'old':
      v2 = worry
    else:
      v2 = int(self.val2)
    if self.operation == '*':
      return v1 * v2
    if self.operation == '+':
      return v1 + v2
    assert False, 'should not reach'
    
  def turn(self):
    items = self.items
    self.items = list()
    for worry in items:
      self.inspect_count += 1
      worry = self.do_operation(worry)
      worry = worry // 3
      if worry % self.cond == 0:
        self.monkeys[self.branch_true].items.append(worry)
      else:
        self.monkeys[self.branch_false].items.append(worry)
      

monkeys = list()
while True:
  monkey = Monkey()
  line = next(iter_lines)
  m = re.match(r'^Monkey (\d+):$', line)
  assert m, line
  monkey.index= int(m.group(1))

  line = next(iter_lines)
  m = re.match(r'^\s+Starting items: ([\d, ]+)$', line)
  assert m
  items = m.group(1).split(', ')
  for item in items:
    monkey.items.append(int(item))

  line = next(iter_lines)
  m = re.match(r'^\s+Operation: new = (old|\d+) (\+|\*) (old|\d+)$', line)
  assert m
  monkey.operation = m.group(2)
  if m.group(1) == 'old':
    monkey.val1 = m.group(1)
  else:
    monkey.val1 = int(m.group(1))
  if m.group(3) == 'old':
    monkey.val2 = m.group(3)
  else:
    monkey.val2 = int(m.group(3))

  line = next(iter_lines)
  m = re.match(r'^\s+Test: divisible by (\d+)$', line)
  assert m
  monkey.cond = int(m.group(1))

  line = next(iter_lines)
  m = re.match(r'^\s+If true: throw to monkey (\d+)$', line)
  assert m
  monkey.branch_true = int(m.group(1))

  line = next(iter_lines)
  m = re.match(r'^\s+If false: throw to monkey (\d+)$', line)
  assert m
  monkey.branch_false = int(m.group(1))

  monkeys.append(monkey)

  try:
    next(iter_lines)
  except StopIteration:
    break


for monkey in monkeys:
  monkey.monkeys = monkeys
  print(monkey.items)


for i in range(20):
  for monkey in monkeys:
    monkey.turn()
  print('#' * 78)
  for monkey in monkeys:
    print(monkey.items)

for monkey in monkeys:
  print(monkey.inspect_count)

#  327*345 = 112815
