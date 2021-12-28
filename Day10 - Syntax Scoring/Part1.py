# https://adventofcode.com/2021/day/10

class Part1:
    def run():
        filename = "./Input.txt" 

        with open(filename) as file:
            score = 0

            for line in file:
                stack = list()
                error = ""

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
                        error = c
                        break # invalid line
                    
                if error != "":
                    if error == ")":
                        score += 3
                    elif error == "]":
                        score += 57
                    elif error == "}":
                        score += 1197
                    elif error == ">":
                        score += 25137

            print("Score:", score)