import enum
from token_parser import Token
from typing import List
from collections import deque


class NodeKind(enum.Enum):
	NUM = enum.auto()
	ADD = enum.auto()
	SUB = enum.auto()
	MUL = enum.auto()
	DIV = enum.auto()


class Node:
	def __init__(self, kind: NodeKind):
		self.kind: NodeKind = kind


class BinaryNode(Node):
	def __init__(self, kind: NodeKind, lhs: "Node", rhs: "Node"):
		super().__init__(kind)
		self.lhs: Node = lhs
		self.rhs: Node = rhs

	def __repr__(self) -> str:
		left = self.lhs.__repr__().replace("\n", "\n ")
		right = self.rhs.__repr__().replace("\n", "\n ")
		tree: str = f"({self.kind})\n"
		tree += f" {left}\n"
		tree += f" {right}"
		return tree


class NumNode(Node):
	def __init__(self, val: int):
		super().__init__(NodeKind.NUM)
		self.val: int = val

	def __repr__(self):
		return str(self.val)


# expr = add
# add = mul (("+" | "-") mul)*
# mul = unary (("*" | "/") unary)*
# unary = ("+" | "-")? primary
# primary = num | ("(" expr ")")

class NodeParser:
	def __init__(self, tokens: List[Token]):
		self.tokens: deque[Token] = deque(tokens)

	@staticmethod
	def token_to_num(token: Token):
		return int(token.string)

	def expr(self) -> Node:
		return self.add()

	def add(self) -> Node:
		node: Node = self.mul()
		for _ in range(len(self.tokens)):
			token: Token = self.tokens.popleft()
			if token.string == "+":
				kind = NodeKind.ADD
				node = BinaryNode(kind, node, self.mul())
			elif token.string == "-":
				kind = NodeKind.SUB
				node = BinaryNode(kind, node, self.mul())
			else:
				self.tokens.appendleft(token)
				return node
		return node

	def mul(self) -> Node:
		token: Token = self.tokens.popleft()
		node: Node = NumNode(self.token_to_num(token))
		for _ in range(len(self.tokens)):
			token = self.tokens.popleft()
			if token.string == "*":
				token = self.tokens.popleft()
				kind = NodeKind.MUL
				num = self.token_to_num(token)
				node = BinaryNode(kind, node, NumNode(num))
			elif token.string == "/":
				token = self.tokens.popleft()
				kind = NodeKind.DIV
				num = self.token_to_num(token)
				node = BinaryNode(kind, node, NumNode(num))
			else:
				self.tokens.appendleft(token)
				return node
		return node


def node_parse(tokens: List[Token]) -> Node:
	parser: NodeParser = NodeParser(tokens)
	return parser.expr()
