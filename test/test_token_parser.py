from token_parser import *


def test_parser():
	assert Token(TokenKind.NUM, "1", 0) == Token(TokenKind.NUM, "1", 0)
	testing = "1 + 2;"
	result = [
		Token(TokenKind.NUM, "1", 0),
		Token(TokenKind.RESERVED, "+", 2),
		Token(TokenKind.NUM, "2", 4),
		Token(TokenKind.RESERVED, ";", 5),
		Token(TokenKind.EOF, "", 6)
	]
	assert tokenize(testing) == result

	testing = "a + 2;"
	result = [
		Token(TokenKind.IDENT, "a", 0),
		Token(TokenKind.RESERVED, "+", 2),
		Token(TokenKind.NUM, "2", 4),
		Token(TokenKind.RESERVED, ";", 5),
		Token(TokenKind.EOF, "", 6)
	]
	assert tokenize(testing) == result

	testing = "a = 1;"
	result = [
		Token(TokenKind.IDENT, "a", 0),
		Token(TokenKind.RESERVED, "=", 2),
		Token(TokenKind.NUM, "1", 4),
		Token(TokenKind.RESERVED, ";", 5),
		Token(TokenKind.EOF, "", 6)
	]
	assert tokenize(testing) == result

	testing = "a = 1; a;"
	result = [
		Token(TokenKind.IDENT, "a", 0),
		Token(TokenKind.RESERVED, "=", 2),
		Token(TokenKind.NUM, "1", 4),
		Token(TokenKind.RESERVED, ";", 5),
		Token(TokenKind.IDENT, "a", 7),
		Token(TokenKind.RESERVED, ";", 8),
		Token(TokenKind.EOF, "", 9)
	]
	assert tokenize(testing) == result
