#!/usr/bin/env python3

import collections
import copy
import json
import queue
import re
import sys

_COUNT_SELF = False
_APPLY_KEY = True
_FILENAME = 'input.txt'
if len(sys.argv) >= 2:
  _FILENAME = sys.argv[1]

with open(_FILENAME, 'r') as f:
  lines = f.read().splitlines()

class Entry(object):
  def __init__(self, val):
    if _APPLY_KEY:
      self.val = val * 811589153
    else:
      self.val = val
    self.prev = None
    self.next = None

class NumList(object):
  def __init__(self, vals):
    self.nums = list()
    self.zero = None
    prev = None
    for val in vals:
      cur = Entry(val)
      if val == 0:
        self.zero = cur
      self.nums.append(cur)
      if prev:
        cur.prev = prev
        prev.next = cur
      prev = cur
    self.nums[0].prev = self.nums[-1]
    self.nums[-1].next = self.nums[0]

  def mix(self):
    iterations = 0
    for num in self.nums:
      iterations += 1
      if num.val == 0:
        # print('#' * 40)
        # print('val == 0')
        # print(f'iterations = {iterations}')
        # print(str(nums))
        continue
      if _COUNT_SELF:
        size = len(self.nums)
      else:
        # Remove item
        num.prev.next = num.next
        num.next.prev = num.prev
        size = len(self.nums) - 1
      if num.val > 0:
        target = num
        shift = (num.val+1) % size
        if shift == 0:
          target = target.prev
        else:
          for i in range(shift):
            target = target.next
      else:
        target = num
        shift = (-num.val) % size
        if shift == 0:
          target = target.next
        else:
          for i in range(shift):
            target = target.prev
      if target == num:
        assert _COUNT_SELF
        # print('#' * 40)
        # print('target == num')
        # print(f'iterations = {iterations}')
        # print(str(nums))
        continue
      if _COUNT_SELF:
        # Remove item
        num.prev.next = num.next
        num.next.prev = num.prev
      # Move item to (before) target location
      num.prev = target.prev
      num.next = target
      target.prev.next = num
      target.prev = num
      # print('#' * 40)
      # print(f'iterations = {iterations}')
      # print(str(nums))

  def result(self):
    cur = self.zero
    total = 0
    for i in range(1000):
      cur = cur.next
    print(cur.val)
    total += cur.val
    for i in range(1000):
      cur = cur.next
    print(cur.val)
    total += cur.val
    for i in range(1000):
      cur = cur.next
    print(cur.val)
    total += cur.val
    print(total)
    return total
    
  def __str__(self):
    output = list()
    cur = self.zero
    while not output or cur.val != self.zero.val:
      output.append(f'{cur.val}')
      if cur == self.nums[0]:
        output[-1] += ' <- first'
      # output.append(f'{cur.prev.val} , {cur.val} , {cur.next.val}')
      cur = cur.next
    return '\n'.join(output)


nums = NumList([int(x) for x in lines])
for i in range(10):
  # print('#' * 40)
  # print(str(nums))
  nums.mix()
print('#' * 40)
print('final')
print(str(nums))
print('#' * 40)
print('result')
print(nums.result())

