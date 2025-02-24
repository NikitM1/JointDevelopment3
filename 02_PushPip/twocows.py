import argparse
import cowsay


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

picture1 = cowsay.cowsay(args.message1, cow=args.f, eyes=args.e, wrap_text=args.n)+'\n'
picture2 = cowsay.cowsay(args.message2, cow=args.F, eyes=args.E, wrap_text=args.N)+'\n'

lines1, lines2=picture1.split('\n'), picture2.split('\n')
len1, len2=map(len, [lines1, lines2])
maxlen1, maxlen2=max(map(len,lines1)), max(map(len,lines2))

lines1, lines2=[' '*maxlen1]*(len2-len1)+lines1, [' '*maxlen2]*(len1-len2)+lines2
for i in range(len1): print(lines1[i]+' '*(maxlen1-len(lines1[i]))+lines2[i])
