from node_parser import NodeKind, Node, NumNode, BinaryNode, LocalVarNode, Function
from token_parser import error_token
from typing import List


class AssemblyGenerator:
	def __init__(self, source: str):
		self.source = source

	def gen_lvar_addr(self, node: Node) -> str:
		asm = ""
		if not isinstance(node, LocalVarNode):
			error_token(node.token, self.source, "代入先が不正です。")
		asm += "  mov rax, rbp\n"
		asm += "  sub rax, {}\n".format(node.offset)
		asm += "  push rax\n"
		return asm

	@staticmethod
	def gen_op_code(kind: NodeKind) -> str:
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
		asm += "  push rax\n"
		return asm

	def gen(self, node: Node) -> str:
		asm = ""
		if isinstance(node, NumNode):
			asm += f"  push {node.val}\n"
			return asm
		if node.kind == NodeKind.LVAR:
			asm += self.gen_lvar_addr(node)
			asm += "  pop rax\n"
			asm += "  mov rax, [rax]\n"
			asm += "  push rax\n"
			return asm

		if not isinstance(node, BinaryNode):
			error_token(node.token, self.source, "未知のノードです。")

		if node.kind == NodeKind.ASSIGN:
			asm += self.gen_lvar_addr(node.lhs)
			asm += self.gen(node.rhs)
			asm += "  pop rdi\n"
			asm += "  pop rax\n"
			asm += "  mov [rax], rdi\n"
			asm += "  push rdi\n"
			return asm

		asm += self.gen(node.lhs)
		asm += self.gen(node.rhs)
		asm += "  pop rdi\n"
		asm += "  pop rax\n"
		asm += self.gen_op_code(node.kind)
		return asm

	def function(self, function: Function) -> str:
		asm = ""
		asm += "{}:".format(function.name)
		asm += "  push rbp\n"
		asm += "  mov rbp, rsp\n"
		offset: int = sum([function.lvar_offsets[name] for name in function.lvar_offsets])
		asm += "  sub rsp, {}\n".format(offset)
		for node in function.nodes:
			asm += self.gen(node)
			asm += "  pop rax\n"
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