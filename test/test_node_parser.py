from node_parser import *
from token_parser import tokenize


def test_node_parser():
	null_token: Token = Token(TokenKind.INVALID, "", 0)
	assert NumNode(1, null_token) == NumNode(1, null_token)
	assert LocalVarNode(0, null_token) == LocalVarNode(0, null_token)
	assert BinaryNode(NodeKind.ADD, null_token, NumNode(0, null_token), NumNode(0, null_token)) \
		== BinaryNode(NodeKind.ADD, null_token, NumNode(0, null_token), NumNode(0, null_token))
	source = "2 * (3 - 1) + -2"
	testing = tokenize(source)
	result = [BinaryNode(
		NodeKind.ADD,
		Token(TokenKind.RESERVED, "+", 12),
		BinaryNode(
			NodeKind.MUL,
			Token(TokenKind.RESERVED, "*", 2),
			NumNode(2, Token(TokenKind.NUM, "2", 0)),
			BinaryNode(
				NodeKind.SUB,
				Token(TokenKind.RESERVED, "-", 7),
				NumNode(3, Token(TokenKind.NUM, "3", 5)),
				NumNode(1, Token(TokenKind.NUM, "1", 9)),
			),
		),
		BinaryNode(
			NodeKind.SUB,
			Token(TokenKind.RESERVED, "-", 14),
			NumNode(0, Token(TokenKind.RESERVED, "-", 14)),
			NumNode(2, Token(TokenKind.NUM, "2", 15)),
		),
	)]
	assert node_parse(testing, source).nodes == result

	source = "a = 1"
	testing = tokenize(source)
	result = [BinaryNode(
		NodeKind.ASSIGN,
		Token(TokenKind.RESERVED, "=", 2),
		LocalVarNode(8, Token(TokenKind.IDENT, "a", 0)),
		NumNode(1, Token(TokenKind.NUM, "1", 4))
	)]
	assert node_parse(testing, source).nodes == result

	source = "a = 1; a"
	testing = tokenize(source)
	result = [
		BinaryNode(
			NodeKind.ASSIGN,
			Token(TokenKind.RESERVED, "=", 2),
			LocalVarNode(8, Token(TokenKind.IDENT, "a", 0)),
			NumNode(1, Token(TokenKind.NUM, "1", 4))
		),
		LocalVarNode(8, Token(TokenKind.IDENT, "a", 7))
	]
	assert node_parse(testing, source).nodes == result
