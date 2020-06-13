import enum
from token_parser import Token, TokenKind
from typing import List
from collections import deque


class NodeKind(enum.Enum):
	NUM = enum.auto()
	LVAR = enum.auto()  # ローカル変数
	ASSIGN = enum.auto()  # =
	ADD = enum.auto()
	SUB = enum.auto()
	MUL = enum.auto()
	DIV = enum.auto()
	EQ = enum.auto()
	NE = enum.auto()
	LT = enum.auto()
	LE = enum.auto()


class Node:
	def __init__(self, kind: NodeKind) -> None:
		self.kind: NodeKind = kind


class BinaryNode(Node):
	def __init__(self, kind: NodeKind, lhs: "Node", rhs: "Node") -> None:
		super().__init__(kind)
		self.lhs: Node = lhs
		self.rhs: Node = rhs

	def __eq__(self, other: "BinaryNode") -> bool:
		return (
				self.kind == other.kind
				and self.lhs == other.lhs
				and self.rhs == other.rhs
		)

	def __repr__(self) -> str:
		left = self.lhs.__repr__().replace("\n", "\n ")
		right = self.rhs.__repr__().replace("\n", "\n ")
		tree: str = f"({self.kind})\n"
		tree += f" {left}\n"
		tree += f" {right}"
		return tree


class NumNode(Node):
	def __init__(self, val: int) -> None:
		super().__init__(NodeKind.NUM)
		self.val: int = val

	def __eq__(self, other: "NumNode") -> bool:
		return self.val == other.val

	def __repr__(self) -> str:
		return str(self.val)


class LocalVarNode(Node):
	def __init__(self, offset: int) -> None:
		super().__init__(NodeKind.LVAR)
		self.offset: int = offset

	def __eq__(self, other: "LocalVarNode") -> bool:
		return self.offset == other.offset

	def __repr__(self) -> str:
		return f"[ebp - {self.offset:x}]"


def op_to_kind(op: str) -> NodeKind:
	if op == "+":
		return NodeKind.ADD
	elif op == "-":
		return NodeKind.SUB
	elif op == "*":
		return NodeKind.MUL
	elif op == "/":
		return NodeKind.DIV
	elif op == "==":
		return NodeKind.EQ
	elif op == "!=":
		return NodeKind.NE
	elif op == ">":
		return NodeKind.LT
	elif op == ">=":
		return NodeKind.LE


class NodeParser:
	def __init__(self, tokens: List[Token]):
		self.tokens: deque[Token] = deque(tokens)
		self.code: List[Node] = []

	@staticmethod
	def token_to_num(token: Token) -> int:
		return int(token.string)

	def next(self) -> None:
		self.tokens.popleft()

	# program = stmt*
	# stmt = expr ";"
	# expr = assign
	# assign = equality ("=" assign)?
	# equality = relational (("==" | "!=") relational)*
	# relational = add (("<" | "<=" | ">" | ">=") add)*
	# add = mul (("+" | "-") mul)*
	# mul = unary (("*" | "/") unary)*
	# unary = ("+" | "-")? primary
	# primary = num | ident | ("(" expr ")")

	def program(self) -> List[Node]:
		while self.tokens[0].kind != TokenKind.EOF:
			self.code.append(self.stmt())
		return self.code

	def stmt(self) -> Node:
		node: Node = self.expr()
		if self.tokens[0].string == ";":
			self.next()
		return node

	def expr(self) -> Node:
		return self.assign()

	def assign(self) -> Node:
		node: Node = self.equality()
		if self.tokens[0].string == "=":
			kind = NodeKind.ASSIGN
			self.next()
			node = BinaryNode(kind, node, self.assign())
		return node

	def equality(self) -> Node:
		node: Node = self.relational()
		for _ in range(len(self.tokens)):
			if self.tokens[0].string in ["==", "!="]:
				op: str = self.tokens[0].string
				self.next()
				kind: NodeKind = op_to_kind(op)
				node = BinaryNode(kind, node, self.relational())
			else:
				return node
		return node

	def relational(self) -> Node:
		node: Node = self.add()
		for _ in range(len(self.tokens)):
			if self.tokens[0].string in [">", ">="]:
				op: str = self.tokens[0].string.replace("<", ">")
				self.next()
				kind: NodeKind = op_to_kind(op)
				node = BinaryNode(kind, self.add(), node)
			elif self.tokens[0].string in ["<", "<="]:
				op: str = self.tokens[0].string.replace("<", ">")
				self.next()
				kind: NodeKind = op_to_kind(op)
				node = BinaryNode(kind, node, self.add())
			else:
				return node
		return node

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
			node: Node = self.expr()
			self.next()
		else:
			if self.tokens[0].kind == TokenKind.NUM:
				num: int = self.token_to_num(self.tokens[0])
				self.next()
				node = NumNode(num)
			elif self.tokens[0].kind == TokenKind.IDENT:
				name: str = self.tokens[0].string
				offset: int = (ord(name) - ord("a") + 1) * 8
				self.next()
				node = LocalVarNode(offset)
			else:
				# TODO: impl error
				print(self.tokens)
				raise Exception()
		return node


def node_parse(tokens: List[Token]) -> List[Node]:
	parser: NodeParser = NodeParser(tokens)
	return parser.program()
