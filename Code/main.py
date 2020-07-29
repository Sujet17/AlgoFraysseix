
from time_measure import test_time
from gui import App
import argparse


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", "--display", action='store_true', help='Open a tkinter app that displays the straight line '
                                                                'drawing of the specified graphs')
group.add_argument("-p", "--plot", action="store_true", help='Execute the shift-algorithm on the specified graphs and '
                                                             'plot the execution times')
parser.add_argument('filenames', nargs='+', help="The list of files that contains the graphs that will be treated")


if __name__ == "__main__":

    args = parser.parse_args()
    file_names = ['graph_examples/' + filename for filename in args.filenames[1:]]
    if args.display:
        app = App(file_names)
    elif args.plot:
        test_time(file_names)

