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


def compute_op(l, op, r):
  if isinstance(l, str) or isinstance(r, str) or op == '=':
    return f'({l}{op}{r})'
  if op == '/':
    return l / r
  elif op == '*':
    return l * r
  elif op == '+':
    return l + r
  elif op == '-':
    return l - r
  return None


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
        self.num = compute_op(l, self.op, r)

def simplify(equation, val):
  if equation.id == 'humn':
    return val
  l = monkeys[equation.left].num
  r = monkeys[equation.right].num
  assert not isinstance(l, str) or not isinstance(r, str)
  if isinstance(l, str):
    num = r
    if equation.op == '+':  # str + num = val
      return simplify(monkeys[equation.left], val - num)
    if equation.op == '-':  # str - num = val
      return simplify(monkeys[equation.left], val + num)
    if equation.op == '/':  # str / num = val
      return simplify(monkeys[equation.left], val * num)
    if equation.op == '*':  # str * num = val
      return simplify(monkeys[equation.left], val / num)
  if isinstance(r, str):
    num = l
    if equation.op == '+':  # num + str = val
      return simplify(monkeys[equation.right], val - num)
    if equation.op == '-':  # num - str = val
      return simplify(monkeys[equation.right], num - val)
    if equation.op == '/':  # num / str = val
      return simplify(monkeys[equation.right], num / val)
    if equation.op == '*':  # num * str = val
      return simplify(monkeys[equation.right], val / num)
  assert False

monkeys = dict()
for line in lines:
  monkey = Monkey(line)
  if monkey.id == 'humn':
    monkey.num = 'x'
  if monkey.id == 'root':
    monkey.op = '='
  monkeys[monkey.id] = monkey

root_value = None
while root_value is None:
  for monkey_id, monkey in monkeys.items():
    monkey.compute(monkeys)
    if monkey.id == 'root' and monkey.num is not None:
      root_value = monkey.num
      break
# (((3872582054047.0-((((((((2*(((355.0+((316+(2*((((18*(((50+(2*(((112.0+((7+(((((2*(((234+(((10*(285.0+(((((((((((((449.0+(275.0+(2*(((((579.0+((((3*(((403.0+(778.0+(((x+86)*40)-517)))/4)-937))+638.0)/5)-740))/2)+757.0)*8)-750))))/6)-801)/5)+959.0)*16)-890)*2)+897)+291)/4)-280)/4)))-181.0)/3))*2)-93.0))+942.0)/8)-11)+380))/2))*2)-824.0)))/6)-136))+362.0)/2)-976)))/2))/3)-164))+64)*2)-173)/3)+372.0)+749)/10))*27)=40608253763172.0)
print(root_value)

print(simplify(monkeys[monkeys['root'].left], monkeys[monkeys['root'].right].num))


