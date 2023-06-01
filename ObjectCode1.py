# import chardet
#
# from semantic import check_charset
# from 词法分析 import lexical_Analysis
# from 语义分析 import semantic_analysis
import re

regex = r"\[(\w+)]"

global_main_symbol = []
# 除main函数外其他函数里参数 以及对应的ss:[bp+n]， 局部变量  以及对应的ss:[bp-n]     sub sp n    n的值为局部变量个数*2
function = {}
function_array = {}

# {函数1：[]，函数2：[]}                 #  n=参数个数*2+2  [{参数1：'ss:[bp+n]',参数2:'ss:[bp+n-2]'...} ,{局部变量1:'ss:[bp-2]',局部变量2:'ss:[bp-2-2]'}]

def is_var(s):
    state = '0'
    for ch in s:
        if state == '0':
            if ch.isalpha() or ch == '_':
                state = '1'
            else:
                return False
        elif state == '1':
            if ch.isalnum() or ch == '_':
                state = '1'
            else:
                return False
    return True


function_param_list = {}
function_jubu_list = {}
function_array_list = {}
global_array_list = []
temporary_address = {}
temporary = {}


def function_get(quaternion_list):
    sys = quaternion_list.index(['sys', '_', '_', '_'])
    # function_param_list 函数声明
    # 不知道参数名字 [{参数1：'ss:[bp+n]',参数2:'ss:[bp+n-2]'...} ,{局部变量1:'ss:[bp-2]',局部变量2:'ss:[bp-2-2]'}]

    for i, v in function_param_list.items():  # i是函数名 v对应参数名
        # function[i][0]存参数字典 参数以及ss值 function[i][1]存局部变量
        function_array[i] = {}
        function[i] = [{}, {}]
        for j in v:
            function[i][0][j] = '_'
    # 遍历四元式
    for i, line in enumerate(quaternion_list[0:sys+1]):  # i从0标号 line[1:]
        if line[0] not in ['jnz', 'para', 'call', 'j', 'jz', 'j<', 'j>', 'j<=', 'j>=', 'j==', 'j!=']:  # 如果不是跳转语句 不是函数调用
            for var in line[1:]:  # 全局变量表添加
                print('line1',line[1:])
                if is_var(var) and var not in global_main_symbol + ['_'] and var[0] != 'T':
                    global_main_symbol.append(var)
    print(global_main_symbol)

    num = 0
    f_name = ''
    for i in quaternion_list[sys+1:]:
        if i[0] in function_jubu_list:
            f_name = i[0]
            temporary[f_name] = []
            num = len(function_jubu_list[f_name])*2+2
        for j in i[1:]:
            if str(j)[0] == 'T' and j not in temporary[f_name]:
                temporary[f_name].append(j)
                temporary_address[j] = 'ss:[bp-%s]' % num
                num += 2

    for i, v in function_jubu_list.items():  # i是函数名 v对应参数名
        # function[i] = [{}, {}] #function[i][0]存参数字典 参数以及ss值 function[i][1]存局部变量
        for j in v:
            function[i][1][j] = '_'

    for i, v in function.items():
        print(len(function[i][0]))
        print(len(function[i][1]))
        n = (len(function[i][0]) + len(function[i][1])) * \
            2 + 6  # BP+0:原BP的值 BP+2:返回地址 BP+4:返回值
        for s, vv in enumerate(function[i][0].keys()):
            function[i][0][vv] = 'ss:[bp+' + \
                str(4 + (s * 2)) + ']'  # bp+4 bp+6 实参
        for s, vv in enumerate(function[i][1].keys()):
            function[i][1][vv] = 'ss:[bp-' + \
                str(2 + (s * 2)) + ']'  # BP-2 Bp-4  临时变量
    for i in function_array_list:
        length = len(function[i][1])*2+2+len(temporary[i])*2
        for j in function_array_list[i]:
            function_array[i][j[0]] = length
            if j[2] == '':
                length += int(j[1])*2
            else:
                length += int(j[1])*int(j[2])*2
    '''
   {'sum': [{'sum_x': 'ss:[bp+4]', 'sum_y': 'ss:[bp+6]'}, {'result': 'ss:[bp-2]'}], 
   'max': [{'m_x': 'ss:[bp+6]', 'm_y': 'ss:[bp+8]'}, {'result': 'ss:[bp-2]'}]}
    '''
    print('function', function)


def array_address1(fun_name1, name):
    print(function_array_list)
    print(function_array)
    if fun_name1 != '**':
        if '[' in name:
            match = re.findall(regex, name)
            t = match[0]
            p = ''
            if t[0] == 'T':
                p = temporary_address[t]  # 'es:[' + str(int(t[1:]) * 2) + ']'
            elif t.isdigit():
                p = t
            elif t in function[fun_name][1]:
                p = function[fun_name][1][t]
            else:
                p = function[fun_name][0][t]
            return 'lea si, [bp - %d]\n\tmov di, %s\n\tshl di, 1\n\tsub si, di\n\t'%(int(function_array[fun_name1][name[:name.index('[')]]), p)
    else:
        if '[' in name:
            match = re.findall(regex, name)
            t = match[0]
            p = ''
            if t[0] == 'T':
                p = 'es:[' + str(int(t[1:]) * 2) + ']'
            elif t.isdigit():
                p = t
            else:
                p = '_' + t
            return 'lea si, [_%s]\n\tmov di, %s\n\tshl di, 1\n\tadd si, di\n\t' % (name[:name.index('[')], p)
    return ''


def target_code(four_table):
    global s
    global fun_name  # 根据中间代码来确定当前执行的函数名
    global global_array_list
    print(function)
    fun_name = '**'
    f = open('./target/data_segment.txt', 'r')
    s = f.read()
    for i in global_main_symbol:
        s += '\t_' + i + ' dw 0\n'
    for i in global_array_list:
        if i[2] == '':
            s += '\t_' + i[0] + ' dw %d dup(0)\n' % int(i[1])
        else:
            s += '\t_' + i[0] + ' dw %d dup(0)\n' % (int(i[1])*int(i[2]))
    f.close()
    f = open('./target/code_segment1.txt', 'r')
    s1 = f.read()
    s += s1
    f = open('./target/code_segment2.txt', 'r')
    rear = f.read()
    f.close()
    fun_name = '**'
    for i, line in enumerate(four_table):
        one = four_table[i][0]
        if one == 'main':  # main函数 跳过main四元式 不对main进行翻译
            continue
        two = str(four_table[i][1])
        three = str(four_table[i][2])
        four = str(four_table[i][3])
        two1 = two
        three1 = three
        four1 = four
        if one not in ['j']:  # 不是跳转语句
            '''
            先查看数据是否在当前函数栈中 在查看是否在全局作用域中
            '''
            if fun_name != '**' and '[' in two:
                two = 'ss:[si]'
            elif fun_name == '**' and '[' in two:
                two = '[si]'
            if fun_name != '**' and '[' in three:
                three = 'ss:[si]'
            elif fun_name == '**' and '[' in three:
                three = '[si]'
            if fun_name != '**' and '[' in four:
                four = 'ss:[si]'
            elif fun_name == '**' and '[' in four:
                four = '[si]'
            if fun_name != '**' and two in function[fun_name][0]:  # 当前为函数 使用的值在该函数栈里面 形参
                print(function[fun_name][0])
                two = function[fun_name][0][two]
            elif fun_name != '**' and two in function[fun_name][1]:  # 函数内局部变量
                two = function[fun_name][1][two]
            elif two != '_' and two in global_main_symbol:  # 从ds取出数据
                two = 'ds:[_' + two + ']'
            elif two[0] == 'T' and fun_name == '**':  # 将临时变量放到es T1对应es:[2]  每个临时变量占用两个
                # 用变量序号作为存放es的地址值 每个变量都不一样 所以不会被冲掉 四元式不会出现(+,T0,T0,T1)这种情况
                two = 'es:[' + str(int(two[1:]) * 2) + ']'
            elif two[0] == 'T':
                two = temporary_address[two]
            # 对函数的参数进行处理
            if fun_name != '**' and three in function[fun_name][0]:
                three = function[fun_name][0][three]
            elif fun_name != '**' and three in function[fun_name][1]:
                three = function[fun_name][1][three]
            elif three != '_' and three in global_main_symbol:
                three = 'ds:[_' + three + ']'
            elif three[0] == 'T' and fun_name == '**':  # 将临时变量放到es区
                three = 'es:[' + str(int(three[1:]) * 2) + ']'
            elif three[0] == 'T':
                three = temporary_address[three]
            if fun_name != '**' and four in function[fun_name][0]:
                four = function[fun_name][0][four]
            elif fun_name != '**' and four in function[fun_name][1]:
                four = function[fun_name][1][four]
            elif four != '_' and four in global_main_symbol:
                four = 'ds:[_' + four + ']'
            elif four[0] == 'T' and fun_name == '**':
                four = 'es:[' + str(int(four[1:]) * 2) + ']'
            elif four[0] == 'T':
                four = temporary_address[four]
        print(2222222222222222222222222222222222,
              one, two, three, four, fun_name)

        if one == '=':
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV AX,' + two + \
                '\n\t' + array_address1(fun_name,four1) + 'MOV ' + four + ',AX\n'
        elif one == '+':
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +\
                'ADD AX,' + three + '\n\t' + array_address1(fun_name,four1) +'MOV ' + four + ',AX\n'
        elif one == '-' or one == '@':  # 对负号进行处理
            if three == '_':
                three1 = two1
                two1 = '_'
                three = two
                two = '0'
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +\
                'SUB AX,' + three + '\n\t' + array_address1(fun_name,four1) +'MOV ' + four + ',AX\n'
        elif one == '*':
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'MOV BX,' + three + '\n\t' + 'MUL BX\n\t' + array_address1(fun_name,four1) +'MOV ' + four + ',AX\n'
        elif one == '/':
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) + 'MOV DX,0\n\t' + 'MOV BX,' + three + '\n\t' + array_address1(fun_name,four1) +'DIV BX\n\t' + 'MOV ' + four + ',AX\n'
        elif one == '%':
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + 'MOV DX,0\n\t' + array_address1(fun_name,three1) +'MOV BX,' + three + '\n\t' + 'DIV BX\n\t' + array_address1(fun_name,four1) +'MOV ' + four + ',DX\n'
        elif one == '<':
            s += '_%d:\t' % (
                i) + array_address1(fun_name, two1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + array_address1(
                fun_name, three1) + 'CMP AX,' + three + '\n\t' + 'JA _GT_' + str(
                i) + '\n\t' + array_address1(fun_name, four1) + 'MOV DX,0\n' + '_GT_' + str(
                i) + ':\tMOV ' + four + ',DX\n'
        elif one == 'j<':  # 1
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,' + three + '\n\t' + array_address1(fun_name,four1) + 'jl _%s\n' % four
        elif one == '>=':
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,' + three + '\n\t' + array_address1(fun_name,four1) +'JNB _GE_' + str(
                i) + '\n\t' + 'MOV DX,0\n' + '_GE_' + str(i) + ':\tMOV ' + four + ',DX\n'
        elif one == 'j>=':  # 2
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) + 'CMP AX,' + three + '\n\t' + array_address1(fun_name,four1) +'jge _%s\n' % four
        elif one == '>':
            s += '_%d:\t' % (
                i) + array_address1(fun_name, two1) + 'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + array_address1(
                fun_name, three1) + 'CMP AX,' + three + '\n\t' + 'JB _LT_' + str(
                i) + '\n\t' + array_address1(fun_name, four1) + 'MOV DX,0\n' + '_LT_' + str(
                i) + ':\tMOV ' + four + ',DX\n'

        elif one == 'j>':  # 3
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) + 'CMP AX,' + three + '\n\t' + array_address1(fun_name,four1) +'jg _%s\n' % four
        elif one == '<=':  # (j<=,A,B,P)
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,' + three + '\n\t' + 'JNA _LE_' + str(
                i) + '\n\t' + array_address1(fun_name,four1) +'MOV DX,0\n' + '_LE_' + str(i) + ':\tMOV ' + four + ',DX\n'
        elif one == 'j<=':  # (j<=,A,B,P) 4
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,' + three + '\n\t' + array_address1(fun_name,four1) +'jle _%s\n' % four
        elif one == '==':
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,' + three + '\n\t' + 'JE _EQ_' + str(
                i) + '\n\t' + array_address1(fun_name,four1) + 'MOV DX,0\n' + '_EQ_' + str(i) + ':\tMOV ' + four + ',DX\n'
        elif one == 'j==':  # 5
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,' + three + '\n\t' + array_address1(fun_name,four1) +'je _%s\n' % four
        elif one == '!=':
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,' + three + '\n\t' + 'JNE _NE_' + str(
                i) + '\n\t' + array_address1(fun_name,four1) + 'MOV DX,0\n' + '_NE_' + str(i) + ':\tMOV ' + four + ',DX\n'
        elif one == 'j!=':  # 6
            s += '_%d:\t' % (
                i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,' + three + '\n\t' + array_address1(fun_name,four) +'jne _%s\n' % four
        elif one == '&&':
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) + 'MOV DX,0\n\t' + 'MOV AX,' + two + '\n\t' + array_address1(fun_name,three1) +'CMP AX,0\n\t' + 'JE _AND_' + str(
                i) + '\n\t' + 'MOV AX,' + three + '\n\t' + array_address1(fun_name,four1) +'CMP AX,0\n\t' + 'JE _AND_' + str(
                i) + '\n\t' + 'MOV DX,1\n' + '_AND_' + str(i) + ':\tMOV ' + four + ',DX\n'
        elif one == '||':
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JNE _OR_' + str(
                i) + '\n\t' + array_address1(fun_name,three1) +'MOV AX,' + three + '\n\t' + 'CMP AX,0\n\t' + 'JNE _OR_' + str(
                i) + '\n\t' + array_address1(fun_name,four1) +'MOV DX,0\n' + '_OR_' + str(i) + ':\tMOV ' + four + ',DX\n'
        elif one == '!':
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV DX,1\n\t' + 'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JE _NOT_' + str(
                i) + '\n\t' + array_address1(fun_name,four1) +'MOV DX,0\n' + '_NOT_' + str(i) + ':\tMOV ' + four + ',DX\n'
        elif one == 'j':
            gg = '_' + str(int(four))
            if four_table[int(four)][0] == 'sys':
                gg = 'quit'
            s += '_%d:\t' % (i) + 'JMP far ptr ' + gg + '\n'
        elif one == 'jz':
            gg = '_' + str(int(four))
            if four_table[int(four)][0] == 'sys':
                gg = 'quit'
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JNE _NE_' + str(
                i) + '\n\t' + 'JMP far ptr ' + gg + '\n' + '_NE_' + str(i) + ':\tNOP\n'
        elif one == 'jnz':
            gg = '_' + str(int(four))
            if four_table[int(four)][0] == 'sys':
                gg = 'quit'
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + 'CMP AX,0\n\t' + 'JE _EZ_' + str(
                i) + '\n\t' + 'JMP far ptr ' + gg + '\n' + '_EZ_' + str(i) + ':\tNOP\n'
        elif one == 'para':
            '''
            第二个参数->BP+4
            第一个参数->BP+6
            '''
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + 'PUSH AX\n'
        elif one == 'call':
            two = str(four_table[i][1])
            s += '_%d:\t' % (i) + 'CALL ' + two + '\n'
            if four != '_':
                s += '\tMOV ' + four + ',AX\n'
        elif one == 'ret' and two != '_':
            # 返回结果放到AX中
            # 'MOV SP,BP' 把BP的数据送到SP
            s += '_%d:\t' % (i) + array_address1(fun_name,two1) +'MOV AX,' + two + '\n\t' + \
                'MOV SP,BP\n\t' + 'POP BP\n\t' + 'RET '
            # if four != '_':
            #     s += str(len(function[fun_name][0]) * 2)  # ret 后的数字是参数个数*2  即参数区的大小 返回原来地址
            s += '\n'
        elif one == 'ret':
            s += '_%d:\t' % (i) + 'MOV SP,BP\n\t' + 'POP BP\n\t' + 'RET\n'
        elif one == 'sys':  # 不用进行标号 我们只在main执行结束写了sys四元式
            s += 'quit:\t' + 'mov ah,4ch\n\t' + 'int 21h\n'
        else:  # (fun_name,_,_,_) 进入函数定义
            fun_name = one
            print(fun_name)
            # s += one + ':\t' + 'PUSH BP\n\t' + 'MOV BP,SP\n\t' + 'SUB SP,' + 100 + '\n'
            '''
            PUSH BP:将BP原来指向的地址值压进栈，将BP保存起来 
            MOV BP,SP:移动BP到SP 
            SUB SP: SP向上移动 
            '''
            length = 0
            if len(function_array_list) != 0:
                for i in function_array_list[fun_name]:
                    if i[2] == '':
                        length = int(i[1])*2
                    else:
                        length = int(i[1]) * int(i[2]) * 2
            s += one + ':\t' + 'PUSH BP\n\t' + 'MOV BP,SP\n\t' + 'SUB SP,' + \
                str(len(function[fun_name][1]) * 2+length+len(temporary[fun_name])*2) + '\n'  # 根据局部变量的个数 确定栈顶位置
            print('000000000000000000000000000000')
            print(len(function[fun_name][1]) * 2)
            print(length)
            print(one + ':\t' + 'PUSH BP\n\t' + 'MOV BP,SP\n\t' +
                  'SUB SP,' + str(len(function[fun_name][1]) * 2+length+len(temporary[fun_name])*2) + '\n')
    return s + rear


def get_target_code(mid_result):
    global global_main_symbol, function, quaternion_list, symbol_constant_list, symbol_variable_list, symbol_function_list, func_param_list, function_param_list
    quaternion_list, symbol_constant_list, symbol_variable_list, symbol_function_list, function_param_list = mid_result
    global_main_symbol = []
    function = {}
    function_get(quaternion_list)
    target_code_list = target_code(quaternion_list)
    print('-------------------------')
    print(function)
    return target_code_list


def solve(function_param_list1, function_jubu_list1, siyuanshi1, function_array_list1, global_array_list1):
    global global_main_symbol, function, function_param_list, function_jubu_list, function_array_list, global_array_list
    # 初始化
    global_main_symbol = []
    # 除main函数外其他函数里参数 以及对应的ss:[bp+n]， 局部变量  以及对应的ss:[bp-n]     sub sp n    n的值为局部变量个数*2
    function = {}
    function_param_list = function_param_list1
    function_jubu_list = function_jubu_list1
    function_array_list = function_array_list1
    print('99999999999999999')
    print(function_array_list)
    global_array_list = global_array_list1
    print("function_param_list", function_param_list)
    print("function_jubu_list", function_jubu_list)
    quaternion_list = siyuanshi1
    print(quaternion_list)
    symbol_variable_list = []
    function_get(quaternion_list)
    target_code_list = target_code(quaternion_list)
    print('-------------------------')
    print(function)
    print(target_code_list)
    return target_code_list

    # Filepath = "D:\pythonProject\pythonProject\新版编译器测试用例\\test1.txt"
    # code = open(Filepath, encoding=check_charset(Filepath)).read()
    # Assemble = lexical_Analysis(code)
    # ans, err = Assemble.display_result()
    #
    # ll, token_information = Assemble.obtain_result()
    # token_information.append([token_information[-1][0] + 1, -1, -1, '#end#', -1])
    # for i in range(len(token_information)):
    #     print(token_information[i])
    # test = semantic_analysis(token_information)
    # test.program(0)
    # test.quaternion_changeT()
    # [print(i, k) for i, k in enumerate(test.quaternion_list)]
    # function_param_list=test.function_param_table


# a = [ ['main', '_', '_', '_'], ['call', 'read', '_', 'T0'], ['=', 'T0', '_', 'N'], ['call', 'read', '_', 'T1'], ['=', 'T1', '_', 'M'], ['>=', 'M', 'N', 'T2'], ['jnz', 'T2', '_', 9], ['jz', 'T2', '_', 11], ['=', 'M', '_', 'result'], ['j', '_', '_', 12], ['=', 'N', '_', 'result'], ['+', 'result', '100', 'T3'], ['=', 'T3', '_', 'a'], ['para', 'a', '_', '_'], ['call', 'write', '_', 'T4'], ['sys', '_', '_', '_']]

# print(a)
