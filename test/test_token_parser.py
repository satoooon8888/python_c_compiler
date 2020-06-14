from token_parser import *


def test_parser():
	assert Token(TokenKind.NUM, "1", 0, 0) == Token(TokenKind.NUM, "1", 0, 0)
	testing = "1 + 2"
	result = [
		Token(TokenKind.NUM, "1", 0, 0),
		Token(TokenKind.RESERVED, "+", 0, 2),
		Token(TokenKind.NUM, "2", 0, 4),
		Token(TokenKind.EOF, "", 0, 5)
	]
	assert tokenize(testing) == result

	testing = "a + 2"
	result = [
		Token(TokenKind.IDENT, "a", 0, 0),
		Token(TokenKind.RESERVED, "+", 0, 2),
		Token(TokenKind.NUM, "2", 0, 4),
		Token(TokenKind.EOF, "", 0, 5)
	]
	assert tokenize(testing) == result

	testing = "a = 1"
	result = [
		Token(TokenKind.IDENT, "a", 0, 0),
		Token(TokenKind.RESERVED, "=", 0, 2),
		Token(TokenKind.NUM, "1", 0, 4),
		Token(TokenKind.EOF, "", 0, 5)
	]
	assert tokenize(testing) == result

	testing = "a = 1; a"
	result = [
		Token(TokenKind.IDENT, "a", 0, 0),
		Token(TokenKind.RESERVED, "=", 0, 2),
		Token(TokenKind.NUM, "1", 0, 4),
		Token(TokenKind.RESERVED, ";", 0, 5),
		Token(TokenKind.IDENT, "a", 0, 7),
		Token(TokenKind.EOF, "", 0, 8)
	]
	assert tokenize(testing) == result
