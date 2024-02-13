from queue import PriorityQueue

# gets the total risk for the minimum path from the top left cell to bottom right one via A*
# if largeGrid is true: make grid 5 times larger according to part 2 specification
def getMinPathRisk(input, largeGrid = False):
    grid = [[int(y) for y in x] for x in input.split('\n')]
    h, w = (len(grid) * 5, len(grid[0]) * 5) if largeGrid else (len(grid), len(grid[0]))

    # state represented by (x, y) location
    strtState = (0, 0)
    xGoal, yGoal = w - 1, h - 1

    frontier = PriorityQueue()
    cost_so_far = {strtState: 0}
    frontier.put((0, strtState))
    
    while not frontier.empty():
        priority, (x, y) = priority, current = frontier.get()
        
        if current == (xGoal, yGoal):
            break
        
        for (dx, dy) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= w: continue
            if ny < 0 or ny >= h: continue

            if largeGrid:
                tileDist = (nx // len(grid)) + (ny // len(grid[0])) # number of maps right and down this tile sits
                tileVal = ((grid[ny % len(grid)][nx % len(grid[0])] - 1 + tileDist) % 9) + 1
            else:
                tileVal = grid[ny][nx]

            next_state = (nx, ny)
            new_cost = cost_so_far[current] + tileVal
            heuristic = abs(nx - xGoal) + abs(ny - yGoal)
            
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + heuristic
                frontier.put((priority, next_state))
    
    return cost_so_far[(xGoal, yGoal)]

def day15_part1(input):
    return getMinPathRisk(input)

def day15_part2(input):
    return getMinPathRisk(input, True)

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day15_part1(example_input) == 40
    print(day15_part1(test_input))

    assert day15_part2(example_input) == 315
    print(day15_part2(test_input))