import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while(True):
        sys.stdout.write("$ ")
        command = input()
        word_list = command.split()
        first_word = word_list[0]
        word_list.pop(0)

        command_map = {
            'echo': echo_handler,
            'type': type_handler,
            'exit': lambda x, y: 'EXIT'
        }

        if first_word in command_map:
            result = command_map[first_word](word_list, command_map)
            if(result == 'EXIT'): 
                break
        else:
            print(f"{command}: command not found")
                
def echo_handler(word_list: list[str], context):
    print(' '.join(word_list))

def type_handler(word_list:list[str], command_map: dict):
    arguments = ' '.join(word_list)
    if(arguments in command_map):
        print(f'{arguments} is a shell builtin')
    else:
        print(f'{arguments}: not found')

if __name__ == "__main__":
    main()
