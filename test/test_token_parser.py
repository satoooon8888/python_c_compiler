
from token_parser import *


def test_parser():
	result = [
		Token(TokenKind.NUM, "1"),
		Token(TokenKind.RESERVED, "+"),
		Token(TokenKind.NUM, "2"),
		Token(TokenKind.EOF, "")
	]
	assert Token(TokenKind.NUM, "1") == Token(TokenKind.NUM, "1")
	assert tokenize("1 + 2") == result
