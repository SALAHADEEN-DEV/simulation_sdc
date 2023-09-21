from sdc.settings import BASE_DIR
from . import instructions
from . import utils
from . import constant
import os

# ============================================
##
# Check number sign
##
# ============================================


def twos(val):
    # دالة ايجاد الاعداد السالبة

    return hex((val+(1 << 16)) % (1 << 16))


def check_sign(n):
    # ? Check the sign of the number wither is negitive or positive

    # string array to store all kinds of number
    s = "negative", "zero", "positive"
    s = 0, 1, 2

    # function call to check the sign of number
    val = twos(n)

    return s[val]


def is_positive(n):
    if check_sign(n) == 2:
        return True
    else:
        return False


def is_negitive(n):
    if check_sign(n) == 0:
        return True
    else:
        return False


def is_zero(n):
    if check_sign(n) == 1:
        return True
    else:
        return False

# ============================================
##
# Conversion
##
# ============================================


def decimalToBinary(n):
    # التحويل من عشري الى نظام ثنائي

    return bin(n).replace("0b", "")


def binaryToHex(n):
    # التحويل من النظام الثنائي الى السداسي عشر

    return '%0*X' % ((len(n) + 3) // 4, int(n, 2))


def hexToBinary(n):
    # التحويل من النظام السداسي عشر الى النظام الثنائي

    return "{:0b}".format(int(n, 16))


def hexToDecimal(n):
    # التحويل من النظام السداسي عشر الى النظام العشري

    return int(n, 16)


def decimalToHex(n):
    # التحويل من النظام العشري الى النظام السداسي عشر

    return hex(n)[2:]


def first_compelement(n):
    # The First compelemt if binary value

    data = ''
    for item in hexToBinary(n).rjust(constant.BASE_NUMBER, '0'):
        if item == '1':
            data += '0'
        else:
            data += '1'
    return data

# ============================================
##
# Other actions
##
# ============================================


def log(data):
    print('===========================================')
    print(data)
    print('===========================================')


def is_mri_instruction(instruction):
    if instruction in instructions.MRI:
        return True
    else:
        return False


def is_rri_instruction(instruction):
    if instruction in instructions.RRI:
        return True
    else:
        return False


def is_mri_control_instruction(instruction):
    if instruction in instructions.CONTROL_MRI:
        return True
    else:
        return False


def is_rri_control_instruction(instruction):
    if instruction in instructions.CONTROL_RRI:
        return True
    else:
        return False


def get_registers_data():

    a_f = open(os.path.join(
        BASE_DIR, '1_registers/'+constant.A_REGISTER), "r")
    a_reg_data = a_f.readline().split()[0]
    a_f.close()

    b_reg_data = ''
    b_f = open(os.path.join(
        BASE_DIR, '1_registers/'+constant.B_REGISTER), "r")
    if b_f.readable:
        b_reg_data = b_f.readline().split()[0]
        b_f.close()

    a_log_f = open(os.path.join(
        BASE_DIR, '1_registers/'+constant.A_REGISTER_LOG), "r")
    a_reg_log_data = a_log_f.readlines()
    a_log_f.close()

    b_reg_log_data = ''
    b_log_f = open(os.path.join(
        BASE_DIR, '1_registers/'+constant.B_REGISTER_LOG), "r")
    if b_log_f.readable:
        b_reg_log_data = b_log_f.readlines()
        b_log_f.close()

    #   Other registers
    others = os.listdir(os.path.join(BASE_DIR, '1_registers/'))
    others.remove(constant.B_REGISTER_LOG)
    others.remove(constant.A_REGISTER_LOG)
    others.remove(constant.B_REGISTER)
    others.remove(constant.A_REGISTER)

    others_reg_data = []
    other_reg_caption = []

    for reg in others:
        f = open(os.path.join(
            BASE_DIR, '1_registers/'+reg), "r")
        data = f.readlines()
        other_reg_caption.append(reg)
        others_reg_data.append(data)

        f.close()

    return [a_reg_data, b_reg_data, a_reg_log_data, b_reg_log_data, other_reg_caption, others_reg_data]


def write_error_file(data):
    # Write data to the Accomulator Register

    f = open(os.path.join(BASE_DIR, '1_registers/'+constant.ERROR_REGISTER), 'w')
    f.writelines(data)
    f.close()
