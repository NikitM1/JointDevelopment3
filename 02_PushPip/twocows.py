import argparse
import os
import sys


parser = argparse.ArgumentParser(
    description="Generates an image of two cows saying the given text"
)

parser.add_argument(
    "-e",
    type=str,
    help="First cow's eyes string. This is ignored if a preset mode is given",
    default='oo'
)
parser.add_argument(
    "-f", 
    type=str, 
    help="Animal for the first 'cow'"
)
parser.add_argument(
    "-n",
    help="First cow's speech wrapped"
)
parser.add_argument(
    "-E",
    type=str,
    help="Second cow's eyes string. This is ignored if a preset mode is given",
    default='oo'
)
parser.add_argument(
    "-F", 
    type=str, 
    help="Animal for the second 'cow'"
)
parser.add_argument(
    "-N",
    help="First cow's speech wrapped"
)
parser.add_argument(
    "message1", 
    default=None, 
    help="First cow's speech"
)
parser.add_argument(
    "message2", 
    default=None, 
    help="Second cow's speech"
)

args = parser.parse_args()