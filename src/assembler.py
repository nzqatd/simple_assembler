import os
import sys

"""
各コマンドに特有のopcodeなど
"""
opcode = dict(
    [
        ("ADD", "0000"),
        ("SUB", "0001"),
        ("AND", "0010"),
        ("OR", "0011"),
        ("XOR", "0100"),
        ("CMP", "0101"),
        ("MOV", "0110"),
        ("SLL", "1000"),
        ("SLR", "1001"),
        ("SRL", "1010"),
        ("SRA", "1011"),
        ("IN", "1100"),
        ("OUT", "1101"),
        ("HLT", "1111"),
        ("LD", "00"),
        ("ST", "01"),
        ("LI", "000"),
        ("B", "100"),
        ("BE", "000"),
        ("BLT", "001"),
        ("BLE", "010"),
        ("BNE", "011"),
    ]
)


def read_data():
    """
    コマンドライン引数の一番目で指定されたファイルから読み取り、一行ずつリストにして返す。
    コマンドライン引数が指定されなかった場合は、usageを表示してプログラムを終了する。
    """
    if len(sys.argv) < 2:
        print("usage: python3 assembler.py input-file [output-file]")
        exit(0)
    path_in = sys.argv[1]
    fin = open(path_in)
    s = [tmp.strip() for tmp in fin.readlines()]
    fin.close()
    return s


def preproc(line):
    head, tail = "", ""
    for i in range(len(line)):
        if line[i] == " ":
            tail = line[i + 1 :]
            break
        head += line[i]
    cmd = head.upper()
    tmp = [s.strip() for s in tail.split(",")]
    args = []
    for i in range(len(tmp)):
        if "(" in tmp[i] and ")" in tmp[i]:
            a = tmp[i][: tmp[i].find("(")].strip()
            b = tmp[i][tmp[i].find("(") + 1 : tmp[i].find(")")].strip()
            args.append(a)
            args.append(b)
        else:
            args.append(tmp[i])
    return cmd, list(map(int, args))


def assemble(data):
    result = []
    for i in range(len(data)):
        cmd, args = preproc(data[i])
        if cmd in ["ADD", "SUB", "AND", "OR", "XOR", "CMP", "MOV"]:
            result.append(
                "11"
                + format(args[1], "03b")
                + format(args[0], "03b")
                + opcode[cmd]
                + "0000"
            )
        elif cmd in ["SLL", "SLR", "SRL", "SRA"]:
            result.append(
                "11"
                + "000"
                + format(args[0], "03b")
                + opcode[cmd]
                + format(args[1], "04b")
            )
        elif cmd in ["IN"]:
            result.append("11" + "000" + format(args[0], "03b") + opcode[cmd] + "0000")
        elif cmd in ["OUT"]:
            result.append("11" + format(args[0], "03b") + "000" + opcode[cmd] + "0000")
        elif cmd in ["HLT"]:
            result.append("11" + "000" + "000" + "1111" + "0000")
        elif cmd in ["LD", "ST"]:
            result.append(
                opcode[cmd]
                + format(args[0], "03b")
                + format(args[2], "03b")
                + format(args[1] & (2 ** 8 - 1), "08b")
            )
        elif cmd in ["LI"]:
            result.append(
                "10"
                + opcode[cmd]
                + format(args[0], "03b")
                + format(args[1] & (2 ** 8 - 1), "08b")
            )
        elif cmd in ["B"]:
            result.append(
                "10" + opcode[cmd] + "000" + format(args[0] & (2 ** 8 - 1), "08b")
            )
        elif cmd in ["BE", "BLT", "BLE", "BNE"]:
            result.append(
                "10" + "111" + opcode[cmd] + format(args[0] & (2 ** 8 - 1), "08b")
            )
        else:
            print(str(i + 1) + "行目:コマンド名が正しくありません")
            exit(1)
    return result


def write_result(result):
    """
      アセンブルした二進数のリストを書き込む
      書き込み先は、コマンドライン引数によって指定された場合はそのファイル、
      されなかった場合はout.mif
      ワード幅は16,ワード数は256としている
      DATA_RADIXは二進数、ADDRESS_RADIXはDECとしているが
      HEXのほうがよいか？
    """
    path_out = ""
    if len(sys.argv) >= 3:
        path_out = sys.argv[2]
    else:
        path_out = "out.mif"
    fout = open(path_out, mode="w")
    fout.write("WIDTH=16;\n")
    fout.write("DEPTH=256;\n")
    fout.write("ADDRESS_RADIX=DEC;\n")
    fout.write("DATA_RADIX=BIN;\n")
    fout.write("CONTENT BEGIN\n")
    for i in range(len(result)):
        fout.write("\t" + str(i) + " : " + result[i] + ";\n")
    fout.write("END;\n")
    fout.close()


data = read_data()
result = assemble(data)
write_result(result)
