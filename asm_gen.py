from node_parser import NodeKind, Node, NumNode, BinaryNode
from typing import List


def get_asm(kind: NodeKind):
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
		asm += "cmp rax, rdi\n"
		asm += "sete al\n"
		asm += "movzb rax, al\n"
	elif kind == NodeKind.NE:
		asm += "cmp rax, rdi\n"
		asm += "setne al\n"
		asm += "movzb rax, al\n"
	elif kind == NodeKind.LT:
		asm += "cmp rax, rdi\n"
		asm += "setl al\n"
		asm += "movzb rax, al\n"
	elif kind == NodeKind.LE:
		asm += "cmp rax, rdi\n"
		asm += "setle al\n"
		asm += "movzb rax, al\n"
	asm += "  push rax\n"
	return asm


def gen(node: Node) -> str:
	code = ""
	if isinstance(node, NumNode):
		code += f"  push {node.val}\n"
		return code
	if not isinstance(node, BinaryNode):
		# TODO: impl error class
		raise Exception
	code += gen(node.lhs)
	code += gen(node.rhs)
	code += "  pop rdi\n"
	code += "  pop rax\n"
	code += get_asm(node.kind)
	return code


def code_gen(nodes: List[Node]) -> str:
	code = ""
	code += ".intel_syntax noprefix\n"
	code += ".global main\n"
	code += "main: \n"
	for node in nodes:
		code += gen(node)
	code += "  pop rax\n"
	code += "  ret\n"
	return code
