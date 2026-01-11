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
            'exit': lambda x: x
        }

        match first_word:
            case 'echo':
                arguments = ' '.join(word_list)
                print(arguments)
            case 'type':
                arguments = ' '.join(word_list)
                if(arguments in command_map.keys()):
                    print(f'{arguments} is a shell builtin')
                else:
                    print(f'{arguments}: not found')
            case 'exit':
                break
            case _:
                print(f"{command}: command not found")

def echo_handler(word_list: list[str]):
    print(' '.join(word_list))

def type_handler(word_list:list[str], command_map: dict):
    arguments = ' '.join(word_list)
    if(arguments in command_map.keys):
        print(f'{arguments} is a shell builtin')
    else:
        print(f'{arguments}: not found')

if __name__ == "__main__":
    main()
