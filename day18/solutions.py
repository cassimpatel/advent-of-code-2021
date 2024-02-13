import re
from math import floor, ceil
from queue import PriorityQueue

class SnailFishNum:
    def __init__(self, val = None, left = None, right = None, parent = None, nesting = 0):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.nesting = nesting

    # convert back to list format as shown in input
    def __repr__(self):
        if self.val != None: return str(self.val)
        return '[{},{}]'.format(self.left, self.right)

    # increment every node's nesting level in the tree by 1
    def increment_nesting(self):
        self.nesting += 1
        if self.left != None: self.left.increment_nesting()
        if self.right != None: self.right.increment_nesting()

    # find the next regular number to the left of this snailfish node, none if there is no node
    def get_next_left(self):
        curr = self
        # traverse up until we find an opportunity to visit a left child, return if we reach root
        while True:
            if curr.parent is None: return None
            pLeft, pRight = curr.parent.left, curr.parent.right
            if pLeft is not curr:
                curr = pLeft
                break
            curr = curr.parent
        # find the furthest right leaf of this subtree
        while curr.right != None:
            curr = curr.right
        return curr

    # find the node for the next regular number to the right of this node (similar to get_next_left)
    def get_next_right(self):
        curr = self
        while True:
            if curr.parent is None: return None
            pLeft, pRight = curr.parent.left, curr.parent.right
            if pRight is not curr:
                curr = pRight
                break
            curr = curr.parent
        while curr.left != None:
            curr = curr.left
        return curr

    # get an enumeration of this node in the full number ordering (useful for tracking which is the furthest left (smallest))
    def get_index(self):
        # get L R movement backwards, use binary repr going back down
        path = []

        curr = self
        while curr.parent != None:
            pLeft, pRight = curr.parent.left, curr.parent.right
            path.insert(0, 'L' if curr is pLeft else 'R')
            curr = curr.parent

        index = 0
        i = 5
        for dir in path:
            index += (2 ** i) * (1 if dir == 'R' else 0)
            i -= 1
        
        return index

    # def __lt__(self, other):
    #     return self.val < other.val

    def reduce(self):
        unresolved_explodes = PriorityQueue()
        unresolved_splits = PriorityQueue()

        # search over the tree via DFS for nums that are nested 4 deep, add to unresolved
        frontier = [self]
        while len(frontier) > 0:
            curr = frontier.pop(0)
            if curr.val != None: continue
            if curr.nesting == 4:
                unresolved_explodes.put((curr.get_index(), curr))
                continue
            frontier = [curr.left, curr.right] + frontier

        while True:
            if unresolved_explodes.empty() and unresolved_splits.empty(): break
            # print('beginning of loop', newRoot)

            if not unresolved_explodes.empty():
                # print('explode')
                (index, curr) = unresolved_explodes.get()
                lVal, rVal = curr.left.val, curr.right.val
                nextLeft, nextRight = curr.get_next_left(), curr.get_next_right()
                if nextLeft != None:
                    nextLeft.val += lVal
                    if nextLeft.val > 9: unresolved_splits.put((nextLeft.get_index(), nextLeft))
                if nextRight != None:
                    nextRight.val += rVal
                    if nextRight.val > 9: unresolved_splits.put((nextRight.get_index(), nextRight))
                curr.val, curr.left, curr.right = 0, None, None

            elif not unresolved_splits.empty():
                # print('split')
                (index, curr) = unresolved_splits.get()
                # print('THIS', curr)
                if curr.val == None: continue
                curr.left = SnailFishNum(floor(curr.val / 2), None, None, curr, curr.nesting + 1)
                curr.right = SnailFishNum(ceil(curr.val / 2), None, None, curr, curr.nesting + 1)
                if curr.nesting == 4: unresolved_explodes.put((index, curr))
                curr.val = None

    def add(self, r_num):
        # join the two nums together, update nesting levels
        l_num = self
        newRoot = SnailFishNum(None, l_num, r_num, None, 0)
        l_num.parent = r_num.parent = newRoot
        l_num.increment_nesting()
        r_num.increment_nesting()

        newRoot.reduce()
        return newRoot
        
    def get_magnitude(self):
        if self.val != None: return self.val
        return self.left.get_magnitude() * 3 + self.right.get_magnitude() * 2

def string_to_snailfish(input):
    root = SnailFishNum()
    curr = root.left = SnailFishNum(None, None, None, root, 1)

    for char in input[1:]:
        if char == '[':
            curr.left = SnailFishNum(None, None, None, curr, curr.nesting + 1)
            curr = curr.left
        elif char == ']':
            curr = curr.parent
        elif char == ',':
            curr.parent.right = SnailFishNum(None, None, None, curr.parent, curr.nesting)
            curr = curr.parent.right
        else:
            curr.val = int(char)

    return root

def get_matching_indices(pattern, str):
    return [x.start() for x in re.finditer(pattern, str)]

def get_exploding_index(num):
    nesting = -1
    for i, char in enumerate(num):
        if char == '[': nesting += 1
        elif char == ']': nesting -= 1
        if nesting == 4: return i
    return None

def get_splitting_index(num):
    result = get_matching_indices('\d\d', num)
    if len(result) > 0: return result[0]
    return None

def reduce_snailfish_num(num):
    while True:
        
        exploding = get_exploding_index(num)
        splitting = get_splitting_index(num) if exploding == None else None
        print(num, exploding, splitting)

        if exploding == None and splitting == None: break

        if exploding != None:
            # part1, lNum, rNum, part2 = num[:exploding], int(num[exploding+1]), int(num[exploding+3]), num[exploding+5:]

            part1, part2 = num[:exploding], num[exploding+5:]
            print(re.findall('[0-9]+', num[exploding: exploding+5]))
            [lNum, rNum] = [int(x) for x in re.findall('[0-9]+', num[exploding: exploding+5])]

            part1_nums = get_matching_indices('\d', part1)
            if len(part1_nums) > 0:
                part1_last_num = part1_nums[-1]
                part1 = part1[:part1_last_num] + str(lNum + int(part1[part1_last_num])) + part1[part1_last_num+1:]

            part2_nums = get_matching_indices('\d', part2)
            if len(part2_nums) > 0:
                part2_first_num = part2_nums[0]
                part2 = part2[:part2_first_num] + str(rNum + int(part2[part2_first_num])) + part2[part2_first_num+1:]

            num = part1 + '0' + part2

            pass
        elif splitting != None:
            part1, splittingNum, part2 = num[:splitting], int(num[splitting:splitting+2]), num[splitting+2:]
            new_pair = '[{},{}]'.format(floor(splittingNum / 2), ceil(splittingNum / 2))
            num = part1 + new_pair + part2

    return num
        
def day15_part1(input):
    # snailfish_num1 = parse_input('[[[[4,3],4],4],[7,[[8,4],9]]]')
    # snailfish_num2 = parse_input('[1,1]')
    # print(snailfish_num1, snailfish_num2)
    # snailfish_num1.add(snailfish_num2)
    input = input.split('\n')
    result = string_to_snailfish(input[0])
    for other_num in input[1:]:
        print('adding new num on', other_num)
        other_num = string_to_snailfish(other_num)
        result = result.add(other_num)
        print('now result', result)

    # for other_num in input[1:]:
    #     print('adding new num on', other_num)
    #     result = '[{},{}]'.format(result, other_num)
    #     result = reduce_snailfish_num(result)
    # print(result)
    return None

def day15_part2(input):
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day15_part1(example_input) == 4140
    print(day15_part1(test_input))

    # assert day15_part2(example_input) == 315
    # print(day15_part2(test_input))