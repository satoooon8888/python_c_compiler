from node_parser import NodeKind, Node, NumNode, BinaryNode


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


def code_gen(node: Node) -> str:
	code = ""
	code += ".intel_syntax noprefix\n"
	code += ".global main\n"
	code += "main: \n"
	code += gen(node)
	code += "  pop rax\n"
	code += "  ret\n"
	return code
