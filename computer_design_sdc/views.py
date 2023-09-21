from django.shortcuts import render
from django.contrib import messages
import os

from computer_design_sdc.utils import utils, assembling, instruction_activity
from sdc.settings import BASE_DIR
# Create your views here.


def index(request):
    if request.method == 'POST':
        assembly = assembling.Assembling(
            request.POST['data_python_input'], request)
        utils.log(assembly.assembly)

        output_data = ''
        a_reg = ''
        b_reg = ''
        a_reg_log = ''
        b_reg_log = ''

        # Other register
        other_reg_caption = ''
        other_reg_data = ''

        if len(assembly.assembly) > 0:
            output_data = ''.join(map(str, assembly.assembly[0]))
            b = instruction_activity.AssemblingActivity(
                assembly.assembly, request)

            registers = utils.get_registers_data()
            utils.log(registers)
            a_reg = registers[0]
            b_reg = registers[1]
            a_reg_log = registers[2]
            b_reg_log = registers[3]

            # Other register
            other_reg_caption = registers[4]
            other_reg_data = registers[5]

        return render(request, 'home/index.html', {
            'output': output_data,
            'a_reg': a_reg,
            'b_reg': b_reg,
            'a_reg_log': a_reg_log,
            'b_reg_log': b_reg_log,
            'other_reg_caption': other_reg_caption,
            'other_reg_data': other_reg_data,

            'input': request.POST['data_python_input']
        })
    else:
        return render(request, 'home/index.html')
