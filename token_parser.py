import enum
from typing import List, Optional

# 長い記号から順に
reserved_symbol = [
	"==",
	"!=",
	"<=",
	">=",
	"<",
	">",
	"+",
	"-",
	"*",
	"/",
	"=",
	"(",
	")",
	";"
]

reserved_word = [
	"return"
]

padding = [" ", "	", "\n"]


class TokenKind(enum.Enum):
	RESERVED = enum.auto()  # 記号
	IDENT = enum.auto()  # 識別子（変数）
	NUM = enum.auto()  # 数値
	RETURN = enum.auto()  # return文
	EOF = enum.auto()  # プログラムの終端
	INVALID = enum.auto()  # エラーの際に使う


class Token:
	def __init__(self, kind: TokenKind, string: str, index: int) -> None:
		self.kind: TokenKind = kind
		self.string: str = string
		self.index: int = index

	def __str__(self) -> str:
		kind: str = str(self.kind).split(".")[1]
		return f'<class Token {kind} \"{self.string}\" {self.index}>'

	def __repr__(self) -> str:
		return self.__str__()

	def __eq__(self, other: "Token") -> bool:
		return self.__dict__ == other.__dict__


def error_token(token: Token, source: str, message: str) -> None:
	error_with_place(token.index, len(token.string), source, message)


def error_with_place(index: int, length: int, source: str, message: str) -> None:
	column: int = 0
	row: int = 0
	for i, si in enumerate(source):
		if i == index:
			break
		row += 1
		if si == "\n":
			column += 1
			row = 0
	info: str = f"line {column + 1} | "
	print(info + source.split("\n")[column])
	padding_length: int = len(info) + row
	print(" " * padding_length + "^" + "~" * (length - 1))
	print(f"Error: {message}")
	exit(1)


def match_with_words(cmp: str, search_words: List) -> Optional[str]:
	for word in search_words:
		if cmp[:len(word)] == word:
			return word
	return None


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
	while i < len(input_str):

		match_string = match_with_words(input_str[i:], padding)
		if match_string is not None:
			i += 1
			continue

		match_string = match_with_words(input_str[i:], reserved_symbol)
		if match_string is not None:
			kind = TokenKind.RESERVED
			token_str = match_string
			tokens.append(Token(kind, token_str, i))
			i += len(match_string)
			continue

		if input_str[i].isdigit():
			kind = TokenKind.NUM
			token_str = ""
			allowed_num_string = "0123456789"
			base = 10
			match_base = match_with_words(input_str[i:], ["0x", "0b", "0o"])
			token_index: int = i
			if match_base is not None:
				i += 2
				if match_base == "0x":
					allowed_num_string = "0123456789abcdef"
					base = 16
				elif match_base == "0b":
					allowed_num_string = "01"
					base = 2
				elif match_base == "0o":
					allowed_num_string = "01234567"
					base = 8
			while i < len(input_str) and input_str[i] in allowed_num_string:
				token_str += input_str[i]
				i += 1
			if token_str == "":
				error_with_place(i, 1, input_str, "無効な数値です。")
			token_str = str(int(token_str, base))
			tokens.append(Token(kind, token_str, token_index))
			continue

		match_string = match_with_words(input_str[i:], reserved_word)
		if match_string is not None:
			if match_string == "return":
				kind = TokenKind.RETURN
			else:
				error_with_place(i, len(match_string), input_str, "予約語が実装されていません。")
				raise Exception()
			token_str = match_string
			tokens.append(Token(kind, token_str, i))
			i += len(token_str)
			continue

		if is_allowed_first_var_char(input_str[i]):
			kind = TokenKind.IDENT
			token_str = ""
			token_index: int = i
			while i < len(input_str) and is_allowed_var_char(input_str[i]):
				token_str += input_str[i]
				i += 1
			tokens.append(Token(kind, token_str, token_index))
			continue

		error_with_place(i, 1, input_str, "解釈できません")

	kind = TokenKind.EOF
	token_str = ""
	tokens.append(Token(kind, token_str, i))

	return tokens
