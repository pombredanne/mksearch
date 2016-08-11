'''
    Main entry
'''
from __future__ import absolute_import
import argparse
from makefile_parser.modules.manager import Manager


def menu():
    '''
    The Menu is here
    '''
    parser = argparse.ArgumentParser(
        description='makefile_parser')
    parser.add_argument('-p',
                        action="store",
                        dest="path",
                        help='base path to scan files')
    parser.add_argument('-e',
                        action="store_true",
                        dest="execute",
                        default=False,
                        help='execute the values')
    parser.add_argument('-d',
                        action="store_true",
                        dest="debug",
                        default=False,
                        help='execute the values')
    parser.add_argument('-i',
                    action='append',
                    dest="include",
                    default=['Makefile'],
                    help='include files or directories')
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 1.0')
    return parser.parse_args()

def main():
    '''
    This is used in the cli and from a couple places
    '''
    options = menu()
    if options.path:
        m1 = Manager(options)
if __name__ == '__main__':
    main()