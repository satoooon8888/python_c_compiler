import enum
from token_parser import Token, TokenKind, error_token
from typing import List, Dict, Optional
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
	RETURN = enum.auto()
	IF = enum.auto()
	WHILE = enum.auto()
	FOR = enum.auto()


class Node:
	def __init__(self, kind: NodeKind, token: Token) -> None:
		self.kind: NodeKind = kind
		self.token: Token = token


class BinaryNode(Node):
	def __init__(self, kind: NodeKind, token: Token, lhs: "Node", rhs: "Node") -> None:
		super().__init__(kind, token)
		self.lhs: Node = lhs
		self.rhs: Node = rhs

	def __eq__(self, other: "BinaryNode") -> bool:
		return self.__dict__ == other.__dict__

	def __repr__(self) -> str:
		left = self.lhs.__repr__().replace("\n", "\n ")
		right = self.rhs.__repr__().replace("\n", "\n ")
		tree: str = f"({self.kind}) {self.token}\n"
		tree += f" {left}\n"
		tree += f" {right}"
		return tree


class NumNode(Node):
	def __init__(self, val: int, token: Token) -> None:
		super().__init__(NodeKind.NUM, token)
		self.val: int = val

	def __eq__(self, other: "NumNode") -> bool:
		return self.__dict__ == other.__dict__

	def __repr__(self) -> str:
		return f"{self.val} {self.token}"


class LocalVarNode(Node):
	def __init__(self, offset: int, token: Token) -> None:
		super().__init__(NodeKind.LVAR, token)
		self.offset: int = offset

	def __eq__(self, other: "LocalVarNode") -> bool:
		return self.__dict__ == other.__dict__

	def __repr__(self) -> str:
		return f"[ebp - {self.offset:x}] {self.token}"


class ReturnNode(Node):
	def __init__(self, token: Token, value: Node):
		super().__init__(NodeKind.RETURN, token)
		self.value = value

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def __repr__(self) -> str:
		tree: str = f"({self.kind}) {self.token}"
		tree += f" {self.value}"
		return tree


class IfNode(Node):
	def __init__(self, token: Token, conditions: Node, if_node: Node, else_node: Optional[Node]) -> None:
		super().__init__(NodeKind.IF, token)
		self.conditions = conditions
		self.if_node: Node = if_node
		self.else_node: Optional[Node] = else_node
		self.token: Token = token

	def __eq__(self, other: "LocalVarNode") -> bool:
		return self.__dict__ == other.__dict__

	def __repr__(self) -> str:
		conditions = self.if_node.__repr__().replace("\n", "\n ")
		if_node = self.if_node.__repr__().replace("\n", "\n ")
		tree: str = ""
		tree += f"{self.token}"
		tree += f"IF (\n"
		tree += f" {conditions}\n"
		tree += ")\n"
		tree += f" {if_node}\n"
		if self.else_node is not None:
			else_node = self.else_node.__repr__().replace("\n", "\n ")
			tree += f"ELSE"
			tree += f" {else_node}"
		return tree


class WhileNode(Node):
	def __init__(self, token: Token, conditions: Node, loop_node: Node) -> None:
		super().__init__(NodeKind.WHILE, token)
		self.conditions: Node = conditions
		self.loop_node: Node = loop_node
		self.token: Token = token

	def __eq__(self, other: "LocalVarNode") -> bool:
		return self.__dict__ == other.__dict__

	def __repr__(self) -> str:
		loop = self.loop_node.__repr__().replace("\n", "\n ")
		conditions = self.conditions.__repr__().replace("\n", "\n ")
		tree: str = ""
		tree += f"{self.token}"
		tree += f"WHILE (\n"
		tree += f" {conditions}\n"
		tree += ")\n"
		tree += f" {loop}\n"
		return tree


class ForNode(Node):
	def __init__(self, token: Token, init: Optional[Node], condition: Optional[Node], inc: Optional[Node],
				 loop_node: Node) -> None:
		super().__init__(NodeKind.FOR, token)
		self.init = init
		self.conditions = condition
		self.inc = inc
		self.loop_node = loop_node

	def __eq__(self, other: "LocalVarNode") -> bool:
		return self.__dict__ == other.__dict__

	def __repr__(self) -> str:
		init = self.init.__repr__().replace("\n", "\n ")
		cond = self.conditions.__repr__().replace("\n", "\n ")
		inc = self.inc.__repr__().replace("\n", "\n ")
		loop = self.loop_node.__repr__().replace("\n", "\n ")
		tree = ""
		tree += f"{self.token}"
		tree += f"FOR ("
		tree += f" {init} ;\n"
		tree += f" {cond} ;\n"
		tree += f" {inc}\n"
		tree += ")\n"
		tree += f" {loop}"
		return tree


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
	def __init__(self, tokens: List[Token], source: str):
		self.source: str = source
		self.tokens: deque[Token] = deque(tokens)
		self.code: List[Node] = []
		self.lvar_offsets: Dict[str, int] = {}
		self.max_local_var_offset: int = 0

	def next(self) -> None:
		self.tokens.popleft()

	def current(self) -> Token:
		return self.tokens[0]

	def is_current(self, string: str) -> bool:
		return self.current().string == string

	def check_syntax(self, string: str, message: str) -> None:
		if not self.is_current(string):
			self.error(message)

	def error(self, message: str) -> None:
		error_token(self.current(), self.source, message)

	# program = stmt*
	# stmt = expr ";"
	#        | "return" expr ";"
	#        | "if" "(" expr ")" stmt ("else" stmt)?
	#        | "while" "(" expr ")" stmt
	#        | "for" "(" expr? ";" expr? ";" expr? ")" stmt
	# expr = assign
	# assign = equality ("=" assign)?
	# equality = relational (("==" | "!=") relational)*
	# relational = add (("<" | "<=" | ">" | ">=") add)*
	# add = mul (("+" | "-") mul)*
	# mul = unary (("*" | "/") unary)*
	# unary = ("+" | "-")? primary
	# primary = num | ident | ("(" expr ")")

	def program(self) -> List[Node]:
		while self.current().kind != TokenKind.EOF:
			self.code.append(self.stmt())
		return self.code

	def stmt(self) -> Node:
		if self.current().kind == TokenKind.RETURN:
			token: Token = self.current()
			self.next()
			node: Node = ReturnNode(token, self.expr())
		elif self.current().kind == TokenKind.IF:
			token: Token = self.current()
			self.next()
			self.check_syntax("(", "不正な条件式です。")
			self.next()
			conditions: Node = self.expr()
			self.check_syntax(")", "不正な条件式です。")
			self.next()
			if_node: Node = self.stmt()
			if self.current().kind == TokenKind.ELSE:
				self.next()
				else_node: Node = self.stmt()
			else:
				else_node: Optional[Node] = None
			node: Node = IfNode(token, conditions, if_node, else_node)
			return node
		elif self.current().kind == TokenKind.WHILE:
			token: Token = self.current()
			self.next()
			self.check_syntax("(", "不正な条件式です。")
			self.next()
			conditions: Node = self.expr()
			self.check_syntax(")", "不正な条件式です。")
			self.next()
			loop_node: Node = self.stmt()
			node: Node = WhileNode(token, conditions, loop_node)
			return node
		elif self.current().kind == TokenKind.FOR:
			token: Token = self.current()
			self.next()
			self.check_syntax("(", "不正な条件式です。")
			self.next()
			init: Optional[Node] = None
			if not self.is_current(";"):
				init = self.expr()
			self.check_syntax(";", "不正な文です。")
			self.next()
			conditions: Optional[Node] = None
			if not self.is_current(";"):
				conditions = self.expr()
			self.check_syntax(";", "不正な文です。")
			self.next()
			inc: Optional[Node] = None
			if not self.is_current(")"):
				inc = self.expr()
			self.check_syntax(")", "不正な条件式です。")
			self.next()
			loop_node: Node = self.stmt()
			node: Node = ForNode(token, init, conditions, inc, loop_node)
			return node
		else:
			node: Node = self.expr()

		self.check_syntax(";", ";が行末にありません")
		self.next()
		return node

	def expr(self) -> Node:
		return self.assign()

	def assign(self) -> Node:
		node: Node = self.equality()
		if self.is_current("="):
			token: Token = self.current()
			kind: NodeKind = NodeKind.ASSIGN
			self.next()
			node = BinaryNode(kind, token, node, self.assign())
		return node

	def equality(self) -> Node:
		node: Node = self.relational()
		for _ in range(len(self.tokens)):
			if self.current().string in ["==", "!="]:
				token: Token = self.current()
				op: str = self.current().string
				kind: NodeKind = op_to_kind(op)
				self.next()
				node = BinaryNode(kind, token, node, self.relational())
			else:
				return node
		return node

	def relational(self) -> Node:
		node: Node = self.add()
		for _ in range(len(self.tokens)):
			if self.current().string in [">", ">="]:
				token: Token = self.current()
				op = self.current().string
				kind: NodeKind = op_to_kind(op)
				self.next()
				node = BinaryNode(kind, token, self.add(), node)
			elif self.current().string in ["<", "<="]:
				token: Token = self.current()
				op: str = self.current().string.replace("<", ">")
				kind: NodeKind = op_to_kind(op)
				self.next()
				node = BinaryNode(kind, token, node, self.add())
			else:
				return node
		return node

	def add(self) -> Node:
		node: Node = self.mul()
		for _ in range(len(self.tokens)):
			if self.current().string in ["+", "-"]:
				token: Token = self.current()
				op: str = self.current().string
				kind: NodeKind = op_to_kind(op)
				self.next()
				node = BinaryNode(kind, token, node, self.mul())
			else:
				return node
		return node

	def mul(self) -> Node:
		node: Node = self.unary()
		for _ in range(len(self.tokens)):
			if self.current().string in ["*", "/"]:
				token: Token = self.current()
				op: str = self.current().string
				kind: NodeKind = op_to_kind(op)
				self.next()
				node = BinaryNode(kind, token, node, self.unary())
			else:
				return node
		return node

	def unary(self) -> Node:
		if self.is_current("-"):
			token: Token = self.current()
			kind = NodeKind.SUB
			self.next()
			node = BinaryNode(kind, token, NumNode(0, token), self.primary())
			return node
		if self.is_current("+"):
			self.next()
		node: Node = self.primary()
		return node

	def primary(self) -> Node:
		if self.is_current("("):
			self.next()
			node: Node = self.expr()
			self.check_syntax(")", "括弧が閉じられていません。")
			self.next()
		else:
			if self.current().kind == TokenKind.NUM:
				token: Token = self.current()
				num: int = int(self.current().string)
				self.next()
				node = NumNode(num, token)
			elif self.current().kind == TokenKind.IDENT:
				token: Token = self.current()
				name: str = self.current().string
				if name in self.lvar_offsets:
					offset: int = self.lvar_offsets[name]
				else:
					self.max_local_var_offset += 8
					offset: int = self.max_local_var_offset
					self.lvar_offsets[name] = offset
				self.next()
				node = LocalVarNode(offset, token)
			else:
				self.error("不正な文です。")
				# 前の関数で例外が投げられるはずだが、IDEが反応してくれないのでここでも投げる
				raise Exception()
		return node


class Function:
	def __init__(self, name: str, nodes: List[Node], local_vars: Dict[str, int]):
		self.name = name
		self.nodes: List[Node] = nodes
		self.lvar_offsets: Dict[str, int] = local_vars


def node_parse(tokens: List[Token], source: str) -> Function:
	parser: NodeParser = NodeParser(tokens, source)
	nodes: List[Node] = parser.program()
	function = Function("main", nodes, parser.lvar_offsets)
	return function
