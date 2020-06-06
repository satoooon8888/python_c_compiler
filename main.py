import sys
from token_parser import tokenize


def main() -> None:
	source = sys.argv[1]
	tokens = tokenize(source)


main()
