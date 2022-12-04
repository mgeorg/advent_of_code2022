#!/usr/bin/env python3

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

them_map = {
  'A': 'rock',
  'B': 'paper',
  'C': 'scissors',
}

you_map = {
  'X': 'lose',
  'Y': 'draw',
  'Z': 'win',
}

def score(them, you):
  t = them_map[them]
  result = you_map[you]
  y = None
  if result == 'draw':
    y = t
  elif result == 'lose':
    if t == 'rock':
      y = 'scissors'
    elif t == 'paper':
      y = 'rock'
    elif t == 'scissors':
      y = 'paper'
  elif result == 'win':
    if t == 'rock':
      y = 'paper'
    elif t == 'paper':
      y = 'scissors'
    elif t == 'scissors':
      y = 'rock'

  score = 0
  if y == 'rock':
    score += 1
  elif y == 'paper':
    score += 2
  elif y == 'scissors':
    score += 3

  if t == y:
    score += 3
  elif t == 'rock' and y == 'paper':
    score += 6
  elif t == 'paper' and y == 'scissors':
    score += 6
  elif t == 'scissors' and y == 'rock':
    score += 6
  return score

total = 0
for line in lines:
  them, you = line.split()
  total += score(them, you)
  
print(total)
