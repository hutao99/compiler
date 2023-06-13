from FirstAndFollow import first_dict, follow_dict, print_dic, kong  # 从字典文件中导入first集 follow集 以及字典映射关系
from Symbol_Table import node1, node2, VariableSymbolTable, FunctionSymbolTable, CreateTableFlag
from graphviz import Digraph
from suanfu import Suanfufirst
import copy

"""
中间代码:
编号 运算符 第一个 第二个 变量
"""


# pyecharts
class recDesc_analysis:
    def __init__(self, file):
        self.text1 = ""
        self.text2 = ""
        self.grammer = {}  # 保存非终结符对应的函数
        self.vn = []  # 非终结符
        self.goal_str = ""  # 输入文本字符串
        self.goal_list = []  # 输入字符串列表
        self.p = 0  # 字符串列表指针
        self.len = 0  # 字符串列表长度
        self.scope = '0'  # 作用域标记
        self.area = 0  # 作用域标记
        self.Tid = 0  # 临时变量标记
        self.count = 0
        self.node_number = 0  # 语法树节点编号
        self.warnings_str = ''  # 语义错误信息
        self.syntax_error = ""  # 语法错误信息
        self.main_flag = 0
        self.quaternions = []
        self.sym_flag = CreateTableFlag()  # 声明标记
        self.shengmingflag = 0  # 0 表示不是声明语句 1表示为常量声明 2表示为变量声明 3表示为函数声明
        self.suan_process = Suanfufirst()
        self.sym1 = VariableSymbolTable()  # 常量变量符号表
        self.sym2 = FunctionSymbolTable()  # 函数符号表
        self.str1 = Stack()  # 表达式元素列表 [[]]
        self.str2 = Stack()  # 表达式元素值
        self.str_type = Stack()  # 表达式元素类型
        self.expression_shengming = 0
        self.expression_list = Stack()  # [类型 值]
        self.assignment_list = Stack()  # 赋值语句嵌套赋值语句 [类型 值 行号 作用域]
        self.func_call_namelist = Stack()  # 函数调用嵌套函数调用 因此记录名字 [行号 函数调用名 函数返回类型]
        self.func_call_argulist = Stack()  # 函数调用嵌套实参类型
        self.func_call_flag = 0  # 调用的函数名字
        self.if_FC = Stack()
        self.if_SC = Stack()
        self.dowhile_head = Stack()
        self.dowhile_FC = Stack()
        self.while_FC = Stack()
        self.while_head = Stack()
        self.xunhuan = Stack()
        self.for_TEST = Stack()
        self.for_INC = Stack()
        # self.for_AGAIN = Stack()  # [,,]
        self.for_TC = Stack()
        self.for_FC = Stack()  # break,表达式不满足 [[],[]]
        self.func_define_flag = 0
        self.return_flag = 0
        self.return_value = 0
        self.p4_assignment = 0
        self.fun_list = []  # 存储函数
        self.function_param_list = {}  # 存储函数以及对应参数
        self.function_jubu_list = {}
        self.function_parameter_defines = ['', '', [], [], '']  # 函数定义 函数名 函数类型 函数形参类型 函数形参名字 函数定义行号
        self.repetition_type = 0
        self.return_exp = False # 表达式返回值
        self.main_return_id = [] #main中return回填
        self.is_main = False # 当前是否在main函数中
        self.cur_func_type = [None,None] #当前的函数及其返回类型
        for line in file.readlines():
            div_list = line.strip('\n').split('->')
            # print('===============')
            # print(div_list)
            if div_list[0][0:2] not in self.grammer.keys():
                self.grammer[div_list[0][0:2]] = []
            self.grammer[div_list[0][0:2]].append(div_list[1])

            line = line.strip('\n')
            line = line.replace('|', ' ')
            line = line.split()  # 获取字符串中的所有元素 提取终结符
            for ch in line:
                if ch != 'r' and len(ch) == 2 and ch[1].isdigit():
                    if ch[0].isalpha() and ch not in self.vn:  # 大写字母 即非终结符
                        self.vn.append(ch)

    def match(self, ch, fabian):
        """ 递归下降进行匹配，通过模拟所有的非终结符的子程序模块 """
        if self.p >= len(self.goal_list):
            return 1
        if self.shengmingflag:
            if (ch == 'm2' or ch == 'm3') and not self.func_call_flag and self.sym_flag.name != None:  # m2常量 m3变量
                self.add_sym()
        if ch == 'A2':
            self.shengmingflag = 2  # 标记进行声明语句
            if (self.p + 2) < self.len and self.goal_list[self.p + 2][1] == '(':
                self.shengmingflag = 3  # 超前搜索 标记函数声明
        if ch == 'D4':  # 表达式相关处理
            self.str1.push(Stack())
            self.str2.push(Stack())
            self.expression_shengming = 1

        if ch == 'I1':  # if 语句
            self.if_SC.push([])
            self.if_FC.push([])
        if ch == 'I3':  # while语句
            self.xunhuan.push('while')
            self.while_head.push(self.count)
            self.while_FC.push([])
        if ch == 'I4':  # dowhile语句
            self.xunhuan.push('dowhile')
            self.dowhile_head.push(self.count)
            self.dowhile_FC.push([])
        if ch == 'I2':  # for语句
            self.xunhuan.push('for')
            flag = 0  # 判断是第几个出现的表达式 表达式1；表达式2；表达式3
            self.for_FC.push([])  # break,表达式不满足 [[],[]]
        if ch == 'A5':  # 函数定义
            self.func_define_flag = 1
        if ch == 'I5' and self.goal_list[self.p][1] == 'return':  # return 语句
            self.return_flag = 1
            if self.p+1 < self.len and self.goal_list[self.p+1][1]!=';':
                self.return_exp = True
        # print(self.goal_list[self.p][1], '----', ch,'-----',self.grammer[ch])
        for i in range(len(self.grammer[ch])):
            # 如果当前token在self.grammer[ch][i] first中，则递归。如无，则continue;
            if self.goal_list[self.p][1] in first_dict[ch][i] or self.goal_list[self.p][2] in first_dict[ch][i]:
                rule = self.grammer[ch][i]
                record_p = self.p  # 记录指针位置，方便回溯
                for item in rule:
                    # print(item,'-----------------',self.goal_list[self.p][1],self.goal_list[self.p][2],self.shengmingflag)
                    if ch == 'I1':  # if语句处理
                        if item == ')':  # if表达式真假出口表示
                            self.quaternions.append(
                                [self.count, 'jnz', 'T%s' % (self.Tid - 1), '_', self.count + 2])  # if条件语句不为0 则跳转到下一条
                            self.count += 1
                            self.quaternions.append([self.count, 'jz', 'T%s' % (self.Tid - 1), '_', 0])  # if条件语句为0
                            self.if_FC.gettop().append(self.count)
                            self.count += 1
                        elif item == 'm9':
                            self.quaternions.append([self.count, 'j', '_', '_', 0])  # if条件语句不为0 则跳转到chukou
                            self.if_SC.gettop().append(self.count)
                            self.count += 1
                            for i in self.if_FC.gettop():
                                self.quaternions[i][4] = self.count
                            self.if_FC.pop()
                    if ch == 'I4':  # do while语句处理
                        if item == ')':
                            self.quaternions.append(
                                [self.count, 'jnz', 'T%s' % (self.Tid - 1), '_', self.dowhile_head.gettop()])  #
                            self.dowhile_head.pop()
                            self.count += 1
                            self.quaternions.append([self.count, 'jz', 'T%s' % (self.Tid - 1), '_', self.count + 1])  #
                            self.count += 1
                            for i in self.dowhile_FC.gettop():
                                self.quaternions[i][4] = self.count
                            self.dowhile_FC.pop()
                            self.xunhuan.pop()
                    if ch == 'I3':  # while语句处理
                        if item == ')':
                            self.quaternions.append([self.count, 'jnz', 'T%s' % (self.Tid - 1), '_',
                                                     self.count + 2])  # 表达式为真 则跳转到下下条四元式
                            self.count += 1
                            self.quaternions.append(
                                [self.count, 'jz', 'T%s' % (self.Tid - 1), '_', 0])  # if条件语句为0
                            self.while_FC.gettop().append(self.count)  # 待回填
                            self.count += 1
                    if ch == 'I2':  # for 语句
                        if flag == 0 and item == 'D4':
                            flag = 1
                            temp = self.goal_list[self.p][1]
                        elif flag == 1 and item == 'D4':  # 第二句的入口
                            x1 = self.expression_list.gettop()
                            self.expression_list.pop()
                            x2 = self.expression_list.gettop()
                            self.expression_list.pop()
                            self.expression_list.push(x2)
                            self.expression_list.push(x1)
                            self.quaternions.append([self.count, '=', x2[1], '_', temp])
                            self.count += 1
                            self.for_TEST.push(self.count)
                            flag = 2
                            # 为表达式添加跳转语句
                        elif flag == 2 and item == ';':
                            temp = self.goal_list[self.p + 1][1]
                            self.quaternions.append(
                                [self.count, 'jnz', 'T%s' % (self.Tid - 1), '_', 0])  # if条件语句不为0 则跳转到下一条
                            self.for_TC.push(self.count)
                            self.count += 1
                            self.quaternions.append([self.count, 'jz', 'T%s' % (self.Tid - 1), '_', 0])  # if条件语句为0
                            self.for_FC.gettop().append(self.count)
                            self.count += 1
                        elif flag == 2 and item == 'D4':  # 添加测试入口
                            self.for_INC.push(self.count)
                        elif item == ')':
                            x1 = self.expression_list.gettop()
                            self.expression_list.pop()
                            x2 = self.expression_list.gettop()
                            self.expression_list.pop()
                            self.expression_list.push(x2)
                            self.expression_list.push(x1)
                            self.quaternions.append([self.count, '=', x2[1], '_', temp])
                            self.count += 1
                            # 为表达式添加跳转语句
                            self.quaternions.append([self.count, 'j', '_', '_', self.for_TEST.gettop()])  # 跳回测试条件
                            self.count += 1
                            self.quaternions[self.for_TC.gettop()][4] = self.count
                            self.for_TC.pop()
                    '''
                    函数定义形参:个数和类型要保证和函数声明一致
                    '''
                    if ch == 'A5':  # 函数定义
                        if item == 'A6':  # 函数类型
                            function_type = self.goal_list[self.p][1]
                            self.cur_func_type[0] = function_type
                            self.function_parameter_defines[0] = function_type
                            self.function_parameter_defines[4] = self.goal_list[self.p][0]
                        elif item == 'A7':  # 标识符
                            self.func_define_flag = 1  # 函数定义标志 记录函数体形参及变量
                            function_name = self.goal_list[self.p][1]
                            self.cur_func_type[1] = function_name
                            self.function_jubu_list[function_name] = []
                            self.function_param_list[function_name] = []
                            self.fun_list.append(function_name)
                            self.quaternions.append([self.count, function_name, '_', '_', '_'])
                            self.count += 1
                            function_name = self.goal_list[self.p][1]
                            self.function_parameter_defines[1] = function_name
                        elif item == '(':
                            self.func_define_flag = 2
                        elif item == ')':
                            if len(self.function_parameter_defines[0]) != 0:
                                self.check_function_define()  # 检查形参列表
                            self.function_parameter_defines = ['', '', [], [], '']  # 函数定义形参列表清0
                            self.func_define_flag = 1
                    if ch == 'B1':  # 函数定义形参列表
                        if item == 'B2':  # 变量类型
                            type = self.goal_list[self.p][1]
                            self.function_parameter_defines[2].append(type)
                        elif item == 'A7':  # 标识符
                            name = self.goal_list[self.p][1]
                            self.function_parameter_defines[3].append(name)
                        elif item == 'm1':
                            self.shengmingflag = 2
                            self.add_sym()
                            self.shengmingflag = 0
                    '''
                    函数调用 嵌套调用 表达式赋值 形参类型
                    表达式类型相加 返回类型 表达式添加的时候需要添加类型 额外扩充一个
                    '''
                    if ch == 'p4': # p4 -> = D4 ; | ( H1 ) ;
                        if item == '=':  # 对赋值进行处理
                            self.p4_assignment = 1
                            assignment_type = self.goal_list[self.p - 2][1]
                            assignment_type = self.sym1.get_type(self.goal_list[self.p - 1][1],self.scope)
                            self.assignment_list.push(
                                [assignment_type, self.goal_list[self.p - 1][1], self.goal_list[self.p - 1][0],self.scope])
                        elif self.p4_assignment and item == ';':
                            self.p4_assignment = 0
                            if not self.expression_list.empty() and not self.assignment_list.empty():
                                if self.sym1.if_constant(self.assignment_list.gettop()[1],self.assignment_list.gettop()[3]):
                                    self.warnings_str += "Warning: 第%s行 不能对常量%s赋值\n" % (
                                        self.assignment_list.gettop()[2], self.assignment_list.gettop()[1])
                                if not self.if_match_format(self.expression_list.gettop()[0],
                                                            self.assignment_list.gettop()[0]):
                                    self.warnings_str += "Warning: 第%s行 %s等号两边格式不匹配\n" % (
                                    self.assignment_list.gettop()[2], self.assignment_list.gettop()[1])
                                self.quaternions.append([self.count, '=', self.expression_list.gettop()[1], '_',
                                                         self.assignment_list.gettop()[1]])
                                self.expression_list.pop()
                                self.count += 1
                                self.assignment_list.pop()
                        elif not self.p4_assignment and item == '(':
                            self.func_call_flag = 1  # 函数调用标记
                            func_line = self.goal_list[self.p - 1][0]
                            func_name = self.goal_list[self.p - 1][1]
                            func_return_type = self.sym2.get_func_type(func_name)
                            self.func_call_namelist.push([func_line, func_name, func_return_type])  # 行号 函数名 函数类型
                            self.func_call_argulist.push([])

                        elif not self.p4_assignment and item == ')':
                            self.quaternions.append(
                                [self.count, 'call', self.func_call_namelist.gettop()[1], '_', 'T%s' % self.Tid])
                            self.Tid += 1
                            self.count += 1
                            if self.func_call_flag:
                                self.check_function_call()
                            self.func_call_namelist.pop()
                            self.func_call_flag = 0

                    if (ch == 'm2' or ch == 'm3'):
                        if item == ',':
                            self.repetition_type = 1
                        elif item == ';':
                            self.repetition_type = 0
                    if ch == 'n4' and item == '=':  # 进入声明等于
                        if self.repetition_type:
                            assignment_type = self.sym_flag.type
                        else:
                            assignment_type = self.goal_list[self.p - 2][1]
                        self.assignment_list.push(
                            [assignment_type, self.goal_list[self.p - 1][1], self.goal_list[self.p - 1][0],self.scope])
                    if ch == 'C8' and item == '=':  # 常量声明表等于
                            self.expression_list.push([self.goal_list[self.p+1][2],self.goal_list[self.p+1][1]]) #type 值
                            if self.repetition_type:
                                assignment_type = self.sym_flag.type
                            else:
                                assignment_type = self.goal_list[self.p - 2][1]
                            self.assignment_list.push(
                                [assignment_type, self.goal_list[self.p - 1][1], self.goal_list[self.p - 1][0]])  # 类型 名字 行号
                    if ch == 'p1':  # 函数调用 实参列表
                        if item == '(':
                            self.func_call_flag = 1
                            func_name = self.goal_list[self.p - 1][1]
                            func_type = self.sym2.get_func_type(func_name)
                            func_line = self.goal_list[self.p - 1][0]
                            self.func_call_namelist.push([func_line, func_name, func_type])  # 添加一个函数
                            self.func_call_argulist.push([])
                            self.str1.gettop().pop()
                            self.str2.gettop().pop()
                        elif item == ')':
                            self.quaternions.append(
                                [self.count, 'call', self.func_call_namelist.gettop()[1], '_', 'T%s' % self.Tid])
                            func_type = self.func_call_namelist.gettop()[2]  # 函数调用返回类型
                            self.str1.gettop().push('a')
                            self.str2.gettop().push([func_type, 'T%s' % self.Tid])
                            self.Tid += 1
                            self.count += 1
                            if self.func_call_flag:
                                self.check_function_call()
                            self.func_call_namelist.pop()
                            self.func_call_argulist.pop()
                            self.func_call_flag = 0
                    if item in self.vn:
                        # print(ch,'[]',item)
                        if ch == 'A1' and item == 'A4':
                            self.is_main = False
                            for i in self.main_return_id:
                                self.quaternions[i][4] = self.count # 回填return
                            self.main_return_id = []
                            self.quaternions.append([self.count, 'sys', '_', '_', '_'])
                            self.count += 1
                        self.node_number += 1
                        if item in print_dic:
                            tree.node(str(self.node_number), print_dic[item], fontname="SimHei")
                        else:
                            tree.node(str(self.node_number), item, fontname="SimHei")
                        tree.edge(str(fabian), str(self.node_number))
                        self.match(ch=item, fabian=self.node_number)  # 如果碰到了非终结符，直接递归非终结符的子程序
                    elif self.p >= len(self.goal_list):
                        return 1
                    elif self.p < len(self.goal_list) and item == self.goal_list[self.p][2]:
                        if self.func_define_flag:
                            if item == '700':
                                if self.func_define_flag == 2:
                                    self.function_param_list[self.fun_list[-1]].append(self.goal_list[self.p][1])
                                else:  # 添加局部变量
                                    temp = self.goal_list[self.p][1]
                                    if temp not in self.function_param_list[self.fun_list[-1]] and temp not in \
                                            self.function_jubu_list[self.fun_list[-1]] and temp != self.fun_list[-1]:
                                        self.function_jubu_list[self.fun_list[-1]].append(self.goal_list[self.p][1])
                        # 声明语句处理
                        if self.expression_shengming:
                            self.str1.gettop().push('a')
                            if self.goal_list[self.p][2] == '700':
                                str_type = self.sym1.get_type(self.goal_list[self.p][1],self.scope)
                            else:
                                str_type = self.goal_list[self.p][2]
                            self.str2.gettop().push([str_type, self.goal_list[self.p][1]])

                        if self.shengmingflag and not self.func_call_flag:
                            if item == '700':
                                if not self.sym_flag.Equal_Flag:
                                    self.sym_flag.name = self.goal_list[self.p][1]
                                    self.sym_flag.line = self.goal_list[self.p][0]
                            else:  # 其他常量
                                # 如果是数值型常量 且前面有符号 则进行负数处理
                                if self.goal_list[self.p][2] in ['400','800','850'] and self.goal_list[self.p-1][1] == '-':
                                    if self.goal_list[self.p][2] == '400': #　将字符型字符串进行整数转化
                                        self.sym_flag.value = str(-int(self.goal_list[self.p][1]))
                                    else: # 将数值型字符串进行小数 指数转换
                                        self.sym_flag.value = str(-float(self.goal_list[self.p][1]))
                                else:
                                    self.sym_flag.value = self.goal_list[self.p][1]
                        else:
                            if item == '700' and self.goal_list[self.p + 1][1] != '(':
                                if not self.sym1.get(self.goal_list[self.p][1], self.scope):  # 等号左边变量是否声明
                                    if self.func_define_flag != 2:
                                        self.warnings_str += ("Warning: 第%s行 变量%s未声明\n" % (
                                            self.goal_list[self.p][0], self.goal_list[self.p][1]))
                                # else:
                                #     print(self.warnings_str)
                        self.node_number += 1
                        tree.node(str(self.node_number), self.goal_list[self.p][1],fontname="SimHei")
                        tree.edge(str(fabian), str(self.node_number))
                        self.p += 1
                    elif self.p < len(self.goal_list) and (item == self.goal_list[self.p][1]):  # 终结符 则进行匹配 字符串指针++
                        # 声明语句处理

                        if item == '/' and (self.p + 1) < len(self.goal_list) and self.goal_list[self.p + 1][1] == '0':
                            self.warnings_str += ("Warning: 第%s行 0不能做除数\n" % (self.goal_list[self.p][0]))

                        if self.shengmingflag:
                            if item == 'const':
                                self.shengmingflag = 1  # 常量声明
                            elif item in ['void', 'int', 'char', 'float', 'string', 'double', 'bool']:
                                if self.shengmingflag != 4:
                                    self.sym_flag.type = item
                                else:
                                    self.sym_flag.Func_type_list.append(self.goal_list[self.p][1])
                            elif self.shengmingflag == 3 and item == '(': # 超前搜索 函数声明标记
                                self.shengmingflag = 4  # 列表添加函数
                            elif self.shengmingflag == 4 and item == ')':
                                self.add_sym()  # 函数声明
                            elif item == '=':
                                self.sym_flag.Equal_Flag = 1
                        if item == 'main':
                            self.is_main = True
                            self.quaternions.append([self.count, 'main', '_', '_', '_'])
                            self.count += 1
                            self.main_flag = 1
                        elif item == '{':
                            self.area += 1
                            self.scope = "%s/%s" % (self.scope, self.area)
                        elif item == '}':
                            self.scope = self.scope[0:-2]
                        elif item == ';':
                            self.shengmingflag = 0

                        elif item == '=' and self.goal_list[self.p - 1][2] != '700':
                            self.warnings_str += ("Warning: 第%s行 常量%s不能出现在等号左边\n" % (
                                self.goal_list[self.p - 1][0], self.goal_list[self.p - 1][1]))
                        # 对break以及continue语句进行处理
                        elif item == 'break':
                            if self.xunhuan.getlen() >= 1:
                                if self.xunhuan.gettop() == 'dowhile':
                                    self.quaternions.append([self.count, 'j', '_', '_', 0])
                                    self.dowhile_FC.gettop().append(self.count)
                                    self.count += 1
                                elif self.xunhuan.gettop() == 'while':
                                    self.quaternions.append([self.count, 'j', '_', '_', 0])
                                    self.while_FC.gettop().append(self.count)
                                    self.count += 1
                                elif self.xunhuan.gettop() == 'for':
                                    self.quaternions.append([self.count, 'j', '_', '_', 0])
                                    self.for_FC.gettop().append(self.count)
                                    self.count += 1
                            else:  # 语义错误
                                self.warnings_str += ("Warning: 第%s行 %s不能出现在循环语句之外\n" % (
                                    self.goal_list[self.p ][0], self.goal_list[self.p ][1]))
                        elif item == 'continue':
                            if self.xunhuan.getlen() >= 1:
                                if self.xunhuan.gettop() == 'dowhile':
                                    self.quaternions.append([self.count, 'j', '_', '_', self.dowhile_head.gettop()])
                                    self.count += 1
                                elif self.xunhuan.gettop() == 'while':
                                    self.quaternions.append([self.count, 'j', '_', '_', self.while_head.gettop()])
                                    self.count += 1
                                elif self.xunhuan.gettop() == 'for':
                                    self.quaternions.append([self.count, 'j', '_', '_', self.for_INC.gettop()])
                                    self.count += 1
                            else:
                                self.warnings_str += ("Warning: 第%s行 %s不能出现在循环语句之外\n" % (
                                    self.goal_list[self.p ][0], self.goal_list[self.p ][1]))
                        if ch != 'p1' and self.expression_shengming and item in ['+', '-', '*', '/', '%', '(', ')', '>',
                                                                                 '<',
                                                                                 '>=', '<=', '==','!=', '&&', 'or', '!']:
                            self.str1.gettop().push(item)
                        # 对作用域进行标记
                        self.node_number += 1
                        tree.node(str(self.node_number), self.goal_list[self.p][1], fontname="SimHei")
                        tree.edge(str(fabian), str(self.node_number))
                        self.p += 1
                if ch == 'A5':  # 取消函数定义 记录函数形参及函数内变量
                    self.hsdy_flag = 0
                if ch == 'D4':  # 对表达式进行处理
                    if self.expression_shengming and not self.str1.gettop().empty():
                        str1 = copy.deepcopy(self.str1.gettop().getlist())
                        str2 = copy.deepcopy(self.str2.gettop().getlist())
                        # print(str1,str2)
                        if len(str1) == 2 and str1[0] == '-' and str2[0][0] in ['400','800','850']: # 对 “x=-1"形式进行处理
                            expression_type = self.format_type(str2[0][0])
                            if str2[0][0] == '400':
                                self.expression_list.push([expression_type, str(-int(str2[0][1]))])
                            else:
                                self.expression_list.push([expression_type, str(-double(str2[0][1]))])
                        else:
                            expression_type = self.format_type(str2[0][0])
                            ss = []
                            flag1, flag2 = 0, 0  # 表达式中是否出现[char double int bool]类型的 以及string类型
                            for l in str2:
                                if self.format_type(l[0]) in ['char', 'double', 'int', 'bool']:
                                    flag1 = 1
                                elif self.format_type(l[0]) == 'string':
                                    flag2 = 1
                                ss.append(l[1])
                            if flag1 == 1 and flag2 == 1:
                                expression_type = 'mismatch'

                            temp = self.suan_process.solve(self.count, self.Tid, str1, ss)  # 第几条四元式 T的编号，
                            if temp != False:  # 将表达式产生的四元式添加到我们原来的四元式
                                for i in temp[0]:
                                    self.quaternions.append(i)
                                self.count = temp[1]
                                self.Tid = temp[2]
                                if len(temp[0]) >= 1:
                                    self.expression_list.push([expression_type, self.quaternions[-1][4]])
                                else:
                                    # self.expression_list.push(self.str2[-1][0])
                                    self.expression_list.push([expression_type, str2[0][1]])
                    self.str1.pop()
                    self.str2.pop()
                    if self.str1.empty():
                        self.expression_shengming = 0

                if ch == 'A2': #回溯到声明语句
                    self.sym_flag.set_zero()
                    self.shengmingflag = 0  # 消除声明

                if ch == 'I1':  # 回填
                    if self.if_SC.gettop() != []:
                        for i in self.if_SC.gettop():
                            self.quaternions[i][4] = self.count
                        self.if_SC.pop()

                if ch == 'I3':  # while语句回填
                    self.quaternions.append([self.count, 'j', '_', '_', self.while_head.gettop()])  # 跳转到头 处理表达式
                    self.count += 1
                    self.while_head.pop()
                    if not self.while_FC.empty():
                        for i in self.while_FC.gettop():
                            self.quaternions[i][4] = self.count
                        self.while_FC.pop()
                    self.xunhuan.pop()

                if ch == 'I2':  # for语句回填
                    self.xunhuan.pop()
                    self.quaternions.append([self.count, 'j', '_', '_', self.for_INC.gettop()])
                    self.count += 1
                    for i in self.for_FC.gettop():
                        self.quaternions[i][4] = self.count
                    self.for_FC.pop()
                    self.for_INC.pop()
                    self.for_TEST.pop()
                    # self.for_AGAIN.pop()

                if ch == 'A5':  # 函数定义
                    self.func_define_flag = 0
                    if self.return_flag != 1:# 函数中无return语句 返回调用函数 生成ret语句
                        if self.cur_func_type[0]!='void':
                            self.warnings_str += ("Warning: 第%s行 %s函数应该有返回值!\n" % (
                                self.goal_list[self.p][0], self.cur_func_type[1]))
                        self.quaternions.append([self.count, 'ret', '_', '_', '_'])
                        self.count += 1
                    self.return_flag = 0
                if ch == 'I5':  # return 语句
                    #语义错误处理
                    if self.cur_func_type[0] == 'void':
                        self.warnings_str += ("Warning: 第%s行 %s函数无返回值，不能有return语句!\n" % (
                            self.goal_list[self.p-2][0], self.cur_func_type[1]))
                    if self.is_main == True: # main函数中的return语句
                        self.quaternions.append([self.count, 'j', '_', '_', '0'])
                        self.main_return_id.append(self.count)
                    elif self.return_exp == True:
                        self.quaternions.append([self.count, 'ret', self.expression_list.gettop()[1], '_', '_'])
                        self.expression_list.pop()
                    else:
                        self.quaternions.append([self.count, 'ret', '_', '_', '_']) # 无返回值的return 语句
                    self.return_exp = False
                    self.count += 1
                    self.return_flag = 1
                if ch == 'H2':  # 实参
                    self.quaternions.append([self.count, 'para', self.expression_list.gettop()[1], '_', '_'])
                    self.count += 1
                    self.func_call_argulist.gettop().append(self.expression_list.gettop()[0])  # 添加类型
                    self.expression_list.pop()

                if ch == 'n4':
                    if not self.if_match_format(self.expression_list.gettop()[0], self.assignment_list.gettop()[0]):
                        self.warnings_str += "Warning: 第%s行 %s等号两边格式不匹配\n " % (
                        self.assignment_list.gettop()[2], self.assignment_list.gettop()[1])
                    self.quaternions.append(
                        [self.count, '=', self.expression_list.gettop()[1], '_', self.assignment_list.gettop()[1]])
                    self.expression_list.pop()
                    self.count += 1
                    self.assignment_list.pop()

                if ch == 'C8':
                    if not self.if_match_format(self.expression_list.gettop()[0], self.assignment_list.gettop()[0]):
                        self.warnings_str += "Warning: 第%s行 %s等号两边格式不匹配\n " % (
                            self.assignment_list.gettop()[2], self.assignment_list.gettop()[1])
                    self.quaternions.append(
                        [self.count, '=', self.expression_list.gettop()[1], '_', self.assignment_list.gettop()[1]])
                    self.expression_list.pop()
                    self.count += 1
                    self.assignment_list.pop()

                return 1
        # 如果不在任意一个first(Ui)中，空 属于 first(Ui)，则判断当前符号是否在Follow集中
        if ch in kong and self.goal_list[self.p][1] in follow_dict[ch] or self.goal_list[self.p][2] in follow_dict[ch]:
            if ch == 'A2':
                self.shengmingflag = 0
            self.node_number += 1
            tree.node(str(self.node_number),'ε', fontname="SimHei")
            tree.edge(str(fabian), str(self.node_number))
            return 1
        else:
            # 进行语法错误处理
            self.syntax_error += (
                    "syntax_error: 第%s行 %s未匹配\n" % (self.goal_list[self.p][0], self.goal_list[self.p][1]))
            self.p += 1
            while self.p < self.len and (
                    self.goal_list[self.p][1] in follow_dict[ch] or self.goal_list[self.p][2] in follow_dict[ch]):
                self.p += 1
                #print(self.p)
            #print("出错啦！！！")
            return 1

    # 等号两边格式是否匹配
    def if_match_format(self, format1, format2):
        if format1 == 'mismatch' or format2 == 'mismatch':
            return False
        format1 = self.format_type(format1)
        format2 = self.format_type(format2)
        if format1 == format2:
            return True
        if format1 in ['int', 'char', 'double', 'bool'] and format2 in ['int', 'char', 'double', 'bool']:
            return True
        if format1 == None or format2 == None:
            return True
        return False

    def format_type(self, name):
        if name in ['int', '102', '400']:
            return 'int'
        elif name in ['char', '101', '500']:
            return 'char'
        elif name in ['string', '135', '600']:
            return 'string'
        elif name in ['double', '115', '800', '850']:
            return 'double'
        elif name in ['bool', '136', '137', '138']:
            return 'bool'

    def add_sym(self):
        #print('add-----', self.sym_flag.name, self.sym_flag.type, self.shengmingflag)
        if self.func_define_flag != 2 and (self.shengmingflag == 1 or self.shengmingflag == 2):
            # 常量表添加
            node = node1(self.sym_flag.type, self.sym_flag.name, self.sym_flag.value, self.scope, self.sym_flag.line)
            self.warnings_str += self.sym1.put(node, self.shengmingflag)
            self.sym_flag.set_zero1()
        elif self.shengmingflag == 4:
            # 函数表添加
            node = node2(self.sym_flag.type, self.sym_flag.name, self.sym_flag.Func_type_list, self.sym_flag.line)
            node.parameter = len(self.sym_flag.Func_type_list)
            self.warnings_str += self.sym2.put(node)
            self.sym_flag.set_zero2()

    # 函数调用检查 函数参数 以及参数类型
    def check_function_call(self):
        if self.func_call_namelist.gettop()[1] not in ['read', 'write']:
            self.warnings_str += self.sym2.check_function_call(self.func_call_namelist.gettop(),
                                                               self.func_call_argulist.gettop())  # 传入函数名 函数形参

    # 函数定义检查
    def check_function_define(self):
        self.warnings_str += self.sym2.check_function_define(self.function_parameter_defines)
        # 将形参登记到变量符号表
        if len(self.function_parameter_defines[2]) != 0:
            typelist = self.function_parameter_defines[2]
            namelist = self.function_parameter_defines[3]
            scope = "%s/%s" % (self.scope, self.area + 1)
            for i in range(len(typelist)):
                node = node1(typelist[i], namelist[i], 0, scope, self.goal_list[self.p][0])
                self.warnings_str += self.sym1.put(node, 2)  # 2 插入变量
        # 将形参登记到符号表中

    # 打印符号表
    def check_print(self):
        self.text1 = self.sym1.lookAll()
        self.text2 = self.sym2.lookAll()

    def solve(self, wordlist):
        try:
            # 语法树
            global tree
            filename = './Syntax_Tree/tree'
            tree = Digraph(filename, 'Syntax Tree', None, None, 'png', None, "UTF-8")
            """ 文法字典预处理 """
            self.goal_list = wordlist
            #print(wordlist)
            for i in self.grammer:
                list1 = str(self.grammer[i][0]).split('|')
                list2 = []
                for j in list1:
                    list2.append(j.split())
                self.grammer[i] = list2
            #print('==========', self.grammer, '+++++++', self.vn)

            """ 递归下降分析 """
            tree.node(str(self.node_number), print_dic[self.vn[0]], fontname="SimHei")
            self.p = 0  # 字符串指针
            self.len = len(self.goal_list)
            flag = (self.match(self.vn[0], self.node_number) & (self.p == len(self.goal_list)))  # 必须要遍历完测试字符串
            #print(self.p)
            if flag:
                #print(self.quaternions)
                print(' 分析成功')
            else:
                print(' 分析失败')
            self.check_print()
            if self.main_flag == 0:
                self.warnings_str += "Warning: 程序中无main函数！！！\n"
            siyuanshi = []
            for i in self.quaternions:
                siyuanshi.append(i[1:])
            self.quaternions = siyuanshi
            for i in self.quaternions:
                if i[0] == '@':
                    i[0] = '-'
            """打印符号表"""
            tree.render()
            # print(tree.source)
            # tree.render('test-output/test-table.gv', view=True)
            return self.fun_list, self.function_param_list, self.function_jubu_list, self.quaternions, self.syntax_error, self.warnings_str, self.text1, self.text2
        except:
            return self.fun_list, self.function_param_list, self.function_jubu_list, self.quaternions, self.syntax_error, self.warnings_str, self.text1, self.text2
# 定义栈
class Stack(object):


    def __init__(self):
        self.stack = []


    def push(self, data):
        """
        进栈函数
        """
        self.stack.append(data)


    def pop(self):
        """
        出栈函数，
        """
        if not self.empty():
            return self.stack.pop()
        else:
            return None


    def gettop(self):
        """
        取栈顶
        """
        if not self.empty():
            return self.stack[-1]
        else:
            return None


    def empty(self):
        """
        判断是否为空
        """
        if len(self.stack) == 0:
            return 1
        else:
            return 0


    def getlist(self):
        '''
        :return: stack()列表
        '''
        return self.stack


    def getlen(self):
        return len(self.stack)

# file_object = open('文法.txt')
# a = recDesc_analysis(file_object)
# # a.solve([[2, 'main', '142'], [2, '(', '201'], [2, ')', '202'], [2, '{', '301'], [3, 'int', '102'], [3, 'n', '700'], [3, ',', '304'], [3, 'i', '700'], [3, ',', '304'], [3, 'sum', '700'], [3, ';', '303'], [5, 'for', '113'], [5, '(', '201'], [5, 'int', '102'], [5, 'n', '700'], [5, '=', '230'], [5, '1', '400'], [5, ';', '303'], [5, 'n', '700'], [5, '<=', '220'], [5, '1000', '400'], [5, ';', '303'], [5, 'n', '700'], [5, '=', '230'], [5, 'n', '700'], [5, '+', '207'], [5, '1', '400'], [5, ')', '202'], [5, '{', '301'], [6, 'sum', '700'], [6, '=', '230'], [6, '0', '400'], [6, ';', '303'], [7, 'for', '113'], [7, '(', '201'], [7, 'i', '700'], [7, '=', '230'], [7, '1', '400'], [7, ';', '303'], [7, 'i', '700'], [7, '<', '219'], [7, 'n', '700'], [7, ';', '303'], [7, 'i', '700'], [7, '=', '230'], [7, 'i', '700'], [7, '+', '207'], [7, '1', '400'], [7, ')', '202'], [7, '{', '301'], [8, 'if', '111'], [8, '(', '201'], [8, 'n', '700'], [8, '%', '216'], [8, 'i', '700'], [8, '==', '223'], [8, '0', '400'], [8, ')', '202'], [8, 'sum', '700'], [8, '=', '230'], [8, 'sum', '700'], [8, '+', '207'], [8, 'i', '700'], [8, ';', '303'], [9, '}', '302'], [10, 'if', '111'], [10, '(', '201'], [10, 'sum', '700'], [10, '==', '223'], [10, 'n', '700'], [10, ')', '202'], [10, '{', '301'], [11, 'write', '700'], [11, '(', '201'], [11, 'n', '700'], [11, ')', '202'], [11, ';', '303'], [12, '}', '302'], [13, '}', '302'], [14, 'return', '106'], [14, '0', '400'], [14, ';', '303'], [15, '}', '302']]
# #         )
# fun_list,function_param_list,function_jubu_list,siyuanshia,dd,worrings_str,text1,text2 = a.solve([[2, 'int', '102'], [2, 'a', '700'], [2, '=', '230'], [2, '1', '400'], [2, ';', '303'], [3, 'int', '102'], [3, 'seq', '700'], [3, '(', '201'], [3, 'int', '102'], [3, ',', '304'], [3, 'int', '102'], [3, ')', '202'], [3, ';', '303'], [4, 'const', '105'], [4, 'int', '102'], [4, 'c', '700'], [4, '=', '230'], [4, '2', '400'], [4, ',', '304'], [4, 'd', '700'], [4, '=', '230'], [4, '3', '400'], [4, ';', '303'], [5, 'int', '102'], [5, 'p', '700'], [5, ',', '304'], [5, 'q', '700'], [5, '=', '230'], [5, '9', '400'], [5, ';', '303'], [6, 'main', '142'], [6, '(', '201'], [6, ')', '202'], [6, '{', '301'], [8, 'int', '102'], [8, 'result', '700'], [8, ';', '303'], [9, 'int', '102'], [9, 'N', '700'], [9, '=', '230'], [9, 'read', '700'], [9, '(', '201'], [9, 'a', '700'], [9, '+', '207'], [9, '1', '400'], [9, ',', '304'], [9, 'c', '700'], [9, ')', '202'], [9, ';', '303'], [10, 'int', '102'], [10, 'M', '700'], [10, '=', '230'], [10, 'read', '700'], [10, '(', '201'], [10, ')', '202'], [10, ';', '303'], [11, 'int', '102'], [11, 'b', '700'], [11, '=', '230'], [11, '2', '400'], [11, '+', '207'], [11, '3', '400'], [11, '-', '208'], [11, '2', '400'], [11, '+', '207'], [11, '(', '201'], [11, '5', '400'], [11, '+', '207'], [11, '6', '400'], [11, ')', '202'], [11, '+', '207'], [11, '3', '400'], [11, '*', '213'], [11, '5', '400'], [11, '/', '215'], [11, 'a', '700'], [11, ';', '303'], [12, 'if', '111'], [12, '(', '201'], [12, 'A', '700'], [12, '&&', '227'], [12, 'B', '700'], [12, '&&', '227'], [12, 'c', '700'], [12, '>', '221'], [12, 'D', '700'], [12, ')', '202'], [13, 'if', '111'], [13, '(', '201'], [13, 'M', '700'], [13, '>=', '222'], [13, 'N', '700'], [13, ')', '202'], [13, 'result', '700'], [13, '=', '230'], [13, 'M', '700'], [13, ';', '303'], [14, 'else', '112'], [14, 'result', '700'], [14, '=', '230'], [14, 'N', '700'], [14, ';', '303'], [16, 'if', '111'], [16, '(', '201'], [16, 'w', '700'], [16, '<', '219'], [16, '1', '400'], [16, ')', '202'], [17, 'a', '700'], [17, '=', '230'], [17, 'b', '700'], [17, '*', '213'], [17, 'c', '700'], [17, '+', '207'], [17, 'd', '700'], [17, ';', '303'], [18, 'else', '112'], [19, '{', '301'], [20, 'do', '109'], [21, '{', '301'], [22, 'a', '700'], [22, '=', '230'], [22, 'a', '700'], [22, '-', '208'], [22, '1', '400'], [22, ';', '303'], [23, '}', '302'], [23, 'while', '110'], [23, '(', '201'], [23, 'a', '700'], [23, '<', '219'], [23, '0', '400'], [23, ')', '202'], [23, ';', '303'], [25, '}', '302'], [26, 'for', '113'], [26, '(', '201'], [26, 'i', '700'], [26, '=', '230'], [26, 'a', '700'], [26, '+', '207'], [26, 'b', '700'], [26, '*', '213'], [26, '2', '400'], [26, ';', '303'], [26, 'i', '700'], [26, '<', '219'], [26, 'c', '700'], [26, '+', '207'], [26, 'd', '700'], [26, '+', '207'], [26, '10', '400'], [26, ';', '303'], [26, 'i', '700'], [26, '=', '230'], [26, 'i', '700'], [26, '+', '207'], [26, '1', '400'], [26, ')', '202'], [27, 'if', '111'], [27, '(', '201'], [27, 'h', '700'], [27, '>', '221'], [27, 'g', '700'], [27, ')', '202'], [28, 'p', '700'], [28, '=', '230'], [28, 'p', '700'], [28, '+', '207'], [28, '1', '400'], [28, ';', '303'], [29, 'a', '700'], [29, '=', '230'], [29, 'result', '700'], [29, '+', '207'], [29, '100', '400'], [29, ';', '303'], [30, 'write', '700'], [30, '(', '201'], [30, 'a', '700'], [30, ')', '202'], [30, ';', '303'], [32, '}', '302']])
# print(siyuanshia )
# print(function_param_list,function_jubu_list)