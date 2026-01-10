import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while(True):
        sys.stdout.write("$ ")
        command = input()
        word_list = command.split()
        first_word = word_list[0]
        word_list.pop(0)

        match first_word:
            case 'echo':
                string_to_print = ' '.join(word_list)
                print(string_to_print)
            case 'exit':
                break
            case _:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
