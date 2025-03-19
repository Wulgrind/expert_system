from main import expert_system

if __name__ == '__main__':
    choice_list = []
    paths = {
        1 : 'example_and.txt',
        2 : 'example_not.txt',
        3 : 'example_or.txt',
        4 : 'example_xor.txt',
        5 : 'example_parenthesis.txt',
        6 : 'example_all.txt',
    }
    choice = input("What tests do you want to perform ?\n1 : '+'\n2 : '!'\n3 : '|'\n4 : '^'\n5 : '()'\n6 : All\n")
    for i in range(7):
        if str(i) in choice:
            choice_list.append(i)
    for path in choice_list:
        print(f"\033[92m\nTESTING {paths[path]}\n\033[0m")
        expert_system('src/' + paths[path])
