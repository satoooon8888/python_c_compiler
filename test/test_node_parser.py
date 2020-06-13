from node_parser import *
from token_parser import tokenize


def test_node_parser():
	assert NumNode(1) == NumNode(1)
	assert LocalVarNode(0) == LocalVarNode(0)
	assert BinaryNode(NodeKind.ADD, NumNode(0), NumNode(0)) == BinaryNode(NodeKind.ADD, NumNode(0), NumNode(0))
	testing = tokenize("2 * (3 - 1) + -2")
	result = BinaryNode(
		NodeKind.ADD,
		BinaryNode(
			NodeKind.MUL,
			NumNode(2),
			BinaryNode(
				NodeKind.SUB,
				NumNode(3),
				NumNode(1)
			)
		),
		BinaryNode(
			NodeKind.SUB,
			NumNode(0),
			NumNode(2)
		)
	)
	assert node_parse(testing)[0] == result

	testing = tokenize("a = 1")
	result = BinaryNode(
		NodeKind.ASSIGN,
		LocalVarNode(8),
		NumNode(1)
	)
	assert node_parse(testing)[0] == result

	testing = tokenize("a = 1; a")
	result = [
		BinaryNode(
			NodeKind.ASSIGN,
			LocalVarNode(8),
			NumNode(1)
		),
		LocalVarNode(8)
	]
	assert node_parse(testing) == result
