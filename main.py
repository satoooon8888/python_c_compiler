import sys
from token_parser import tokenize
from node_parser import node_parse
from asm_gen import code_gen


def main() -> None:
	source = sys.argv[1]
	tokens = tokenize(source)
	node = node_parse(tokens)
	print(code_gen(node))


main()
