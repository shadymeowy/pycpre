from pycpre import process_file
import os
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog='pycpre', description='pycpre is a prepressor replacement written in Python for the C preprocessor.')
    parser.add_argument('-n', '--no-run', action='store_true', help='disable running the processed file')
    parser.add_argument('-o', '--output', help='output file')
    parser.add_argument('files', nargs='+', help='files to process')
    args = parser.parse_args()
    for file in args.files:
        if args.output is None:
            output = os.path.splitext(file)[0] + ".py"
        else:
            if len(args.files) > 1:
                raise Exception("Cannot specify output file when processing multiple files")
            output = args.output
        process_file(file, output)

    if not args.no_run:
        import subprocess, sys
        subprocess.call([sys.executable, output])


if __name__ == "__main__":
    main()
