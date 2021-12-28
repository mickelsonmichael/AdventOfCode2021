# https://adventofcode.com/2021/day/10

class Part2:
    def run():
        filename = "./Input.txt" # "./Example.txt" 

        with open(filename) as file:
            scores = list()

            for line in file:
                
                stack = list()
                valid = True

                for c in line.strip():
                    if c == "{" or c == "(" or c == "[" or c == "<":
                        stack.append(c)
                        continue

                    if not any(stack):
                        error = c
                        break # close brace before open

                    last = stack.pop()
                    
                    if c == "}" and last == "{":
                        continue
                    elif c == ")" and last == "(":
                        continue
                    elif c == "]" and last == "[":
                        continue
                    elif c == ">" and last == "<":
                        continue
                    else:
                        # incomplete line
                        valid = False
                        break # invalid line
                    
                if not valid:
                    continue # invalid line, skip it

                score = 0
                while any(stack): # incomplete line
                    c = stack.pop()

                    score *= 5

                    if c == "(":
                        score += 1
                    elif c == "[":
                        score += 2
                    elif c == "{":
                        score += 3
                    elif c == "<":
                        score += 4

                if score != 0:
                    scores.append(score)

            scores.sort()
            finalScore = scores[len(scores) // 2]

            print("Part 2 Score:", finalScore)