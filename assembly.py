def parse_assembly_line(line):
    # Separar instrução e argumentos
    parts = line.strip().split()
    if not parts:
        return None  # Linha vazia ou comentário

    instr = parts[0].upper()
    args = parts[1:] if len(parts) > 1 else []

    # Aqui você pode usar um dicionário com os opcodes reais depois
    instr_map = {
        "JMP": "0000",
        "JEQ": "0001",
        "JNE": "0001",
        "JLT": "0001",
        "JGE": "0001",
        "LDR": "0010",
        "STR": "0011",
        "MOV": "0100",
        "ADD": "0101",
        "ADDI": "0110",
        "SUB": "0111",
        "SUBI": "1000",
        "AND": "1001",
        "OR": "1010",
        "SHR": "1011",
        "SHL": "1100",
        "CMP": "1101",
        "PUSH": "1110",
        "POP": "1111",
        "HALT": "1111",
    }

    # Simula encoding de 16 bits com opcode + argumentos
    if instr in instr_map:
        opcode = instr_map[instr]
    else:
        raise ValueError(f"Instrução desconhecida: {instr}")

    # Vamos simular que cada argumento é um número binário de 4 bits
    arg_bin = ""
    # for arg in args:
    #     try:
    #         num = int(arg.replace('R', ''))  # Suporta R0, R1, etc
    #         arg_bin += f'{num:04b}'
    #     except ValueError:
    #         raise ValueError(f"Argumento inválido: {arg}")
    for arg in args:
        arg = arg.replace(",", "")

        if arg.startswith("R"):  # Register
            num = int(arg[1:])
            arg_bin += f"{num:04b}"
        elif arg.startswith("#"):  # Immediate value
            num = int(arg[1:])
            arg_bin += f"{num:08b}"  # Immediate could be longer
        else:
            raise ValueError(f"Invalid argument format: {arg}")

    # Completa para 16 bits se necessário
    instr_bin = opcode + arg_bin
    # .ljust(16, "0")
    if len(instr_bin) > 16:
        return instr_bin[:11] + instr_bin[15:]
    if len(instr_bin) < 16:
        return instr_bin[:4] + "0000" + instr_bin[:8]
    if opcode == instr_map["HALT"]:
        return "1111111111111111"
    return instr_bin


def binary_to_hex(bin_str):
    # Ensure it's exactly 16 bits
    if len(bin_str) != 16 or any(c not in "01" for c in bin_str):
        raise ValueError("Input must be a 16-bit binary string.")

    hex_value = hex(int(bin_str, 2))[2:].upper()  # Convert to hex and remove '0x'
    return hex_value.zfill(4)  # Pad with zeros to make it 4 characters


def assemble(assembly_code):
    machine_code = ""
    i = 0
    for line in assembly_code.splitlines():
        line = line.strip()
        if line == "" or line.startswith(";"):  # Ignorar comentários
            continue
        bin_instr = parse_assembly_line(line)
        if bin_instr:
            machine_code += (
                str(i).rjust(4, "0") + ": 0x" + binary_to_hex(bin_instr) + "\n"
            )
            i += 1
    return machine_code

