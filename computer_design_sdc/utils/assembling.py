
# تعريف الاوامر مع شفرة كل أمر
import re
from builtins import type
from django.contrib import messages

from . import utils
from . import instructions


class Assembling:
    def __init__(self, assembly_code, request):
        self.assembly_code = assembly_code
        self.assembly = read_file(assembly_code, request)


def read_file(assembly_code, request):
    labledic = {}     # dectionary to store the lable and it's location
    codelist = []

    c = []  # Ensure that each instruction in new line

    for line in assembly_code.split('\n'):
        c.append(line.strip())

    # حذف الفراغات والتعليقات اذا وجدت
    for i in range(len(c)):
        c[i] = c[i].strip()
        if (c[i].find('/') != -1):
            c[i] = c[i][0:c[i].find('/')]

    # التأكد من وجود الموجة BEGIN
    # اضهار رسالة خطأ اذا لم يكن موجود
    b = 0
    check = 0
    for i in range(len(c)):
        b = 1+b
        if (c[i].find('BEGIN') != -1):
            check = 1
            break

    if (check == 0):
        utils.log("Begin not found")
        messages.error(request, 'Begin not found')
        return []

    check = -1

    # التأكد من وجود الموجة ومن ثم حذفها ان وجدتEND
    # اضهار رسالة خطأ اذا لم يوجد
    e = 0
    for i in range(len(c)):
        e = 1+e
        if (c[i].find('END') != -1):
            check = 1
            break
    if (check == -1):
        utils.log("end not found")
        messages.error(request, 'end not found')
        return []
    for i in range(b-1, e):
        if (c[i] != ''):
            codelist.append(c[i])
    del codelist[0]

    # # التأكد من وجود الموجة ORG
    # # خزن عنوان البداية اذا وجد الموجة
    # # ثم خزن بقية العناوين الفعليه في قائمة

    found = 'ORG' in codelist[0]
    if found == True:
        linenumber = [codelist[0]]
        del (codelist[0])
        linenumber[0] = re.sub('ORG', '', linenumber[0])
        linenumber[0] = re.sub(' ', '', linenumber[0])
        linenumber = [k.rstrip('\n') for k in linenumber]
        linenumber[0] = '%2x' % int(linenumber[0][0:2], 16)
        linenumber[0] = int(linenumber[0], 16)
        origin = linenumber[0]
        for i in range(0, len(codelist)-2):
            linenumber.append(linenumber[0]+i+1)

    # البدا من العنوان 0 اذا لم يوجد الموجه ORG
    else:
        linenumber = [0]
        for i in range(0, len(codelist)-2):
            linenumber.append(linenumber[0]+i+1)
    # نسخة من المحتوى الكلي للكود بعد التأكد من جميع ما تم ذكرة
    copy_codelist = []
    for i in range(len(codelist)):
        copy_codelist.append(codelist[i])

    # متغيرات لتخزين قيم العناوين الرمزية والفعليه
    HLTindex = -1
    ENDindex = -1
    varaddres = {}
    afterhlt = []

    # التأكد من وجود الموجه HLT
    for i in range(len(codelist)):
        HLTindex = 1 + HLTindex
        if (codelist[i].find('HLT') != -1):
            break

    # التأكد من وجود الموجة END
    for i in range(len(codelist)):
        ENDindex = 1 + ENDindex
        if (codelist[i].find('END') != -1):
            break

    # تخزين كل عنوان ركزي في قاموس مع عنوانه الفعلي
    # التحقق من ان كان الامر RML or RDI or RHN
    # اذا كان الامر RML يتم خزن فراغ في عنوانه الفعلي
    # إرسال رسالة خطا اذا لا يوجد اي من هذه الموجهات ال 3
    lc = 0
    for i in range(HLTindex + 1, ENDindex):

        afterhlt.append(codelist[i])
        afterhlt[lc] = afterhlt[lc].split()
        errorcheck = linenumber[0] + i
        varaddres[afterhlt[lc][0]] = (
            '%2x' % (linenumber[0] + int(hex(i), 16))).strip()

        try:
            if (afterhlt[lc][1].find('RDI') != -1):
                if (int(afterhlt[lc][2]) < 0):
                    afterhlt[lc] = utils.twos(int(afterhlt[lc][2]))
                else:
                    afterhlt[lc] = ('%4x' % int(afterhlt[lc][2]))
            elif (afterhlt[lc][1].find('RML') != -1):
                afterhlt[lc] = '  '
            elif (afterhlt[lc][1].find('RHN') != -1):
                if (int(afterhlt[lc][2]) < 0):
                    afterhlt[lc] = utils.twos(int(afterhlt[lc][2]))
                else:
                    afterhlt[lc] = ('%4x' % int(afterhlt[lc][2], 16))
        except:
            message = "error none of these are found RDI,RHN and RML or a value  at line address" + \
                errorcheck + ':'+codelist[i]
            utils.log(message)
            messages.error(request, message)
            return []
        lc = lc + 1

    del codelist[HLTindex + 1:]

    # التأكد من اذا وجد اي LABEL FIELD
    # اذا وجد يتم خونه في قاموس مع عنوانه الفعلي للعودة اليه وقت الحاجه
    k = 0
    m = linenumber[0]
    lable = 0
    for i in codelist:
        if (i.startswith(instructions.MRI)) == False and (i.startswith(instructions.RRI)) == False:
            lable = i.find(' ')
            order = i[:lable]
            labledic[order] = m
            codelist[k] = i[lable+1:]
        m, k = m+1, k+1

    # التأكد من كل امر في الكود واعطاءة شفرته وايضا اعطاء موقع العنوان الرمزي ان وجد
    for i in range(len(codelist)):
        codelist[i] = codelist[i].split()

    for i in range(len(codelist)):
        for j in range(len(codelist[i])):
            if (codelist[i][j] in instructions.RRI) == True:
                codelist[i][j] = instructions.RRIsh[codelist[i][j]]
            elif (codelist[i][j] in varaddres.keys()) == True:
                codelist[i][j] = varaddres[codelist[i][j]]
            elif (codelist[i][j] in labledic.keys()) == True:
                codelist[i][j] = labledic[codelist[i][j]]
            elif (codelist[i][j] in instructions.MRI) == True:
                codelist[i][j] = instructions.MRIsh[codelist[i][j]]
            else:
                utils.log('non', i, j)

    # # تحويل الشفرات من النظام السداسي عشر الي النظام الثنائي لجعل الحاسوب عبارة عن 8 بت فقط
    codelist2 = []

    for i in range(len(codelist)):
        for j in range(len(codelist[i])):
            if len(codelist[i]) == 2:

                a = utils.hexToBinary(codelist[i][j])

                if len(a) == 2:
                    c = '00' + a
                elif len(a) == 3:
                    c = '0' + a
                else:
                    c = a

                b = utils.hexToBinary(codelist[i][j+1])

                # if len(b) == 1:
                #     d = '0000' + b
                # elif len(b) == 2:
                #     d = '000' + b
                # elif len(b) == 3:
                #     d = '00' + b
                # elif len(b) == 4:
                #     d = '0' + b
                # else:
                #     d = b

                codelist2.append(c.rjust(12, '0') + b.rjust(4, '0'))
                break

            codelist2.append(utils.hexToBinary(codelist[i][j]).rjust(16, '0'))

    # # تحويل الرقم 8 بت من الثنائي الى السداسي هشر مره اخرى ليمكن كتابته في التشفير
    codelist_print = []
    for i in range(len(codelist2)):
        codelist_print.append(utils.binaryToHex(codelist2[i]))

    for i in range(len(afterhlt)):
        codelist_print.append(afterhlt[i])
    utils.log(afterhlt)

    # ? Check that the number not exceding 12 bit
    for i in range(len(afterhlt)):
        item = afterhlt[i]
        if not item.isspace():
            binary_value = utils.hexToBinary(item.split()[0])
            if len(binary_value) > 12:
                message = "Please enter value less than 12 bit"
                utils.log(message)
                messages.error(request, message)
            
    codelist_print_out = []
    instructions_list = []
    instructions_encode_list = []
    address_encode_list = []
    variables_data_list = []

    # Get the code to a list
    for i in range(len(linenumber)):
        ADRESS = ('%02x' % linenumber[i])

        if (codelist_print[i] == '  '):
            HEX = '  '
        else:
            HEX = ('%04x' % int(codelist_print[i], 16))

        # print(ADRESS, '     ', HEX, '          ', copy_codelist[i])
        w = ADRESS + '     ' + HEX + '          ' + copy_codelist[i]
        instructions_list.append(copy_codelist[i])
        instructions_encode_list.append(HEX)
        address_encode_list.append(ADRESS)
        codelist_print_out.append(w+'\n')

    # File the instruction with empty value
    variables_data_list = [0] * (len(codelist_print_out)-len(varaddres))
    for i in range(len(afterhlt)):
        variables_data_list.append(afterhlt[i])

    return [
        codelist_print_out,
        instructions_list,
        instructions_encode_list,
        address_encode_list,
        varaddres,
        variables_data_list
    ]
