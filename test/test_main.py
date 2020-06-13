import subprocess
from main import gen_asm
import os


def executed_exit_code(source: str):
	asm: str = gen_asm(source)
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
	assert_asm("1 + 2", 3)
	assert_asm("1 + 2", 3)
	assert_asm("0", 0)

	assert_asm("42", 42)
	assert_asm("5+20-4", 21)
	assert_asm(" 12 + 34 - 5 ", 41)

	assert_asm("3+3*3", 12)
	assert_asm("(3+3)*3", 18)

	assert_asm("-3+4", 1)
	assert_asm("12 + (-2 * 3)", 6)

	assert_asm("1 == 1", 1)
	assert_asm("1 == 0", 0)
	assert_asm("1 != 1", 0)
	assert_asm("1 != 0", 1)

	assert_asm("1 < 2", 1)
	assert_asm("2 < 1", 0)
	assert_asm("1 < 1", 0)

	assert_asm("1 > 2", 0)
	assert_asm("2 > 1", 1)
	assert_asm("1 > 1", 0)

	assert_asm("1 <= 2", 1)
	assert_asm("2 <= 1", 0)
	assert_asm("1 <= 1", 1)

	assert_asm("1 >= 2", 0)
	assert_asm("2 >= 1", 1)
	assert_asm("1 >= 1", 1)

	assert_asm("(1+2*3) - 6 == 1 < 1 - -1", 1)
	assert_asm("1 > 2 == 2 < 1", 1)

	assert_asm("a = 1", 1)
	assert_asm("z = 1", 1)
	assert_asm("a = 1; a", 1)
	assert_asm("a = 1; b = a + 1; a + b", 3)
