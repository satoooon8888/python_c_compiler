from token_parser import *


def test_parser():
	assert Token(TokenKind.NUM, "1") == Token(TokenKind.NUM, "1")
	testing = "1 + 2"
	result = [
		Token(TokenKind.NUM, "1"),
		Token(TokenKind.RESERVED, "+"),
		Token(TokenKind.NUM, "2"),
		Token(TokenKind.EOF, "")
	]
	assert tokenize(testing) == result

	testing = "a + 2"
	result = [
		Token(TokenKind.IDENT, "a"),
		Token(TokenKind.RESERVED, "+"),
		Token(TokenKind.NUM, "2"),
		Token(TokenKind.EOF, "")
	]
	assert tokenize(testing) == result

	testing = "a = 1"
	result = [
		Token(TokenKind.IDENT, "a"),
		Token(TokenKind.RESERVED, "="),
		Token(TokenKind.NUM, "1"),
		Token(TokenKind.EOF, "")
	]
	assert tokenize(testing) == result