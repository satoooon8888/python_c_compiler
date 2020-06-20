import subprocess
from main import compile_source
import os


def executed_exit_code(source: str):
	asm: str = compile_source(source)
	with open("./tmp.s", "w") as f:
		f.write(asm)
	if os.name == "nt":
		proc = subprocess.run("ubuntu run \"gcc ./tmp.s -o ./tmp && ./tmp; echo $?\"", shell=True, stdout=subprocess.PIPE)
	elif os.name == "posix":
		proc = subprocess.run("gcc ./tmp.s -o ./tmp && ./tmp; echo $?", shell=True, stdout=subprocess.PIPE)
	else:
		raise EnvironmentError("This OS don't support.")
	result: int = int(proc.stdout.decode())
	os.remove("./tmp")
	os.remove("./tmp.s")
	return result


def assert_asm(source: str, result: int):
	assert executed_exit_code(source) == result


def test_main():
	assert_asm("return 1 + 2;", 3)
	assert_asm("return 1 + 2;", 3)
	assert_asm("return 0;", 0)

	assert_asm("return 42;", 42)
	assert_asm("return 5+20-4;", 21)
	assert_asm("return 12 + 34 - 5 ;", 41)

	assert_asm("return 3+3*3;", 12)
	assert_asm("return (3+3)*3;", 18)

	assert_asm("return -3+4;", 1)
	assert_asm("return 12 + (-2 * 3);", 6)

	assert_asm("return 1 == 1;", 1)
	assert_asm("return 1 == 0;", 0)
	assert_asm("return 1 != 1;", 0)
	assert_asm("return 1 != 0;", 1)

	assert_asm("return 1 < 2;", 1)
	assert_asm("return 2 < 1;", 0)
	assert_asm("return 1 < 1;", 0)

	assert_asm("return 1 > 2;", 0)
	assert_asm("return 2 > 1;", 1)
	assert_asm("return 1 > 1;", 0)

	assert_asm("return 1 <= 2;", 1)
	assert_asm("return 2 <= 1;", 0)
	assert_asm("return 1 <= 1;", 1)

	assert_asm("return 1 >= 2;", 0)
	assert_asm("return 2 >= 1;", 1)
	assert_asm("return 1 >= 1;", 1)

	assert_asm("return (1+2*3) - 6 == 1 < 1 - -1;", 1)
	assert_asm("return 1 > 2 == 2 < 1;", 1)

	assert_asm("a = 1; return a;", 1)
	assert_asm("z = 1; return z;", 1)
	assert_asm("a = 1; b = a + 1; return a + b;", 3)

	assert_asm("foo = 1; return foo;", 1)
	assert_asm("foo = 1; bar = foo + 1; return bar;", 2)
	assert_asm("hoge = 1; fuga = 2; return hoge + fuga;", 3)
	assert_asm("_azAZ09_ = 1; return _azAZ09_;", 1)

	assert_asm("foo = 0xef; return foo + 16;", 255)
	assert_asm("1; return 2; 3;", 2)

	assert_asm("if (1 == 1) return 2; return 1;", 2)
	assert_asm("if (1 != 1) return 2; return 1;", 1)
	assert_asm("if (1 == 1) foo = 1; else foo = 2; return foo;", 1)
	assert_asm("if (1 != 1) foo = 1; else foo = 2; return foo;", 2)




