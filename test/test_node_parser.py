from node_parser import *
from token_parser import tokenize


def test_node_parser():
	assert NumNode(1) == NumNode(1)
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
	assert node_parse(testing) == result
