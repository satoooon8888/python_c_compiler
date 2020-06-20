from node_parser import NodeKind, Node, NumNode, BinaryNode, LocalVarNode, Function, ReturnNode, IfNode, WhileNode, \
	ForNode, BlockNode
from token_parser import error_token
from typing import List


class AssemblyGenerator:
	def __init__(self, source: str):
		self.source = source
		self.label_counter = 0

	def create_label(self, name=""):
		self.label_counter += 1
		return f".{name}__{self.label_counter}"

	def gen_lvar_addr(self, node: Node) -> str:
		asm = ""
		if not isinstance(node, LocalVarNode):
			error_token(node.token, self.source, "代入先が不正です。")
		asm += f"  lea rax, [rbp - {node.offset}]\n"
		return asm

	@staticmethod
	def gen_opcode(kind: NodeKind) -> str:
		asm = ""
		if kind == NodeKind.ADD:
			asm += "  add rax, rdi\n"
		elif kind == NodeKind.SUB:
			asm += "  sub rax, rdi\n"
		elif kind == NodeKind.MUL:
			asm += "  imul rax, rdi\n"
		elif kind == NodeKind.DIV:
			asm += "  cqo\n"
			asm += "  idiv rdi\n"
		elif kind == NodeKind.EQ:
			asm += "  cmp rax, rdi\n"
			asm += "  sete al\n"
			asm += "  movzb rax, al\n"
		elif kind == NodeKind.NE:
			asm += "  cmp rax, rdi\n"
			asm += "  setne al\n"
			asm += "  movzb rax, al\n"
		elif kind == NodeKind.LT:
			asm += "  cmp rax, rdi\n"
			asm += "  setl al\n"
			asm += "  movzb rax, al\n"
		elif kind == NodeKind.LE:
			asm += "  cmp rax, rdi\n"
			asm += "  setle al\n"
			asm += "  movzb rax, al\n"
		return asm

	def gen(self, node: Node) -> str:
		asm = ""

		if isinstance(node, NumNode):
			asm += f"  mov rax, {node.val}\n"
			return asm

		if node.kind == NodeKind.LVAR:
			asm += self.gen_lvar_addr(node)
			asm += "  mov rax, [rax]\n"
			return asm

		if node.kind == NodeKind.RETURN:
			if not isinstance(node, ReturnNode):
				error_token(node.token, self.source, "RETURNトークンがReturnNode型でありません。")
			asm += self.gen(node.value)
			asm += "  jmp .L.end\n"
			return asm

		if node.kind == NodeKind.IF:
			if not isinstance(node, IfNode):
				error_token(node.token, self.source, "IfトークンがIfNode型でありません。")
			asm += self.gen(node.conditions)
			asm += "  cmp rax, 0\n"
			end_label = self.create_label("L.endif")
			if node.else_node is None:
				asm += f"  je {end_label}\n"
				asm += self.gen(node.if_node)
				asm += f"{end_label}:\n"
			else:
				else_label = self.create_label("L.else")
				asm += f"  je {else_label}\n"
				asm += self.gen(node.if_node)
				asm += f"  jmp {end_label}\n"
				asm += f"{else_label}:\n"
				asm += self.gen(node.else_node)
				asm += f"{end_label}:\n"
			return asm

		if node.kind == NodeKind.WHILE:
			if not isinstance(node, WhileNode):
				error_token(node.token, self.source, "WhileトークンがWhileNode型でありません。")
			begin_label = self.create_label("L.begin_while")
			end_label = self.create_label("L.end_while")
			asm += f"{begin_label}:\n"
			asm += self.gen(node.conditions)
			asm += f"  cmp rax, 0\n"
			asm += f"  je {end_label}\n"
			asm += self.gen(node.loop_node)
			asm += f"  jmp {begin_label}\n"
			asm += f"{end_label}:\n"
			return asm

		if node.kind == NodeKind.FOR:
			if not isinstance(node, ForNode):
				error_token(node.token, self.source, "WhileトークンがWhileNode型でありません。")
			begin_label = self.create_label("L.begin_for")
			end_label = self.create_label("L.end_for")
			asm += self.gen(node.init)
			asm += f"{begin_label}:\n"
			asm += self.gen(node.conditions)
			asm += f"  cmp rax, 0\n"
			asm += f"  je {end_label}\n"
			asm += self.gen(node.loop_node)
			asm += self.gen(node.inc)
			asm += f"  jmp {begin_label}\n"
			asm += f"{end_label}:\n"
			return asm

		if node.kind == NodeKind.BLOCK:
			if not isinstance(node, BlockNode):
				error_token(node.token, self.source, "BlockトークンがBlockNode型でありません。")
			for node in node.nodes:
				asm += self.gen(node)
			return asm

		if not isinstance(node, BinaryNode):
			error_token(node.token, self.source, "未知のノードです。")

		if node.kind == NodeKind.ASSIGN:
			asm += self.gen_lvar_addr(node.lhs)
			asm += "  push rax\n"
			asm += self.gen(node.rhs)
			asm += "  push rax\n"
			asm += "  pop rdi\n"
			asm += "  pop rax\n"
			asm += "  mov [rax], rdi\n"
			return asm

		asm += self.gen(node.lhs)
		asm += "  push rax\n"
		asm += self.gen(node.rhs)
		asm += "  push rax\n"
		asm += "  pop rdi\n"
		asm += "  pop rax\n"
		asm += self.gen_opcode(node.kind)
		return asm

	def function(self, function: Function) -> str:
		asm = ""
		asm += "{}:\n".format(function.name)
		asm += "  push rbp\n"
		asm += "  mov rbp, rsp\n"
		offset: int = sum([function.lvar_offsets[name] for name in function.lvar_offsets])
		asm += "  sub rsp, {}\n".format(offset)
		for node in function.nodes:
			asm += self.gen(node)
		asm += ".L.end:\n"
		asm += "  mov rsp, rbp\n"
		asm += "  pop rbp\n"
		asm += "  ret\n"
		return asm

	def program(self, functions: List[Function]):
		asm = ""
		asm += ".intel_syntax noprefix\n"
		asm += ".global main\n"
		asm += "".join(map(self.function, functions))
		return asm


def asm_gen(functions: List[Function], source: str) -> str:
	generator = AssemblyGenerator(source)
	return generator.program(functions)
