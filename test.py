import argparse
def main(argv = None): 
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--add', nargs=2, type=str, help = 'enter name and deadline to add task to the list')

    parser.add_argument('-s', '--swap', nargs=2, type=int, help = 'swap the order of two tasks')

    parser.add_argument('--top', nargs=1, type=int, help = 'move task to top of the list')

    parser.add_argument('-d', '--del', nargs='+', type=int, help = 'delete tasks from the list')

    args = parser.parse_args(argv) 
    print(dir(args))
    breakpoint()

main()
