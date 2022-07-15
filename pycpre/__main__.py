from re import sub
from pycpre import process_file
import os
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog='pycpre', description='pycpre is a prepressor replacement written in Python for the C preprocessor.')
    parser.add_argument('-n', '--no-run', action='store_true', help='disable running the processed file')
    parser.add_argument('-o', '--output', help='output file')
    parser.add_argument('-r', '--remove', action='store_true', help='remove the .py files after running')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('-i', '--no-import', action='store_true', help='disable auto-importing pycpre')
    parser.add_argument('-c', '--curly', action='store_true', help='enable curly brackets parsing for Python')
    parser.add_argument('files', nargs='+', help='files to process')
    args = parser.parse_args()
    for file in args.files:
        if args.output is None:
            output = os.path.splitext(file)[0] + ".py"
        else:
            if len(args.files) > 1:
                raise Exception("Cannot specify output file when processing multiple files")
            output = args.output
        process_file(file, output, auto_import=not args.no_import, curl=args.curly)

    if not args.no_run:
        import subprocess, sys
        subprocess.call([sys.executable, output])
        if args.remove:
            subprocess.call(['rm', output])


if __name__ == "__main__":
    main()
