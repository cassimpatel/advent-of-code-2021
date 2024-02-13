def day1(part, input):
  def part1(input):
    depths = [int(x) for x in input.split("\n")]
    increasing = 0
    for x in range(1, len(depths)):
      if depths[x] > depths[x-1]:
        increasing += 1
    return increasing
  def part2(input):
    depths = [int(x) for x in input.split("\n")]
    threeSum = sum(depths[0:3])
    #print(threeSum)
    increasing = 0
    for x in range(3, len(depths)):
      prevSum = threeSum
      threeSum += depths[x] - depths[x-3]
      if threeSum > prevSum:
        increasing += 1
      #print(threeSum)
    return increasing
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day2(part, input):
  def part1(input):
    input = [x.split() for x in input.split("\n")]
    pos = {"forward":0, "down":0, "up":0}
    for ins in input:
      pos[ins[0]] += int(ins[1])
    return (pos["forward"]) * (pos["down"] - pos["up"])
  def part2(input):
    input = [x.split() for x in input.split("\n")]
    pos = {"horizontal":0, "depth":0, "aim":0}
    for ins in input:
      command, val = ins[0], int(ins[1])
      if command == "down":
        pos["aim"] += val
      elif command == "up":
        pos["aim"] -= val
      elif command == "forward":
        pos["horizontal"] += val
        pos["depth"] += pos["aim"] * val
    return pos["horizontal"] * pos["depth"]
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day3(part, input):
  import numpy
  def part1(input):
    input = [[int(y) for y in x] for x in input.split("\n")]
    binlen = len(input[0])

    bincount = [0 for x in range(binlen)] #count of 1's in each position x
    for x in input:
      bincount = numpy.add(bincount, x)

    common = len(input) / 2
    gamma = [1 if x > common else 0 for x in bincount]
    gamma = int("".join([str(x) for x in gamma]), 2)
    epsilon = (2 ** binlen -1) - gamma
    return gamma * epsilon
  def part2(input):
    def reduce(mode):
      #mode is either o2 or co2
      lst = [x for x in input.split("\n")]
      index = 0

      while(len(lst) > 1):
        ones = [x[index] == "1" for x in lst].count(True)
        zeros = len(lst) - ones

        if mode == "o2":
          condition = ones >= zeros
        elif mode == "co2":
          condition = ones < zeros

        if condition:
          lst = [x for x in lst if x[index] == "1"]
        else:
          lst = [x for x in lst if x[index] == "0"]
        index += 1
      return int(lst[0],2)
    return reduce("o2") * reduce("co2")
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day4(part, input):
  def part1(input):
    boards = [[y.split() for y in x.split("\n")] for x in input.split("\n\n")[1:]]
    numbers = input.split("\n\n")[0].split(",")
    size = len(boards[0])
    for i in range(len(numbers)):
      num = numbers[i]
      for b in range(len(boards)):
        boardchecked = False
        for y in range(size):
          if boardchecked: break
          for x in range(size):
            if boardchecked: break
            if boards[b][y][x] != num:
              continue
            boards[b][y][x] = "X"
            boardchecked = True
            if i < size: continue #not enough numbers yet to get a bingo

            #check if a win on current row or column
            win = ([a == "X" for a in boards[b][y]].count(False) == 0) or ([a == "X" for a in [boards[b][c][x] for c in range(size)]].count(False) == 0)
            if win == False: continue
            score = sum([sum([int(k) for k in j if k!="X"]) for j in boards[b]])
            #print(b, y, x, score, num)
            return score * int(num)
        #print(boards[b])
    return "panic"
  def part2(input):
    boards = [[y.split() for y in x.split("\n")] for x in input.split("\n\n")[1:]]
    numbers = input.split("\n\n")[0].split(",")
    possWinners = [i for i in range(len(boards))]
    size = len(boards[0])
    for i in range(len(numbers)):
      num = numbers[i]
      for b in possWinners[::-1]:
        boardchecked = False
        for y in range(size):
          if boardchecked: break
          for x in range(size):
            if boardchecked: break
            if boards[b][y][x] != num:
              continue
            boards[b][y][x] = "X"
            boardchecked = True
            if i < size: continue #not enough numbers yet to get a bingo

            #check if a win on current row or column
            win = ([a == "X" for a in boards[b][y]].count(False) == 0) or ([a == "X" for a in [boards[b][c][x] for c in range(size)]].count(False) == 0)
            if win == False: continue
            if len(possWinners) > 1:
              #print(str(b) + " won")
              possWinners.remove(b)
              #print(possWinners)
            else:
              score = sum([sum([int(k) for k in j if k!="X"]) for j in boards[b]])
              return score * int(num)
    return "panic"
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day5(part, input):
  import numpy as np
  def getLinePoints(l):
    x1, y1 = l[0]
    x2, y2 = l[1]
    result = set([])
    xstep = np.sign(x2 - x1)
    ystep = np.sign(y2 - y1)
    #print(x1, y1, x2, y2, xstep, ystep)
    while(x1!=x2 or y1!=y2):
      result.add(str(x1) + "," + str(y1))
      x1 += xstep
      y1 += ystep
    result.add(str(x1) + "," + str(y1))
    return result
  def part1(input):
    input = [x for x in input if x[0][0]==x[1][0] or x[0][1]==x[1][1]]
    points = {}
    for l in input:
      for p in getLinePoints(l):
        if p not in points:
          points[p] = 0
        points[p] += 1
    #print(points)
    return len([x for x in points.values() if x > 1])
  def part2(input):
    points = {}
    for l in input:
      for p in getLinePoints(l):
        if p not in points:
          points[p] = 0
        points[p] += 1
    #print(points)
    return len([x for x in points.values() if x > 1])
  input = [[[int(z) for z in y.split(",")] for y in x.split(" ")] for x in input.replace("-> ", "").split("\n")]
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day6(part, input):
  def calcFish(input, days):
    fish = {x:input.count(str(x)) for x in range(9)}
    for i in range(days):
      fish = {x:fish[(x+1)%9] for x in range(9)}
      fish[6] += fish[8]
    return sum(fish.values())
  def part1(input):
    return calcFish(input, 80)
  def part2(input):
    return calcFish(input, 256)
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day7(part, input):
  import math
  def minFuel(fuelFunc):
    def getCost(position):
      if position not in costs:
        costs[position] = sum([fuelFunc(x, position) for x in input])
      return costs[position]
    costs = {}
    x = math.ceil(sum(input)/len(input)) #current best position
    while(True):
      # print("now checking position " + str(x))
      current = getCost(x) #full fuel cost if the position is at x
      if getCost(x-1) < current: x -= 1
      elif getCost(x+1) < current: x += 1
      else: return int(current)
    return "panic"
  def part1(input):
    def simpleFuelFunc(x, position):
      return abs(x-position)
    return minFuel(simpleFuelFunc)
  def part2(input):
    def complexFuelFunc(x, position):
      d = abs(x-position)
      return d * (d + 1) / 2
    return minFuel(complexFuelFunc)
  input = [int(x) for x in input.split(",")]
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day8(part, input):
  def getNum(unknown, combo1Set, combo4Set):
    unknown = set([x for x in unknown])
    if len(unknown) in [2,4,7,3]: return {2:"1", 4:"4", 3:"7", 7:"8"}[len(unknown)]
    elif len(unknown) == 5:
      if len(combo1Set - unknown) == 0: return "3"
      elif len(combo4Set - unknown) == 1: return "5"
      else: return "2"
    elif len(unknown) == 6:
      if len(combo4Set - unknown) == 0: return "9"
      elif len(combo1Set - unknown) == 0: return "0"
      else: return "6"
  def part1(input):
    input = [x[1] for x in input] #only take second part of each line
    input = [x for sublist in input for x in sublist] #flatten list
    input = [x for x in input if len(x) in [2, 4, 3, 7]]
    return len(input)
  def part2(input):
    total = 0
    for line in input:
      temp = sorted(line[0], key=len)
      oneCombo = set([x for x in temp[0]])
      fourCombo = set([x for x in temp[2]])
      code = "".join([getNum(x, oneCombo, fourCombo) for x in line[1]])
      total += int(code)
    return total
  input = input.replace("|\n", "| ")
  input = [[y.split() for y in x.split(" | ")] for x in input.split("\n")]
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day9(part, input):
  def cave(y, x):
    if x < 0 or x >= len(input[0]): return 10
    elif y < 0 or y >= len(input): return 10
    return input[y][x]
  def getMinPoints():
    minPoints = []
    for y in range(len(input)):
      for x in range(len(input[0])):
        current = cave(y, x)
        if cave(y, x+1) <= current: continue
        elif cave(y+1, x) <= current: continue
        elif cave(y, x-1) <= current: continue
        elif cave(y-1, x) <= current: continue
        #print(y, x, current, current+1)
        minPoints.append([x, y])
    return minPoints
  def part1(input):
    return sum([cave(x[1], x[0]) + 1 for x in getMinPoints()])
  def part2(input):
    import math
    def getBasinSize(y, x):
      if cave(y, x) >= 9: return 0
      elif str(x) + "," + str(y) in checked: return 0

      checked.add(str(x) + "," + str(y))
      size = 1
      current = cave(y, x)
      for adj in [[0, 1],[1, 0],[0, -1],[-1, 0]]:
        if cave(y+adj[0], x+adj[1]) > current:
          size += getBasinSize(y+adj[0], x+adj[1])
      return size
    checked = set([])
    minPoints = getMinPoints()
    basins = [getBasinSize(i[1], i[0]) for i in minPoints]
    basins = sorted(basins, reverse=True)[0:3]
    return math.prod(basins)
  input = [[int(y) for y in x] for x in input.split("\n")]
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day10(part, input):
  def corruptedScore(line):
    pairs = {"(":")", "[":"]", "{":"}", "<":">"}
    scores = {")":3, "]":57, "}":1197, ">":25137}
    stack = []
    for c in line:
      if c in pairs.keys(): stack.append(c)
      elif c != pairs[stack.pop()]: return scores[c]
    return 0
  def completionScore(line):
    pairs = {"(":")", "[":"]", "{":"}", "<":">"}
    scores = {")":1, "]":2, "}":3, ">":4}
    stack = []
    for c in line:
      if c in pairs.keys(): stack.append(c)
      else: stack.pop()
    score = 0
    while (len(stack) > 0):
      score = score*5 + scores[pairs[stack.pop()]]
    return score
  def part1(input):
    return sum([corruptedScore(x) for x in input])
  def part2(input):
    input = [x for x in input if corruptedScore(x) == 0]
    scores = sorted([completionScore(x) for x in input])
    return scores[int((len(scores)-1)/2)]
  input = input.split("\n")
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day11(part, input):
  def flash(cave, x, y):
    if x < 0 or x >= 10: return
    elif y < 0 or y >= 10: return
    elif cave[y][x] == 10: return
    cave[y][x] += 1
    if cave[y][x] < 10: return
    for dy in range(-1, 2):
      for dx in range(-1, 2):
        if dy == 0 and dx == 0: continue
        flash(cave, x+dx, y+dy)
  def showCave(cave):
    print("*****showing cave*****")
    for x in cave:
      print("".join([str(y) for y in x]))
  def runStep(cave):
    _ = [flash(cave, x, y) for x in range(10) for y in range(10)]
    cave = [[x%10 for x in y] for y in cave]
    return cave
  def part1(input):
    flashes = 0
    for _ in range(100):
      input = runStep(input)
      flashes += sum(x.count(0) for x in input)
    return flashes
  def part2(input):
    step = 0
    while(True):
      input = runStep(input)
      step += 1
      if sum(x.count(0) for x in input) == 100: return step
    return "panic"
  input = [[int(y) for y in x] for x in input.split("\n")]
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day12(part, input):
  from collections import defaultdict
  def numUnique(cave, current, path):
    if current == "end": return 1
    elif current[0].islower() and current in path: return 0
    path += "," + current
    return sum([numUnique(cave, x, path) for x in cave[current]])
  def uniqueNew(cave, current, path, specialCave):
    if current == "end":
      return [path]
    elif current == specialCave and path.count(current) == 2: return []
    elif current != specialCave and current[0].islower() and path.count(current) == 1: return []
    path += "," + current
    uniquePaths = []
    for x in cave[current]:
      if x == "start": continue
      uniquePaths += uniqueNew(cave, x, path, specialCave)
      if current[0].islower() and specialCave == "":
        uniquePaths += uniqueNew(cave, x, path, current)
    return set(uniquePaths)
  def part1(input):
    return numUnique(input, "start", "")
  def part2(input):
    return len(uniqueNew(input, "start", "", ""))
  poss = defaultdict(lambda: [])
  for x in input.split("\n"):
    cave1, cave2 = x.split("-")
    poss[cave1].append(cave2)
    poss[cave2].append(cave1)
  input = poss
  if part == 1: return part1(input)
  elif part == 2: return part2(input)

def day13(part, input):
  def runIns(points, direction, line):
    newPoints = points.copy()
    if direction == "x":
      for p in points:
        x, y = [int(a) for a in p.split(",")]
        if x < line: continue
        newPoints.remove(p)
        x = 2*line - x
        newPoints.add(str(x) + "," + str(y))
    elif direction == "y":
      for p in points:
        x, y = [int(a) for a in p.split(",")]
        if y < line: continue
        newPoints.remove(p)
        y = 2*line - y
        newPoints.add(str(x) + "," + str(y))
    return newPoints
  def part1(points, firstIns):
    return len(runIns(points, firstIns[0], int(firstIns[1])))
  def part2(points, insList):
    for ins in insList:
      points = runIns(points, ins[0], int(ins[1]))
    maxX = max([int(x.split(",")[0]) for x in points])
    maxY = max([int(x.split(",")[1]) for x in points])
    for y in range(maxY+1):
      for x in range(maxX+1):
        if str(x) + "," + str(y) in points: print("#", end="")
        else: print(".", end="")
      print()
    return "Read letters in password from console"
  points, ins = input.replace("fold along ", "").split("\n\n")
  points = set(points.split("\n"))
  ins = [x.split("=") for x in ins.split("\n")]
  if part == 1: return part1(points, ins[0])
  elif part == 2: return part2(points, ins)

def day14(part, input):
  from collections import defaultdict
  import math
  def calcResult(template, rules, steps):
    polymer = defaultdict(lambda: 0)
    for x in range(len(template)-1):
      pair = template[x: x+2]
      polymer[pair] += 1

    for _ in range(steps):
      newPolymer = defaultdict(lambda: 0)
      for x in polymer:
        if x in rules:
          midChar = rules[x]
          newPolymer[x[0] + midChar] += polymer[x]
          newPolymer[midChar + x[1]] += polymer[x]
        else:
          newPolymer[x] += polymer[x]
      polymer = newPolymer
    chars = set([x for x in "".join(polymer.keys())])
    counts = {x:sum([y.count(x)*polymer[y] for y in polymer]) for x in chars}
    counts= {x:math.ceil(y/2) for x,y in counts.items()}
    return max(counts.values()) - min(counts.values())
  def part1(start, insertions):
    return calcResult(start, insertions, 10)
  def part2(start, insertions):
    return calcResult(start, insertions, 40)
  template, insertions = input.split("\n\n")
  insertions = {x[0:2]:x[2] for x in insertions.replace(" -> ","").split("\n")}
  if part == 1: return part1(template, insertions)
  elif part == 2: return part2(template, insertions)

def day15(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day16(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day17(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day18(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day19(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day20(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day21(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day22(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day23(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day24(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

def day25(part, input):
	def part1(input):
		return "unattempted"
	def part2(input):
		return "unattempted"
	if part == 1: return part1(input)
	elif part == 2: return part2(input)

with open("input.txt", "r") as fileObject: input = fileObject.read()
print(day15(1,input))

#create a main thing so u can take an arg from terminal? 