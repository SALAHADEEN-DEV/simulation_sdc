import os
import shutil

from sdc.settings import BASE_DIR
from . import utils
from . import constant
from . import instructions


class AssemblingActivity:
    def __init__(self, assembly, request):
        self.instructions = assembly[1]
        self.instructions_hex = assembly[2]
        self.instructions_addres = assembly[3]
        self.variables_address = assembly[4]
        self.variables_data = assembly[5]

        init_registers()
        self.read_instructions()

    def read_instructions(self):
        # Read instruction line by line and excute each instruction alone

        for instr in self.instructions:

            # Get the opcode whithout the address then check the type of instruction

            # ? Excute Normal MRI Instruction
            if utils.is_mri_instruction(instr.split()[0]):
                self.excute_mri(instr)

            # ?Excute MRI Control Instruction
            elif utils.is_rri_control_instruction(instr.split()[0]):
                print('')

            # ?Excute RRI Control Instruction
            elif utils.is_rri_control_instruction(instr.split()[0]):
                reg_a = get_register_data(constant.A_REGISTER)

                # ? SAZ
                if instr == instructions.CONTROL_RRI[0]:
                    if utils.is_zero(reg_a):
                        continue

                # ? SAP
                if instr == instructions.CONTROL_RRI[1]:
                    if utils.is_positive(reg_a):
                        continue

                # ? SAN
                if instr == instructions.CONTROL_RRI[2]:
                    if utils.is_negitive(reg_a):
                        continue

            # ? Excute Normal RRI Instruction
            else:
                self.excute_rri(instr.split()[0].strip())

    def excute_mri(self, instr):

        #  excute MRI instruction
        instruction = instr.split()[0].strip()

        # The address after the instruction
        address = self.variables_address[instr.split()[1]]

        # The numerical value of the address
        data = self.variables_data[int(utils.hexToDecimal(address))]

        # ? LDA
        if instruction == instructions.MRI[0]:
            set_register_data(constant.A_REGISTER, data)

        # ? STA
        if instruction == instructions.MRI[1]:
            set_variable_data(
                instr.split()[1], get_register_data(constant.A_REGISTER))

    def excute_rri(self, instr):

        # ? CMA
        if instr == instructions.RRI[0]:
            # Get the first compelment
            first_compelment = utils.first_compelement(
                get_register_data(constant.A_REGISTER))
            #
            set_register_data(constant.A_REGISTER,
                              utils.binaryToHex(first_compelment))

        # ? INA
        if instr == instructions.RRI[1]:
            data = get_register_data(constant.A_REGISTER)
            data = int(utils.hexToDecimal(data))+1
            set_register_data(constant.A_REGISTER,
                              utils.decimalToHex(data))

        # ? CLA
        if instr == instructions.RRI[2]:
            set_register_data(constant.A_REGISTER, '')

        # ? ADD
        if instr == instructions.RRI[3]:
            reg_a = (utils.hexToDecimal(
                get_register_data(constant.A_REGISTER)))
            reg_b = (utils.hexToDecimal(
                get_register_data(constant.B_REGISTER)))
            data = bin(reg_a+reg_b)[2:]
            utils.log(bin(reg_a))
            utils.log(bin(reg_b))

            if len(data) > 12:
                data = data[1:]
            set_register_data(constant.A_REGISTER, utils.binaryToHex(data))

        # ? XOR
        if instr == instructions.RRI[4]:
            reg_a = int(utils.hexToDecimal(
                get_register_data(constant.A_REGISTER)))
            reg_b = int(utils.hexToDecimal(
                get_register_data(constant.B_REGISTER)))

            data = reg_a ^ reg_b
            set_register_data(constant.A_REGISTER, utils.decimalToHex(data))

        # ? AND
        if instr == instructions.RRI[5]:
            reg_a = int(utils.hexToDecimal(
                get_register_data(constant.A_REGISTER)))
            reg_b = int(utils.hexToDecimal(
                get_register_data(constant.B_REGISTER)))

            data = reg_a & reg_b
            set_register_data(constant.A_REGISTER, utils.decimalToHex(data))

        # ? OR
        if instr == instructions.RRI[6]:
            reg_a = int(utils.hexToDecimal(
                get_register_data(constant.A_REGISTER)))
            reg_b = int(utils.hexToDecimal(
                get_register_data(constant.B_REGISTER)))

            data = reg_a | reg_b
            set_register_data(constant.A_REGISTER, utils.decimalToHex(data))

        # ? MBA
        if instr == instructions.RRI[11]:
            reg_b = get_register_data(constant.B_REGISTER)
            set_register_data(constant.A_REGISTER, reg_b)

        # ? MAB
        if instr == instructions.RRI[12]:
            reg_a = get_register_data(constant.A_REGISTER)
            set_register_data(constant.B_REGISTER, reg_a)

        return

# ============================================
##
# Variable actions
##
# ============================================


def set_variable_data(variable, data):
    if variable == constant.A_REGISTER:
        write_a_register(data)
    elif variable == constant.B_REGISTER:
        write_b_register(data)
    else:
        write_nameless_register(variable, data)

# ============================================
##
# Register actions
##
# ============================================


def get_register_data(register):
    try:
        f = open(os.path.join(BASE_DIR, '1_registers/'+register), "r")
        data = f.readline()
        f.close()
        return data.split()[0]
    except:
        utils.write_error_file(
            'Please Be sure that the register you enter is valid: '+register)


def set_register_data(register, data):
    if register == constant.A_REGISTER:
        write_a_register(data)
    elif register == constant.B_REGISTER:
        write_b_register(data)

# ============================================
##
# Prepare data
##
# ============================================


# def prepare_instructions(instructions, variables):
#     # To split instruction and address apart and remove the variables

#     instructions_list = []
#     for inst in instructions:
#         data = inst.split()

#         instructions_list.append(data[0])

#         for variable in variables:
#             if data[0] == variable:
#                 del instructions_list[instructions_list.index(data[0])]

#     return instructions_list


def init_registers():
    # Clear any data remains in register files

    for root, dirs, files in os.walk(os.path.join(BASE_DIR, '1_registers')):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

# ============================================
##
# Write data to the registers
##
# ============================================


def write_nameless_register(name, data):
    # Write data to the Accomulator Register

    f = open(os.path.join(BASE_DIR, '1_registers/' +
             name+constant.NAMELESS_REGISTER_LOG), 'a')
    f.writelines('\n'+data)
    f.close()

    f = open(os.path.join(BASE_DIR, '1_registers/' +
             name+constant.NAMELESS_REGISTER), 'w')
    f.writelines(data)
    f.close()


def write_a_register(data):
    # Write data to the Accomulator Register

    f = open(os.path.join(BASE_DIR, '1_registers/'+constant.A_REGISTER_LOG), 'a')
    f.writelines('\n'+data)
    f.close()

    f = open(os.path.join(BASE_DIR, '1_registers/'+constant.A_REGISTER), 'w')
    f.writelines(data)
    f.close()


def write_b_register(data):
    # Write data to the B Register

    f = open(os.path.join(BASE_DIR, '1_registers/'+constant.B_REGISTER_LOG), 'a')
    f.writelines('\n'+data)
    f.close()

    f = open(os.path.join(BASE_DIR, '1_registers/'+constant.B_REGISTER), 'w')
    f.writelines(data)
    f.close()


def write_dr_register(data):
    # Write data to the DR Register

    f = open(os.path.join(BASE_DIR, '1_registers/'+constant.DR_REGISTER_LOG), 'a')
    f.writelines('\n'+data)
    f.close()

    f = open(os.path.join(BASE_DIR, '1_registers/'+constant.DR_REGISTER), 'w')
    f.writelines(data)
    f.close()


