#!/usr/bin/env python3

import collections
import copy
import json
import queue
import re

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

initial_state = {
    'ore_robot': 1,
    'clay_robot': 0,
    'obsidian_robot': 0,
    'geode_robot': 0,
    'ore': 0,
    'clay': 0,
    'obsidian': 0,
    'geode': 0,
}

memoized = dict()
def worth_pursuing_true(new_state, time_left):
  return True

def worth_pursuing(new_state, time_left):
  robots = (
      new_state['ore_robot'],
      new_state['clay_robot'],
      new_state['obsidian_robot'],
      new_state['geode_robot'],
      time_left)
  resources = (
      new_state['ore'],
      new_state['clay'],
      new_state['obsidian'],
      new_state['geode'])
  memo = memoized.get(robots)
  if memo is None:
    memoized[robots] = resources
    return True
  if (memo[0] >= resources[0] and
      memo[1] >= resources[1] and
      memo[2] >= resources[2] and
      memo[3] >= resources[3]):
    return False
  if (memo[0] <= resources[0] and
      memo[1] <= resources[1] and
      memo[2] <= resources[2] and
      memo[3] <= resources[3]):
    memoized[robots] = resources
  return True

class Blueprint(object):
  def __init__(self, line):
    m = re.match(r'Blueprint (\d+): Each ore robot costs (\d+) ore\. +Each clay robot costs (\d+) ore\. +Each obsidian robot costs (\d+) ore and (\d+) clay\. +Each geode robot costs (\d+) ore and (\d+) obsidian\.$', line)
    assert m
    self.blueprint_id = int(m.group(1))
    self.ore_robot = int(m.group(2))
    self.clay_robot = int(m.group(3))
    self.obsidian_robot = (int(m.group(4)), int(m.group(5)))
    self.geode_robot = (int(m.group(6)), int(m.group(7)))

  def evaluate(self, state, time_left):
    if time_left == 1:
      return state['geode'] + state['geode_robot']
    can_build_ore = self.ore_robot <= state['ore']
    can_build_clay = self.clay_robot <= state['ore']
    can_build_obsidian = (self.obsidian_robot[0] <= state['ore'] and
                          self.obsidian_robot[1] <= state['clay'])
    can_build_geode = (self.geode_robot[0] <= state['ore'] and
                       self.geode_robot[1] <= state['obsidian'])
    if time_left == 2:
      if can_build_geode:
        return state['geode'] + 2*state['geode_robot'] + 1
      else:
        return state['geode'] + 2*state['geode_robot']
    can_build = (
        can_build_ore, can_build_clay, can_build_obsidian, can_build_geode)

    previous_can_build = state.get('can_build')
    if previous_can_build:
      if previous_can_build[0]:
        can_build_ore = False
      if previous_can_build[1]:
        can_build_clay = False
      if previous_can_build[2]:
        can_build_obsidian = False
      if previous_can_build[3]:
        can_build_geode = False

    values = list()

    if can_build_ore:
      new_state = copy.copy(state)
      if 'can_build' in new_state:
        del new_state['can_build']
      new_state['ore'] += new_state['ore_robot']
      new_state['clay'] += new_state['clay_robot']
      new_state['obsidian'] += new_state['obsidian_robot']
      new_state['geode'] += new_state['geode_robot']
      new_state['ore'] -= self.ore_robot
      new_state['ore_robot'] += 1
      if worth_pursuing(new_state, time_left-1):
        values.append(self.evaluate(new_state, time_left-1))
    if can_build_clay:
      new_state = copy.copy(state)
      if 'can_build' in new_state:
        del new_state['can_build']
      new_state['ore'] += new_state['ore_robot']
      new_state['clay'] += new_state['clay_robot']
      new_state['obsidian'] += new_state['obsidian_robot']
      new_state['geode'] += new_state['geode_robot']
      new_state['ore'] -= self.clay_robot
      new_state['clay_robot'] += 1
      if worth_pursuing(new_state, time_left-1):
        values.append(self.evaluate(new_state, time_left-1))
    if can_build_obsidian:
      new_state = copy.copy(state)
      if 'can_build' in new_state:
        del new_state['can_build']
      new_state['ore'] += new_state['ore_robot']
      new_state['clay'] += new_state['clay_robot']
      new_state['obsidian'] += new_state['obsidian_robot']
      new_state['geode'] += new_state['geode_robot']
      new_state['ore'] -= self.obsidian_robot[0]
      new_state['clay'] -= self.obsidian_robot[1]
      new_state['obsidian_robot'] += 1
      if worth_pursuing(new_state, time_left-1):
        values.append(self.evaluate(new_state, time_left-1))
    if can_build_geode:
      new_state = copy.copy(state)
      if 'can_build' in new_state:
        del new_state['can_build']
      new_state['ore'] += new_state['ore_robot']
      new_state['clay'] += new_state['clay_robot']
      new_state['obsidian'] += new_state['obsidian_robot']
      new_state['geode'] += new_state['geode_robot']
      new_state['ore'] -= self.geode_robot[0]
      new_state['obsidian'] -= self.geode_robot[1]
      new_state['geode_robot'] += 1
      if worth_pursuing(new_state, time_left-1):
        values.append(self.evaluate(new_state, time_left-1))

    new_state = copy.copy(state)
    new_state['ore'] += new_state['ore_robot']
    new_state['clay'] += new_state['clay_robot']
    new_state['obsidian'] += new_state['obsidian_robot']
    new_state['geode'] += new_state['geode_robot']
    new_state['can_build'] = can_build
    # print(new_state)
    if worth_pursuing(new_state, time_left-1):
      values.append(self.evaluate(new_state, time_left-1))

    if values:
      return max(values)
    else:
      return 0


blueprints = list()
for line in lines:
  blueprints.append(Blueprint(line))

total = 0
for b in blueprints:
  memoized = dict()
  best = b.evaluate(initial_state, 24)
  print(f'{b.blueprint_id}: {best}  ({b.blueprint_id*best})')
  total += int(b.blueprint_id) * best

print(total)
