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

def op_to_kind(op: str) -> NodeKind:
	if op == "+":
		return NodeKind.ADD
	elif op == "-":
		return NodeKind.SUB
	elif op == "*":
		return NodeKind.MUL
	elif op == "/":
		return NodeKind.DIV


class NodeParser:
	def __init__(self, tokens: List[Token]):
		self.tokens: deque[Token] = deque(tokens)

	@staticmethod
	def token_to_num(token: Token) -> int:
		return int(token.string)

	def next(self) -> None:
		self.tokens.popleft()

	def expr(self) -> Node:
		return self.add()

	def add(self) -> Node:
		node: Node = self.mul()
		for _ in range(len(self.tokens)):
			if self.tokens[0].string in ["+", "-"]:
				op: str = self.tokens[0].string
				self.next()
				kind: NodeKind = op_to_kind(op)
				node = BinaryNode(kind, node, self.mul())
			else:
				return node
		return node

	def mul(self) -> Node:
		node: Node = self.unary()
		for _ in range(len(self.tokens)):
			if self.tokens[0].string in ["*", "/"]:
				op: str = self.tokens[0].string
				self.next()
				kind: NodeKind = op_to_kind(op)
				node = BinaryNode(kind, node, self.unary())
			else:
				return node
		return node

	def unary(self) -> Node:
		if self.tokens[0].string == "-":
			self.next()
			kind = NodeKind.SUB
			node = BinaryNode(kind, NumNode(0), self.primary())
			return node
		if self.tokens[0].string == "+":
			self.next()
		node: Node = self.primary()
		return node

	def primary(self) -> Node:
		if self.tokens[0].string == "(":
			self.next()
			node = self.expr()
			self.next()
		else:
			num = self.token_to_num(self.tokens[0])
			self.next()
			node = NumNode(num)
		return node


def node_parse(tokens: List[Token]) -> Node:
	parser: NodeParser = NodeParser(tokens)
	return parser.expr()
