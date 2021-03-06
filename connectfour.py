from sense_hat import *
from math import *
import copy, time, random
s = SenseHat()
c = copy.copy

def rc(r, c): #row, column to pixel index
  return c + r * 8
  
def drop():
  global p
  global tr
  global tc
  global player
  while p[rc(tr + 1, tc)] != p1 and p[rc(tr + 1, tc)] != p2 and p[rc(tr + 1, tc)] != w:
    p[rc(tr, tc)] = c(b)
    tr += 1
    p[rc(tr, tc)] = c(player)
    s.set_pixels(p)
    time.sleep(0.07)

def check(p, dr, dc, tr, tc):
  counter = 0
  counter1 = 0
  counter2 = 0
  for x in range(1, 4):
    try:
      if tr + (x * dr) > 6 or tc + (x * dc) > 6 or tr + (x * dr) < 1  or tc + (x * dc) < 0:
        counter += 0
      elif p[rc(tr, tc)] != p[rc(tr + (x * dr), tc + (x * dc))]:
        break
      elif p[rc(tr, tc)] == p[rc(tr + (x * dr), tc + (x * dc))]:
        counter += 1
        counter1 = x
    except IndexError:
      counter += 0
  for x in range(1, 4):
    try:
      if tr - (x * dr) < 1  or tc - (x * dc) < 0 or tr - (x * dr) > 6  or tc - (x * dc) > 6:
        counter += 0
      elif p[rc(tr, tc)] != p[rc(tr - (x * dr), tc - (x * dc))]:
        break
      elif p[rc(tr, tc)] == p[rc(tr - (x * dr), tc - (x * dc))]:
        counter += 1
        counter2 = x
    except IndexError:
      counter += 0
  if counter >= 3:
    global winningpos
    winningpos = (p, counter2, counter1, tr, tc, dr, dc)
    return True
  else:
    return False

def checkall(p, tr, tc):
  if \
  check(p, -1, 0, tr, tc) or \
  check(p, -1, 1, tr, tc) or \
  check(p, 0, 1, tr, tc) or \
  check(p, 1, 1, tr, tc):
    return True
  else:
    return False

def winrowcolor(p, counter2, counter1, tr, tc, dr, dc):
  while True:
    clr = [0, 255, random.randint(0, 255)]
    random.shuffle(clr)
    for x in range(-counter2, counter1 + 1):
      
      p[rc(tr + (x * dr), tc + (x * dc))] = clr
      s.set_pixels(p)
      time.sleep(0.01)
  
winningpos = None
human = 1
computer = 2
vscomputer = 3
p = [] #stands for pixels
b = [0, 0, 0] #stands for black
w = [255, 255, 255] #stands for white
colors = {'red' : [255, 0, 0], 'orange' : [255, 128, 0],\
'yellow' : [255, 255, 0], 'cyan' : [0, 255, 255], 'green' : [0, 255, 0], \
'blue' : [0, 0, 255], 'purple' : [255, 0, 255]}
tc = 3  #Stands for token column
tr = 0  #Stands for token row
turncounter = 1

for x in range(64):
  p.append(c(b))
  
for num in range(8):
  p[rc(num, 7)] = c(w)
  p[rc(7, num)] = c(w)
s.set_pixels(p)
print("Color List: Red, Orange, Yellow, Green, Cyan, Blue, Purple.")

while True:
  try:
    p1color = input("Player 1, please type your color from the list.").lower() or 'red'
    p1 = colors[p1color]
    break
  except KeyError:
    print("Please choose a color from the list.")

while vscomputer != human and vscomputer != computer:
  vscomputer = input("Would you like to play against a computer? [y/n]") or 'y'
  if vscomputer == 'y':
    vscomputer = computer
  else:
    vscomputer = human

if vscomputer == human:
  while True:
    try:
      p2color = input("Player 2, please type your color from the list.").lower() or 'yellow'
      p2 = colors[p2color]
      if p1color == p2color:
        print("Choose a different color than Player 1")
        raise KeyError()
      break
    except KeyError:
      print("Please choose a color from the list.")
else:
  if p1color != 'red':
    p2color = 'red'
    p2 = colors[p2color]
  else:
    p2color = 'yellow'
    p2 = colors[p2color]

print("Move the joystick left and right to move your token, push down \
on the joystick to release your token.")
p[rc(tr, tc)] = c(p1)
s.set_pixels(p)

player = p1
while True:
  events = s.stick.get_events()
  for e in events:
    
    if vscomputer == computer and player == p2:
      p[rc(tr, tc)] = c(b)
      tc = random.randint(0, 6)
      while p[rc(tr + 1, tc)] == p1 or p[rc(tr + 1, tc)] == p2:
        tc = random.randint(0, 6)
      p[rc(tr, tc)] = c(player)
      s.set_pixels(p)
      time.sleep(0.3)
      drop()
      if(checkall(p, tr, tc)):
        if player == p1:
          print("Player 1 has won!")
        else:
          print("Computer has won!")
        winrowcolor(*winningpos)
      turncounter += 1
      if turncounter % 2 == 1:
        player = p1
      else:
        player = p2
      tr = 0
      tc = 3
      p[rc(tr, tc)] = c(player)
      s.set_pixels(p)
      continue
      
    if e.direction == 'right' and e.action == 'pressed':
      p[rc(tr, tc)] = c(b)
      tc += 1
      if tc == 7:
        tc = 0
      p[rc(tr, tc)] = c(player)
      s.set_pixels(p)
      
    if e.direction == 'left' and e.action == 'pressed':
      p[rc(tr, tc)] = c(b)
      tc -= 1
      if tc == -1:
        tc = 6
      p[rc(tr, tc)] = c(player)
      s.set_pixels(p)
      
    if (e.direction == 'down' or e.direction == 'middle') and e.action == 'pressed' and p[rc(tr + 1, tc)] != p1 and p[rc(tr + 1, tc)] != p2:
      drop()
      if(checkall(p, tr, tc)):
        if player == p1:
          print("Player 1 has won!")
        else:
          print("Player 2 has won!")
        winrowcolor(*winningpos)
        
      turncounter += 1
      if turncounter % 2 == 1:
        player = p1
      else:
        player = p2
      tr = 0
      tc = 3
      p[rc(tr, tc)] = c(player)
      s.set_pixels(p)

  if turncounter == 43:
    print("The game was a draw!")
    break
