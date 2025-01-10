from sys import argv

### Must have queries and rules
### Check if rule contradict a fact on any other rule.
class expert_system:
    def __init__(self, file_path):
        self.file_path = file_path 
        self.parse_input_file(file_path)
        for i in range(200):
            print(f"\nLoop numnber : {i + 1}")
            self.find_values()
        print("\n\nResults for our queries :\n")
        for i in self.queries:
            if i in self.facts:
                print(f"{i} is True.")
            else:
                print(f"{i} is False.")

    def conclude(self, solved_rule):
        print("Which implies :")
        index = solved_rule.find(">")
        neg = 0
        true_values = []
        false_values = []
        if index != -1 and solved_rule[index - 2] != '<' :
            if '+' in solved_rule:
                while index < len(solved_rule) - 1:
                    index += 1
                    if solved_rule[index] != ' ' and solved_rule[index] != '+':
                        if solved_rule[index] == '!':
                            neg = 1
                        else :
                            if neg == 1 :
                                neg = 0
                                false_values.append(solved_rule[index])
                                print(f"{solved_rule[index]} is false.")
                            else :
                                true_values.append(solved_rule[index])
                                print(f"{solved_rule[index]} is true.")

            elif '|' in solved_rule:
                tmp_list = []
                while index < len(solved_rule) - 1:
                    index += 1
                    if solved_rule[index] != ' ' and solved_rule[index] != '|':
                        if solved_rule[index] == '!':
                            neg = 1
                        else :
                            res = ''
                            if neg == 1 :
                                neg = 0
                                res += '!'
                            res += str(solved_rule[index])
                            if len(res) > 1 and res[1] not in self.facts:
                                tmp_list.append(res)
                            elif len(res) == 1 and res not in self.false_facts:
                                tmp_list.append(res)
                if len(tmp_list) == 1:
                    if len(tmp_list[0]) > 1:
                        print(f"{tmp_list[0]} is the only assumption which isnt false so we can confirm it's value is false.")
                        false_values.append(tmp_list[0][1])
                    else :
                        print(f"{tmp_list[0]} is the only assumption which isnt false so we can confirm it's value is true.")
                        true_values.append(tmp_list[0])

            elif '^' in solved_rule:
                true = None
                false = []
                tmp_list = []
                while index < len(solved_rule) - 1:
                    index += 1
                    if solved_rule[index] != ' ' and solved_rule[index] != '^':
                        if solved_rule[index] == '!':
                            neg = 1
                        else :
                            res = ''
                            if neg == 1 :
                                neg = 0
                                res += '!'
                            res += str(solved_rule[index])
                            tmp_list.append(res)
                            if len(res) > 1:
                                if res[1] in self.false_facts:
                                    if true == None:
                                        true = res
                                elif res[1] in self.facts :
                                    false.append(res)
                            else:
                                if res in self.facts:
                                    if true == None:
                                        true = res
                                elif res in self.false_facts:
                                    false.append(res)
                if true != None :
                    for i in tmp_list:
                        if i != true:
                            if len(i) > 1:
                                true_values.append(i[1])
                                print(f"{i} is automatically confirmed true because we already know {true} is true which make this statement false.")
                            else :
                                false_values.append(i)
                                print(f"{i} is automatically confirmed false because we already know {true} is true which make this statement false.")
                elif len(false) + 1 == len(tmp_list):
                    for i in tmp_list:
                        if i not in false:
                            if len(i) > 1: 
                                false_values.append(i[1])
                                print(f"{i} is automatically confirmed false because all other statements were wrong so this statement is true.")
                            else :
                                true_values.append(i)
                                print(f"{i} is automatically confirmed true because all other statements were wrong so this statement is true.")
                                                
            else:
                while index < len(solved_rule) - 1:
                    index += 1
                    if solved_rule[index] != ' ':
                        if solved_rule[index] == '!':
                            neg = 1
                        else :
                            if neg == 1:
                                neg = 0
                                false_values.append(solved_rule[index])
                                print(f"{solved_rule[index]} is confirmed as false.")
                            elif neg == 0:
                                true_values.append(solved_rule[index])
                                print(f"{solved_rule[index]} is confirmed as true.")
            for i in true_values:
                if i in self.false_facts:
                    print(f"Rule '{solved_rule}' contradict another rule, saying that {i} is true. This rule will be ignored")
                    self.rules.remove(solved_rule)
                    return
            for i in false_values:
                if i in self.facts:
                    print(f"Rule '{solved_rule}' contradict another rule, saying that {i} is false. This rule will be ignored")
                    self.rules.remove(solved_rule)
                    return
            for i in true_values:
                if i not in self.facts:
                    self.facts.append(i)
            for i in false_values:
                if i not in self.false_facts:
                    self.false_facts.append(i)

                            

    def treate_or(self, rule):
        rule = list(rule) 
        indexes = [i for i, char in enumerate(rule) if char == "|"]
        for i in indexes:
            result = '2'
            prev_i = i - 1
            next_i = i + 1
            while rule[prev_i] == ' ':
                prev_i -= 1
            while rule[next_i] == ' ':
                next_i += 1
            if rule[prev_i] == '1' or rule[prev_i] in self.facts:
                print(f"{rule[prev_i]} is true so the result of '{rule[prev_i]} | {rule[next_i]}' is true.")
                result = '1'
            elif rule[next_i] == '1' or rule[next_i] in self.facts:
                print(f"{rule[next_i]} is true so the result of '{rule[prev_i]} | {rule[next_i]}' is true.")
                result = '1'
            elif result == '2':
                print(f"None of the variables of {rule[prev_i]} | {rule[next_i]} is true so the result is false.")
            rule[i] = result
            rule[prev_i] = " "
            rule[next_i] = " "
        rule = "".join(rule)
        return rule


    def treate_and_xor(self, rule):
        """Func to treat the and & xor operators. By default is one is true, all the other are false, if all are false but one, he is true."""
        rule = list(rule)
        indexes = [i for i, char in enumerate(rule) if char == "+" or char == '^']
        for i in indexes:
            result = '2'
            prev_i = i - 1
            next_i = i + 1
            while rule[prev_i] == ' ':
                prev_i -= 1
            while rule[next_i] == ' ':
                next_i += 1
            if rule[i] == '+':
                if rule[next_i] == '1' or rule[next_i] in self.facts:
                    if rule[prev_i] == '1' or rule[prev_i] in self.facts:
                        print(f"{rule[prev_i]} and {rule[next_i]} are both True so the result of '{rule[prev_i]} + {rule[next_i]}' is true.")
                        result = '1'
            else :
                if rule[next_i] == '1' or rule[next_i] in self.facts:
                    if rule[prev_i] != '1' and rule[prev_i] not in self.facts:
                        print(f"{rule[prev_i]} is False and {rule[next_i]} is True so the result of '{rule[prev_i]} ^ {rule[next_i]}' is true.")
                        result = '1'
                elif rule[next_i] != '1' and  rule[next_i] not in self.facts:
                    if rule[prev_i] == '1' or rule[prev_i] in self.facts:
                        print(f"{rule[prev_i]} is True and {rule[next_i]} is False so the result of '^' is true.")
                        result = '1'
            if result == '2':
                print(f"The conditions you can see above for the validation of '{rule[prev_i]} {rule[i]} {rule[next_i]}' arent validated so the result is false.")
            rule[i] = result
            rule[prev_i] = " "
            rule[next_i] = " "
        rule = "".join(rule)
        return rule
                        

    def treate_not(self, rule):
        """Func to treat the not condition."""
        rule = list(rule)
        indexes = [i for i, char in enumerate(rule) if char == "!"]
        for i in indexes:
            if rule[i + 1] not in self.facts:
                print(f"{rule[i + 1]} isnt in our facts so the condition {rule[i] + rule[i + 1]} is True.")
                rule[i + 1] = '1'
            else:
                print(f"{rule[i + 1]} is in our facts so the condition {rule[i] + rule[i + 1]} is False.")
                rule[i + 1] = '2'
            rule[i] = " "
        rule = "".join(rule)
        return rule


    def treat_parenthesis(self, rule):
        """Func to treat the parenthesis, she solve the parenthesis starting by the last found index and then suppress the parentheses once treated."""
        indexes = [i for i, char in enumerate(rule) if char == "("]
        indexes.reverse()
        for i in indexes:
            tmp_content = ''
            rule = rule[:i] + rule[i + 1:]
            while rule[i] != ')':
                tmp_content += rule[i]
                rule = rule[:i] + rule[i + 1:]
            rule = rule[:i] + rule[i + 1:]
            solved = self.solve_rule(tmp_content, 2)
            rule = rule[:i] + solved + ' ' + rule[i:]
        return rule

    def solve_rule(self, rule, conclude = 1):
        """Func to solve the rules, identifying the signs in the rule."""
        solved_rule = ''
        for i in rule:
            if i != '<' and i != '=':
                solved_rule += i
            else :
                break
        if '(' in rule:
            solved_rule = self.treat_parenthesis(solved_rule)
        if '!' in rule:
            solved_rule = self.treate_not(solved_rule)
        if '+' in rule or '^' in rule:
            solved_rule = self.treate_and_xor(solved_rule)
        if '|' in rule:
            solved_rule = self.treate_or(solved_rule)
        if not '2' in solved_rule and conclude == 1:
            solved_rule = self.conclude(rule)
        return solved_rule
 
    def find_values(self):
        """Func to find the value of each parameter with the given rules."""
        for rule in self.rules:
            print(f"\nEvaluating rule : {rule}")
            self.solve_rule(rule)

    def parse_input_file(self,nfile_path):
        """Open and parse the input file, returning the rules, initial_facts and queries."""
        rules = []
        initial_facts = []
        queries = []

        with open(file_path, "r") as file:
            for line in file:
                line = line.split('#')[0].strip()
                if not line:
                    continue

                if "=>" in line or "<=>" in line:
                    rules.append(line)

                elif line.startswith("="):
                    initial_facts = list(line[1:].strip()) 

                elif line.startswith("?"):
                    queries = list(line[1:].strip())

        self.rules = rules
        self.facts = initial_facts
        self.queries = queries
        self.false_facts = []
        self.or_facts = []


if __name__ == '__main__':
    try :
        file_path = argv[1]
    except Exception :
        exit("Please provide the filepath as your first arg.")
    expert = expert_system(file_path)

    print("Rules:", expert.rules)
    print("Initial Facts:", expert.facts)
    print("Queries:", expert.queries)