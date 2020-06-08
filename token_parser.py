import enum
from typing import List


# Exceptions
class InvalidTokenError(Exception):
	pass


def error_at(index: int, length: int, source: str, message: str, error: Exception) -> None:
	print(source)
	print(" " * index + "^" + "~" * (length - 1))
	print(f"Error: {message}")
	raise error


class TokenKind(enum.Enum):
	RESERVED = enum.auto()  # 記号
	NUM = enum.auto()
	EOF = enum.auto()


class Token:
	def __init__(self, kind: TokenKind, string: str) -> None:
		self.kind: TokenKind = kind
		self.string: str = string

	def __str__(self) -> str:
		return f'<class Token({self.kind}, \"{self.string}")>'

	def __repr__(self) -> str:
		return f'<class Token({self.kind}, "{self.string}")>'

	def __eq__(self, other: "Token") -> bool:
		return self.kind == other.kind and self.string == other.string


def startswith(cmp_str: str, cmp: str) -> bool:
	return cmp_str[:len(cmp)] == cmp


def tokenize(input_str: str) -> List[Token]:
	padding = [" ", "	"]
	tokens: List[Token] = []

	i: int = 0
	# 上から文字列が長い順に
	while i < len(input_str):
		if input_str[i] in padding:
			i += 1
			continue

		if input_str[i:i+2] in ["==", "!=", "<=", ">="]:
			kind = TokenKind.RESERVED
			token_str = input_str[i:i + 2]
			tokens.append(Token(kind, token_str))
			i += 2
			continue

		if input_str[i] in "+-*/()<>":
			kind = TokenKind.RESERVED
			token_str = input_str[i]
			tokens.append(Token(kind, token_str))
			i += 1
			continue

		if input_str[i].isdigit():
			kind = TokenKind.NUM
			token_str = ""
			while i < len(input_str) and input_str[i].isdigit():
				token_str += input_str[i]
				i += 1
			tokens.append(Token(kind, token_str))
			continue

		error_at(i, 1, input_str, "トークナイズできません", InvalidTokenError())

	kind = TokenKind.EOF
	token_str = ""
	tokens.append(Token(kind, token_str))

	return tokens
