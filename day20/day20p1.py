#!/usr/bin/env python3

import collections
import copy
import json
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

class Entry(object):
  def __init__(self, val):
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
    print('#' * 40)
    print(str(self))
    for num in self.nums:
      if num.val == 0:
        continue
      # Remove item
      num.prev.next = num.next
      num.next.prev = num.prev
      if num.val > 0:
        target = num
        for i in range(num.val+1):
          target = target.next
      else:
        target = num
        for i in range(-num.val):
          target = target.prev
      num.prev = target.prev
      num.next = target
      target.prev.next = num
      target.prev = num
      # print('#' * 40)
      # print(str(self))

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
      output.append(f'{cur.prev.val} , {cur.val} , {cur.next.val}')
      cur = cur.next
    return '\n'.join(output)


nums = NumList([int(x) for x in lines])
nums.mix()
print(nums.result())

