import argparse
import os
import sys


parser = argparse.ArgumentParser(
    prog=os.path.basename(sys.argv[0]),
    description="Generates an ASCII image of a cow saying the given text",
)

parser.add_argument(
    "-e",
    type=str,
    help="An eye string. This is ignored if a preset mode is given",
    dest="eyes",
    default=Option.eyes,
    metavar="eye_string",
)
parser.add_argument(
    "-f", type=str, metavar="cowfile",
    help="Either the name of a cow specified in the COWPATH, "
         "or a path to a cowfile (if provided as a path, the path must "
         "contain at least one path separator)",
)
parser.add_argument(
    "-n", action="store_false",
    help="If given, text in the speech bubble will not be wrapped"
)