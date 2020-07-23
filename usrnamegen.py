"""
UsrNameGen by yvantitov
Generates permutations of given names for username brute forcing
TODO: Figure out middle name support
TODO: Dynamic format loading
TODO: Verbosity
"""

import re
import argparse


class OutputHandler:
    def __init__(self, outfile_name=""):
        if outfile_name:
            self.outfile = open(outfile_name, 'a')

    def print(self, output):
        if hasattr(self, "outfile"):
            self.outfile.write(output + "\n")
        else:
            print(output)


class NameFormatter:
    def __init__(self, name, output_handler, format_list):
        self.name = name.lower().split()
        self.output_handler = output_handler
        self.format_list = format_list

    def print_variants(self):
        for fmt in self.format_list:
            name_out = fmt

            first = self.name[0]
            last = ""
            if len(self.name) > 1:
                last = self.name[-1]

            # replace format strings with new values
            name_out = name_out.replace("{first}", first)
            name_out = name_out.replace("{First}", first.capitalize())
            name_out = name_out.replace("{f}", first[0])
            name_out = name_out.replace("{F}", first[0].capitalize())

            if last:
                name_out = name_out.replace("{last}", last)
                name_out = name_out.replace("{Last}", last.capitalize())
                name_out = name_out.replace("{l}", last[0])
                name_out = name_out.replace("{L}", last[0].capitalize())
            else:
                name_out = re.sub(r"{last}|{Last}|{l}|{L}", "", name_out)

            self.output_handler.print(name_out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", dest="output", help="specify a file where output will go (default is stdout)")
    parser.add_argument("names", help="a list of proper names from which to derive usernames")
    parser.add_argument("formats", help="a file with username formats")
    args = parser.parse_args()
    try:
        # infile
        in_file = open(args.names, "r", -1)
        # fmt file + list
        fmt_file = open(args.formats, "r", -1)
        fmt_list = fmt_file.read().splitlines()
        # outfile (if provided)
        output_handler = OutputHandler(args.output)
        # main loop
        while True:
            name = in_file.readline()
            if name:
                if not name.isspace():
                    name_obj = NameFormatter(name, output_handler, fmt_list)
                    name_obj.print_variants()
            else:
                break
    except FileNotFoundError as io_err:
        print("Could not find file", io_err.filename, "->", io_err.strerror)
    except OSError as os_err:
        print("OS error ->", os_err.strerror)


if __name__ == "__main__":
    main()
