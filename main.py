import sys
from token_parser import tokenize
from node_parser import node_parse
from asm_gen import asm_gen


def compile_source(source: str) -> str:
	tokens = tokenize(source)
	function = node_parse(tokens, source)
	return asm_gen([function], source)


def main() -> None:
	source = sys.argv[1]
	print(compile_source(source))


if __name__ == '__main__':
	main()
