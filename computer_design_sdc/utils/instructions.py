MRI = ('LDA',  # 0
       'STA',  # 1
       'JMP',  # 2
       'LAI',  # 3
       'SAI',  # 4
       'JMI',  # 5
       'ISZ'  # 6
       )  # tuple that has the MRI set

RRI = ('CMA',  # 0
       'INA',  # 1
       'CLA',  # 2
       'ADD',  # 3
       'XOR',  # 4
       'AND',  # 5
       'OR',  # 6
       'SAZ',  # 7
       'SAP',  # 8
       'SAN',  # 9
       'HLT',  # 10
       'MAB',  # 11
       'MBA'  # 12
       )

CONTROL_MRI = ('JMP',  # 0
               'JMI',  # 1
               'ISZ',  # 2
               )

CONTROL_RRI = ('SAZ',  # 0
               'SAP',  # 1
               'SAN',  # 2
               )

MRIsh = {'LDA': '111', 'STA': '121', 'JMP': '131',
         'LAI': '141', 'SAI': '151', 'JMI': '161', 'ISZ': '171'}

RRIsh = {'CMA': '1ED0', 'INA': '2EC1', 'CLA': '3EB2', 'ADD': '4EA3', 'XOR': '5E94', 'AND': '6E85', 'OR': '7E76',
         'SAZ': '8E67', 'SAP': '9E58', 'SAN': 'AE49', 'HLT': 'BE3A', 'MAB': 'CE2B', 'MBA': 'DE1C'}
