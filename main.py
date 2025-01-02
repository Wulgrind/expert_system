from sys import argv

### Must have queries and rules
### Check if rule contradict a fact on any other rule.
class expert_system:

    def __init__(self, file_path):
        self.file_path = file_path 
        self.parse_input_file(file_path)
        self.find_values()


    def check_or_facts(self, fact):
        delete_list = []
        for i in self.or_facts:
            if fact in i :
                i.remove(fact)
                if len(i) == 1:
                    if len(i[0] > 1):
                        self.false_facts.append(i[0])
                    else:
                        self.facts.append(i[0])
                    delete_list.append(i)
        for i in delete_list:
            self.or_facts.remove(i)


    def conclude(self, solved_rule, rule):
        index = solved_rule.find(">")
        neg = 0
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
                                if solved_rule[index] in self.facts:
                                    print(f"Rule '{rule}' contradict another rule, saying that {solved_rule[index]} is false. This rule will be ignored")
                                elif solved_rule[index] not in self.false_facts:
                                    self.false_facts.append(solved_rule[index])
                                self.check_or_facts(solved_rule[index])
                            else :
                                if solved_rule[index] in self.false_facts:
                                    print(f"Rule '{rule}' contradict another rule, saying that {solved_rule[index]} is true. This rule will be ignored")
                                elif solved_rule[index] not in self.facts:
                                    self.facts.append(solved_rule[index])
                                self.check_or_facts('!' + solved_rule[index])
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
                if len(tmp_list) >= 2:
                    self.or_facts.append(tmp_list)
                elif len(tmp_list) == 1:
                    if len(tmp_list[0]) > 1:
                        self.false_facts.append(tmp_list[0])
                    else :
                        self.facts.append(tmp_list[0])
            elif '^' in solved_rule:
            else:
                while index < len(solved_rule) - 1:
                    index += 1
                    neg = 0
                    if solved_rule[index] != ' ':
                        if solved_rule[index] == '!':
                            neg = 1
                        else :
                            if neg == 1:
                                if solved_rule[index] in self.facts:
                                    print(f"Rule '{rule}' contradict another rule, saying that {solved_rule[index]} is false. This rule will be ignored")
                                else :
                                    self.false_facts.append(solved_rule[index])
                                    self.check_or_facts(solved_rule[index])
                            elif neg == 0:
                                if solved_rule[index] in self.false_facts:
                                    print(f"Rule '{rule}' contradict another rule, saying that {solved_rule[index]} is true. This rule will be ignored")
                                else:
                                    self.facts.append(solved_rule[index])
                                    self.check_or_facts('!' + solved_rule(index))
                            

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
            if rule[prev_i] == '1' or rule[prev_i] in self.facts or rule[next_i] == '1' or rule[next_i] in self.facts:
                result = '1'
            rule[i] = result
            del rule[prev_i]
            del rule[next_i - 1]
            rule = "".join(rule)
            return rule


    def treate_and_xor(self, rule):
        """Func to treat the and & xor operators."""
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
                        result = '1'
            else :
                if rule[next_i] == '1' or rule[next_i] in self.facts:
                    if rule[prev_i] != '1' and rule[prev_i] not in self.facts:
                        result = '1'
                elif rule[next_i] != '1' and  rule[next_i] not in self.facts:
                    if rule[prev_i] == '1' or rule[prev_i] in self.facts:
                        result = '1'
            rule[i] = result
            del rule[prev_i]
            del rule[next_i - 1]
            rule = "".join(rule)
            return rule
                        

    def treate_not(self, rule):
        """Func to treat the not condition."""
        rule = list(rule)
        indexes = [i for i, char in enumerate(rule) if char == "!"]
        for i in indexes:
            rule[i + 1] = '1' if rule[i + 1] not in self.facts else '2'
            del rule[i]
        rule = "".join(rule)
        return rule


    def treat_parenthesis(self, rule):
        """Func to treat the parenthesis, she solve the parenthesis starting by the last found index and then suppress the parentheses once treated."""
        indexes = [i for i, char in enumerate(rule) if char == "("]
        indexes.reverse()
        tmp_content= ''
        for i in indexes:
            rule = rule[i] + rule[i + 1:]
            while rule[i] != ')':
                tmp_content += rule[i]
                rule = rule[i] + rule[i + 1:]
            rule = rule[i] + rule[i + 1:]
            solved = self.solve_rule(tmp_content)
            rule = rule[i] + solved + ' ' + rule[i + 1:]
        return rule

    def solve_rule(self, rule):
        """Func to solve the rules, identifying the signs in the rule."""
        solved_rule = ''
        if '(' in rule:
            solved_rule = self.treat_parenthesis(rule)
        if '!' in rule:
            solved_rule = self.treate_not(rule)
        if '+' in rule or '^' in rule:
            solved_rule = self.treate_and_xor(rule)
        if '|' in rule:
            solved_rule = self.treate_or(rule)
        if not '2' in solved_rule :
            solved_rule = self.conclude(solved_rule , rule)
        return solved_rule
        


    def find_values(self):
        """Func to find the value of each parameter with the given rules."""
        solved_values = []
        for rule in self.rules:
            solved_values.append(self.solve_rule(rule))
        for i in self.queries:
            if i in self.facts:
                print(f"{i} is True.")
            else:
                print(f"{i} is False.")


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