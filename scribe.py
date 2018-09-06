#!/usr/bin/env python3
import argparse
import sys
from transcribe.render import transcribe
from transcribe.lib.util import check_file

_default_scribe_type = 'stockpile'
_default_input_path = '/tmp/stockpile.json'


def main():
    parser = argparse.ArgumentParser(prog='scribe', usage='%(prog)s [options]')
    parser.add_argument(
        '-t', '--scribe-type', dest="type", nargs='?', choices=['stockpile'],
        default=_default_scribe_type,
        help='Type of data scribe would work with. Example: Stockpile, Foo..\
        Defaults to /{}'.format(_default_scribe_type)
    )
    parser.add_argument(
        '-ip', '--input-path', dest="input_path", nargs='?',
        default=_default_input_path,
        help='path for input-data. Defaults to /{}'.format(_default_input_path)
    )
    input_args = parser.parse_args()
    if input_args.input_path:
        input_data_path = input_args.input_path
    check_file(input_data_path)
    if input_args.type:
        scribe_type = input_args.type
    for scribed_doc in transcribe(input_data_path, scribe_type):
        print(scribed_doc)


if __name__ == '__main__':
    sys.exit(main())
