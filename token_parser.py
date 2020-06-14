import enum
from typing import List


class TokenKind(enum.Enum):
	RESERVED = enum.auto()  # 記号
	IDENT = enum.auto()  # 識別子（変数）
	NUM = enum.auto()  # 数値
	EOF = enum.auto()  # プログラムの終端
	INVALID = enum.auto()  # エラーの際に使う


class Token:
	def __init__(self, kind: TokenKind, string: str, column: int, row: int) -> None:
		self.kind: TokenKind = kind
		self.string: str = string
		self.column: int = column
		self.row: int = row

	def __str__(self) -> str:
		kind: str = str(self.kind).split(".")[1]
		return f'<class Token {kind} \"{self.string}\" {self.column}:{self.row}>'

	def __repr__(self) -> str:
		return self.__str__()

	def __eq__(self, other: "Token") -> bool:
		return self.__dict__ == other.__dict__


def error_token(token: Token, source: str, message: str) -> None:
	error_with_place(token.column, token.row, len(token.string), source, message)


def error_with_place(column: int, row: int, length: int, source: str, message: str) -> None:
	info: str = f"line {column + 1} | "
	print(info + source.split("\n")[column])
	padding_length: int = len(info) + row
	print(" " * padding_length + "^" + "~" * (length - 1))
	print(f"Error: {message}")
	exit(1)


def startswith(cmp_str: str, cmp: str) -> bool:
	return cmp_str[:len(cmp)] == cmp


def is_allowed_var_char(char: str):
	# A-Z a-z 0-9 _
	return (
			"A" <= char <= "Z"
			or "a" <= char <= "z"
			or "0" <= char <= "9"
			or char == "_"
	)


def is_allowed_first_var_char(char: str):
	# A-Z a-z 0-9 _
	return (
			"A" <= char <= "Z"
			or "a" <= char <= "z"
			or char == "_"
	)


def tokenize(input_str: str) -> List[Token]:
	tokens: List[Token] = []

	i: int = 0
	# 0-indexed
	column: int = 0
	row: int = 0
	# 行の最初の文字のiを保存しておく
	column_start_index: int = 0
	# 上から文字列が長い順に
	while i < len(input_str):
		row = i - column_start_index
		if input_str[i] == "\n":
			column += 1
			i += 1
			column_start_index = i
			continue

		if input_str[i] in [" ", "	"]:
			i += 1
			continue

		if input_str[i:i + 2] in ["==", "!=", "<=", ">="]:
			kind = TokenKind.RESERVED
			token_str = input_str[i:i + 2]
			tokens.append(Token(kind, token_str, column, row))
			i += 2
			continue

		if input_str[i] in "+-*/()<>=;":
			kind = TokenKind.RESERVED
			token_str = input_str[i]
			tokens.append(Token(kind, token_str, column, row))
			i += 1
			continue

		if input_str[i].isdigit():
			kind = TokenKind.NUM
			token_str = ""
			while i < len(input_str) and input_str[i].isdigit():
				token_str += input_str[i]
				i += 1
			tokens.append(Token(kind, token_str, column, row))
			continue

		if is_allowed_first_var_char(input_str[i]):
			kind = TokenKind.IDENT
			token_str = ""
			while i < len(input_str) and is_allowed_var_char(input_str[i]):
				token_str += input_str[i]
				i += 1
			tokens.append(Token(kind, token_str, column, row))
			continue

		error_with_place(column, row, 1, input_str, "トークナイズできません")

	kind = TokenKind.EOF
	token_str = ""
	row += 1
	tokens.append(Token(kind, token_str, column, row))

	return tokens
