from gui import AppMatplotlib
from gui_tkinter import AppTk
from load_graph import load_embedding_lst
import argparse


class MyParser(argparse.ArgumentParser):
    def __init__(self, msg_title: str):
        argparse.ArgumentParser.__init__(self, msg_title)
        self.add_argument('-m', '--min', type=int,
                          help='Specify the minimum size of the graphs treated. The too little graphs are ignored.')

        self.add_argument('-M', '--max', type=int,
                          help='Specify the maximum size of the graphs treated. The too big graphs are ignored.')

        self.add_argument('files', type=str, nargs='+',
                          help='The list of files that contains the graphs that will be treated.')


if __name__ == "__main__":
    parser = MyParser('Open a matplotlib window that displays the straight line drawing of the specified graphs.')

    parser.add_argument("-t", "--tk", action="store_true",
                        help='Execute a tkinter window that displays the straight line drawing of the specified graphs.'
                             'The drawing is less pretty than with matplotlib but faster.')

    args = parser.parse_args()
    graph_list = load_embedding_lst(args.files, args.min, args.max)
    if len(graph_list) == 0:
        print("There is no graph to display")
    elif args.tk:
        app = AppTk(graph_list)
    else:
        app = AppMatplotlib(graph_list)
