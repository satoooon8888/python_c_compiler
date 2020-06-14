import sys
from token_parser import tokenize
from node_parser import node_parse
from asm_gen import code_gen


def gen_asm(source: str) -> str:
	tokens = tokenize(source)
	nodes = node_parse(tokens, source)
	return code_gen(nodes)


def main() -> None:
	source = sys.argv[1]
	print(gen_asm(source))


if __name__ == '__main__':
	main()
