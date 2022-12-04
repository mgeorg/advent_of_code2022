#!/usr/bin/env python3

with open('input.txt', 'r') as f:
  lines = f.read().splitlines()

them_map = {
  'A': 'rock',
  'B': 'paper',
  'C': 'scissors',
}

you_map = {
  'X': 'rock',
  'Y': 'paper',
  'Z': 'scissors',
}

def score(them, you):
  t = them_map[them]
  y = you_map[you]
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
