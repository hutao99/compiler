from collection import FirstAndFollow
import difflib
from anytree import Node as AnyTreeNode, RenderTree
from graphviz import Digraph


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Node(AnyTreeNode):
    def __init__(self, value, symbol_info=None, **kwargs):
        super().__init__(value, **kwargs)
        self.symbol_info = symbol_info
        self.type = None
        self.value = None
        self.parameters = 0


class VariableInfo:
    def __init__(self):
        self.type = None
        self.scope = None
        self.value = None


class FunctionInfo:
    def __init__(self):
        self.type = None
        self.para_num = 0
        self.para_type = None


class ConstantInfo:
    def __init__(self):
        self.type = None
        self.scope = None
        self.value = None


class ArrayInfo:
    def __init__(self):
        self.type = None
        self.scope = None
        self.row = 0
        self.col = 0


class CLRParser:
    def __init__(self):
        self.first = None
        # 产生式
        self.Formula = None
        # 文法开始符号
        self.begin = ''
        # 规约式,也是产生式
        self.reduction = []
        # 分析表
        self.parsing_table = dict()
        # 语法树根节点
        self.node = None
        # 语法错误
        self.errors = []
        # 变量表
        self.VariableTable = dict()
        # 函数表
        self.FunctionTable = dict()
        # 常数表
        self.ConstantTable = dict()
        # 数组表
        self.ArrayTable = dict()
        # 语法错误
        self.errors = []
        # 警告
        self.warning = []
        # 变量使用次数
        self.var_num = dict()
        # 中间代码
        self.code = []
        # 分析表_中间代码
        self.parsing_table1 = None
        # 规约式_中间代码
        self.reduction1 = None
        # 函数参数
        self.function_param_list = dict()
        # 函数局部变量
        self.function_jubu_list = dict()
        # 函数内部数组
        self.function_array_list = dict()
        # 全局数组
        self.global_array_list = []

        self.prod_state = None
        self.status_include_num = None
        self.direction = None

        # Digraph图片
        self.dot = Digraph(comment='LR_DFA_Digraph')

    def input(self, data):
        self.__init__()
        p = FirstAndFollow()
        p.input(data)
        self.first = p.first
        self.Formula = p.Formula
        self.begin = p.begin

    # 检查范围
    def CheckScope(self, name, scope):
        if name in self.VariableTable:
            for i in self.VariableTable[name]:
                if i.scope == scope:
                    return True
        if name in self.ConstantTable:
            for i in self.ConstantTable[name]:
                if i.scope == scope:
                    return True
        if name in self.ArrayTable:
            for i in self.ArrayTable[name]:
                if i.scope == scope:
                    return True
        return False

    # 是否为常量
    def IsConst(self, name, scope):
        if name in self.ConstantTable:
            for i in self.ConstantTable[name]:
                if scope.startswith(i.scope):
                    return True
        return False

    # 检查变量是否声明
    def IsDeclare(self, name, scope):
        if name in self.VariableTable:
            for i in self.VariableTable[name]:
                if scope.startswith(i.scope):
                    return True
        if name in self.ConstantTable:
            for i in self.ConstantTable[name]:
                if scope.startswith(i.scope):
                    return True
        if name in self.ArrayTable:
            for i in self.ArrayTable[name]:
                if scope.startswith(i.scope):
                    return True
        return False

    def Action_and_GoTo_Table(self):
        self.Formula[self.begin+"'"] = self.begin
        state = []
        # I0包含的产生式
        state_family = []
        # 给不同产生式进行编号
        prod_state = {}
        label = 0
        # 状态包含的产生式编号
        status_include_num = []
        # 构建初始状态I0
        id0 = []
        stack = [[self.begin, ['.', self.begin], ['#']]]
        # 加入开始产生式
        state_family.append([self.begin+"'", ['.', self.begin], ['#']])
        prod_state[self.begin+"'"+'→'+"".join(['.', self.begin])+' '+'#'] = label
        id0.append(label)
        label += 1
        # 用于规约式编号的字典
        reduction = dict()
        while len(stack) > 0:  # 将所有终结符处理完毕
            h = stack.pop(0)
            prod = self.Formula[h[0]]
            inx = h[1].index('.')
            # 求出展望符(向前搜索符)
            lookahead_symbol = []
            # 没有到末尾
            if inx+2 < len(h[1]):
                # 是非终结符
                if h[1][inx+2] in self.Formula:
                    group = set()
                    stack1 = [[h[1][inx+2], inx+2]]
                    # 将后续first集加入展望符
                    while len(stack1) > 0:
                        tt = stack1.pop()
                        group.update([x for x in self.first[tt[0]] if x != 'ε'])
                        if 'ε' in self.first[tt[0]]:
                            if tt[1]+1 == len(h[1]):
                                group.update(h[2])
                            elif h[tt[1]+1] in self.Formula:
                                stack1.append([h[tt[1]+1], tt[1]+1])
                            else:
                                group.add(h[tt[1]+1])
                    lookahead_symbol = list(group)
                # 不是
                else:
                    lookahead_symbol = [h[1][inx+2]]
            # 到末尾直接继承
            else:
                lookahead_symbol = h[2]
            lookahead_symbol.sort()
            # .后面为非终结符，将非终结符的的产生式加入当前状态，同时去除相同状态内的相同元素
            for g in prod.split('|'):
                word = [k for k in g.split(' ') if k != '']
                if word == ['ε']:
                    word = []
                word.insert(0, '.')
                st = h[0]+'→'+''.join(word)+' '+''.join(lookahead_symbol)
                if st not in prod_state:
                    prod_state[st] = label
                    label += 1
                # 在id0说明存在这个状态，直接跳过
                if prod_state[st] in id0:
                    continue
                id0.append(prod_state[st])
                state_family.append([h[0], word, lookahead_symbol])
                if len(word) > 1 and word[1] in self.Formula:
                    stack.append([word[1], word, lookahead_symbol])
        id0.sort()
        # 记录I0状态包含的产生式状态编号
        status_include_num.append(id0)
        state.append(state_family)
        state1 = []
        # 状态下标
        index = 0
        father = 0
        # 记录状态指向
        direction = []
        number = 0
        # 记录规约表
        reduction_table = []
        while len(state) > 0:
            status = state.pop(0)
            # print(status)
            state1.append(status)
            # 求出'.'后一个符号，如没有就不处理，相同符号的status下标归在一起
            behind = {}
            for l in range(len(status)):
                i = status[l]
                idx = i[1].index('.')
                if idx+1 == len(i[1]):  # 可规约
                    if i[0] + ':' + ' '.join(i[1][:-1]) not in reduction:
                        reduction[i[0] + ':' + ' '.join(i[1][:-1])] = number
                        number += 1
                    for q in i[2]:
                        reduction_table.append([father, q, reduction[i[0] + ':' + ' '.join(i[1][:-1])]])
                    continue
                if i[1][idx+1] in behind:
                    behind[i[1][idx+1]].append(l)
                else:
                    behind[i[1][idx+1]] = [l]
            # 为每个后面符号相同的元素构成一个状态，如果这个状态和已有的状态相同，则直接连上这个状态
            for i in behind:
                new_status = []
                id_n = []  # 记录new_status中已有的产生式状态
                for j in behind[i]:
                    itemset = []
                    idx = status[j][1].index('.')
                    # 加入产生式左部
                    itemset.append(status[j][0])
                    # 加入产生式及状态
                    u = status[j][1]
                    t = u[idx]
                    u[idx] = u[idx+1]
                    u[idx+1] = t
                    itemset.append(u)
                    # 加入向前搜索符
                    itemset.append(status[j][2])
                    new_status.append(itemset)
                    st = status[j][0]+'→'+''.join(u)+' '+''.join(status[j][2])
                    if st not in prod_state:
                        prod_state[st] = label
                        label += 1
                    id_n.append(prod_state[st])
                    # 如果现在'.'后为非终结符，则需加入这个非终结符的状态,如果加入的这个'.'后也是非终结符则还需再加，直到不是非终结符
                    stack = []
                    if idx+2 < len(u) and u[idx+2] in self.Formula:  # 是非终结符
                        stack = [[u[idx+2], u, status[j][2]]]
                    else:
                        continue
                    while len(stack) > 0:  # 将所有终结符处理完毕
                        h = stack.pop(0)
                        prod = self.Formula[h[0]]
                        inx = h[1].index('.')
                        lookahead_symbol = []
                        if inx + 2 < len(h[1]):
                            if h[1][inx + 2] in self.Formula:
                                group = set()
                                stack1 = [[h[1][inx + 2], inx + 2]]
                                while len(stack1) > 0:
                                    tt = stack1.pop()
                                    group.update([x for x in self.first[tt[0]] if x != 'ε'])
                                    if 'ε' in self.first[tt[0]]:
                                        if tt[1] + 1 == len(h[1]):
                                            group.update(h[2])
                                        elif h[tt[1] + 1] in self.Formula:
                                            stack1.append([h[tt[1] + 1], tt[1] + 1])
                                        else:
                                            group.add(h[tt[1] + 1])
                                    lookahead_symbol = list(group)
                            else:
                                lookahead_symbol = [h[1][inx + 2]]
                        else:
                            lookahead_symbol = h[2]
                        lookahead_symbol.sort()
                        for g in prod.split('|'):
                            word = [k for k in g.split(' ') if k != '']
                            if word == ['ε']:
                                word = []
                            word.insert(0, '.')
                            st = h[0] + '→' + ''.join(word) + ' ' + ''.join(lookahead_symbol)
                            if st not in prod_state:
                                prod_state[st] = label
                                label += 1
                            if prod_state[st] in id_n:
                                continue
                            id_n.append(prod_state[st])
                            new_status.append([h[0], word, lookahead_symbol])
                            if len(word) > 1 and word[1] in self.Formula:
                                stack.append([word[1], word, lookahead_symbol])
                #  判断状态是否相同，如I1和new_status
                id_n.sort()
                # 判断各个状态间是否有重复
                if id_n in status_include_num:
                    direction.append([father, i, status_include_num.index(id_n)])
                    continue
                index += 1
                status_include_num.append(id_n)
                state.append(new_status)
                direction.append([father, i, index])
            father += 1
        '''for i in reduction:
            print(i, end=' ')
            print(reduction[i])'''
        # 分析表构造
        for i in direction:
            if i[0] not in self.parsing_table:
                self.parsing_table[i[0]] = dict()
            self.parsing_table[i[0]][i[1]] = str(i[2])
        for i in reduction_table:
            if i[0] not in self.parsing_table:
                self.parsing_table[i[0]] = dict()
            self.parsing_table[i[0]][i[1]] = 'r'+str(i[2])
            if i[2] == reduction[self.begin+"'"+":"+self.Formula[self.begin+"'"]]:
                self.parsing_table[i[0]][i[1]] = 'acc'
        for i in reduction.keys():
            self.reduction.append(i)

        self.prod_state = prod_state
        self.status_include_num = status_include_num
        self.direction = direction

    def draw_graphic(self):
        prod_state_exchange = {v: k for k, v in self.prod_state.items()}
        dot = Digraph(comment='LR_Digraph')
        for i in range(len(self.status_include_num)):
            lab = 'I' + str(i+1) + '\n'
            for j in self.status_include_num[i]:
                lab += prod_state_exchange[j] + '\n'
            dot.node(str(i), lab)
        for i in self.direction:
            dot.edge(str(i[0]), str(i[2]), i[1])
        dot.render('LR_Digraph.gv', view=False, format='png', directory='LR_Digraph')

    def ControlProgram(self, token):
        self.errors.clear()
        self.var_num.clear()
        self.ConstantTable.clear()
        self.VariableTable.clear()
        self.FunctionTable.clear()
        self.warning.clear()
        self.ArrayTable.clear()
        self.dot.clear()
        # read函数
        previse_fun = FunctionInfo()
        previse_fun.type = 'int'
        previse_fun.para_num = 0
        previse_fun.para_type = 'int'
        self.FunctionTable['read'] = previse_fun
        # write函数
        previse_fun = FunctionInfo()
        previse_fun.type = 'void'
        previse_fun.para_num = 1
        previse_fun.para_type = 'int'
        self.FunctionTable['write'] = previse_fun

        # 节点标号
        node_index = 0
        stack_num = []

        # 符号列表
        sign_list = []
        # 终结符顺序
        sign_sequence = [')', '}', '表达式', '布尔表达式', '赋值表达式', '关系表达式', '算数表达式', ';', ',', '(', '{']

        # 定义排序规则
        def my_key(x):
            try:
                return sign_sequence.index(x)
            except ValueError:
                return len(sign_sequence)

        for i in token:
            if i[0] == 'keyword' or i[0] == 'Boundary' or i[0] == 'operator':
                name = i[1]
            else:
                name = i[0]
            if name == '||':
                name = 'or'
            sign_list.append(name)

        # 语法树栈
        stack_node = []
        # 状态栈
        stack_state = [0]
        # 符号栈
        stack_symbol = ['#']
        # token下标
        index = 0
        # 插入导致循环的符号
        sign_loop = ['(', '{']
        # 初始范围
        scope = [['0', 0]]
        #
        fun_name = ''
        while index < len(sign_list):

            name = sign_list[index]
            # print(token[index])
            # print(name)
            # print(stack_state[-1])
            # 错误恢复及处理,采用最小编辑距离决定删除还是插入
            if name not in self.parsing_table[stack_state[-1]]:
                # 找出action表中不为空元素的键值
                expected = list(self.parsing_table[stack_state[-1]].keys())
                if sign_list[index-1] in sign_loop and sign_list[index-1] in expected:
                    expected.remove(sign_list[index-1])
                expected = sorted(expected, key=my_key)
                print(expected)
                flag = True
                for i in expected:
                    if i in self.Formula:
                        name = i
                        flag = False
                        if index-1 >= 0:
                            self.errors.append([token[index-1][2], token[index-1][3], '%s后可能需要%s' % (sign_list[index-1], i)])
                        else:
                            self.errors.append([0, 0,
                                                '程序开始可能需要%s' % i])
                        sign_list.insert(index, i)
                        if index-1 >= 0:
                            token.insert(index, ['', '', token[index-1][2], token[index-1][3]])
                        else:
                            token.insert(index, ['', '', 0, 0])
                        # print('%s后可能需要%s' % (sign_list[index-1], i))
                        break
                if flag:
                    minimum = 10000
                    ops_min = None
                    s1_ = None
                    s2_ = None
                    for sign in expected:
                        if sign not in sign_list[index:]:
                            continue
                        subscript = sign_list.index(sign, index-1)
                        s1 = sign_list[index-1:subscript+1]
                        s2 = [sign_list[index-1], sign]
                        seq_matcher = difflib.SequenceMatcher(None, s1, s2)
                        ops = seq_matcher.get_opcodes()
                        distance = 0
                        for op in ops:
                            if op[0] == "delete":
                                distance += op[2] - op[1]
                            elif op[0] == "insert":
                                distance += op[4] - op[3]
                            elif op[0] == "replace":
                                distance += op[2] - op[1]
                                distance += op[4] - op[3]
                        if distance < minimum:
                            minimum = distance
                            ops_min = ops
                            s1_ = s1
                            s2_ = s2
                    print(s1_)
                    print(s2_)
                    if minimum < 4:
                        for tag, i1, i2, j1, j2 in ops_min:
                            print('{:7} {} --> {}'.format(tag, s1_[i1:i2], s2_[j1:j2]))
                        for tag, i1, i2, j1, j2 in ops_min:
                            index_now = index
                            if tag == 'equal':
                                index_now += i2 - i1
                            elif tag == 'delete':
                                for i in range(len(s1_[i1:i2])):
                                    unnecessary = sign_list.pop(index_now)
                                    self.errors.append([token[index_now][2], token[index_now][3],
                                                        ("多余符号%s" % unnecessary)])
                                    token.pop(index_now)
                                    print("多余符号%s" % unnecessary)
                            elif tag == 'insert':
                                for i in s2_[j1:j2]:
                                    self.errors.append([token[index_now-1][2], token[index_now-1][3],
                                                        ('%s后可能需要%s' % (sign_list[index_now-1], i))])
                                    sign_list.insert(index_now, i)
                                    token.insert(index_now, ['', '', token[index_now-1][2], token[index_now-1][3]])
                                    index_now += 1
                                    print('%s后可能需要%s' % (sign_list[index-1], i))
                            elif tag == 'replace':
                                for i in range(len(s1_[i1:i2])):
                                    unnecessary = sign_list.pop(index_now)
                                    self.errors.append([token[index_now][2], token[index_now][3],
                                                        ("多余符号%s" % unnecessary)])
                                    token.pop(index_now)
                                    print("多余符号%s" % unnecessary)
                                for i in s2_[j1:j2]:
                                    self.errors.append([token[index_now-1][2], token[index_now-1][3],
                                                        ('%s后可能需要%s' % (sign_list[index_now - 1], i))])
                                    token.insert(index_now, ['', '', token[index_now-1][2], token[index_now-1][3]])
                                    sign_list.insert(index_now, i)
                                    index_now += 1
                                    print('%s后可能需要%s' % (sign_list[index_now-1], i))
                    else:
                        # 最短编辑距离大于3，尝试插入期望的符号
                        sign_list.insert(index, expected[0])
                        self.errors.append([token[index-1][2], token[index-1][3],
                                            ('%s后可能需要%s' % (sign_list[index - 1], expected[0]))])
                        print('sda')
                        token.insert(index, ['', '', token[index-1][2], token[index-1][3]])
                        print('%s后可能需要%s' % (sign_list[index-1], expected[0]))
            name = sign_list[index]
            status = self.parsing_table[stack_state[-1]][name]
            if status[0] == 'r':
                production = self.reduction[int(status[1:])]
                idx = production.find(':')
                father = Node(production[0:idx])
                self.dot.node(str(node_index), production[0:idx], fontname="SimHei")
                if idx + 1 < len(production):
                    prod = production[idx+1:].split(' ')
                    for i in range(len(prod)):
                        stack_state.pop()
                        stack_symbol.pop()
                        self.dot.edge(str(node_index), str(stack_num.pop()))
                        stack_node.pop().parent = father
                    # 综合属性传递
                    if father.name == '类型':
                        father.type = father.children[0].name
                        father.parameters = 1
                        # print(father.type)
                    elif father.name == '变量声明':
                        # print(father.children)
                        father.type = father.children[-1].type
                        val = VariableInfo()
                        val.type = father.type
                        val.scope = scope[-1][0]
                        arr = ArrayInfo()
                        arr.type = father.type
                        arr.scope = scope[-1][0]

                        if father.children[0].name == 'identifier':
                            # print(father.children[0].symbol_info[1])
                            if father.children[0].symbol_info[1] in self.FunctionTable:
                                self.errors.append(
                                    [father.children[0].symbol_info[2], father.children[0].symbol_info[3],
                                     "'%s'变量名和函数重复" % father.children[0].symbol_info[1]])
                            elif father.children[0].symbol_info[1] not in self.VariableTable:
                                self.VariableTable[father.children[0].symbol_info[1]] = []
                                self.VariableTable[father.children[0].symbol_info[1]].append(val)

                                self.var_num[father.children[0].symbol_info[1]] = dict()
                                self.var_num[father.children[0].symbol_info[1]][scope[-1][0]] = [0, father.children[
                                    0].symbol_info]
                            else:
                                # 判断是否有作用域相同的标识符
                                if self.CheckScope(father.children[0].symbol_info[1], scope[-1][0]):
                                    self.errors.append(
                                        [father.children[0].symbol_info[2], father.children[0].symbol_info[3],
                                         "'%s'变量名字已声明" % father.children[0].symbol_info[1]])
                                else:
                                    self.VariableTable[father.children[0].symbol_info[1]].append(val)

                                    self.var_num[father.children[0].symbol_info[1]][scope[-1][0]] = [0,
                                                                                                     father.children[
                                                                                                         0].symbol_info]

                        elif father.children[0].name == '表达式':
                            val.value = father.children[0].value
                            if father.children[2].symbol_info[1] in self.FunctionTable:
                                self.errors.append(
                                    [father.children[2].symbol_info[2], father.children[2].symbol_info[3],
                                     "'%s'变量名和函数重复" % father.children[2].symbol_info[1]])
                            elif father.children[2].symbol_info[1] not in self.VariableTable:
                                self.VariableTable[father.children[2].symbol_info[1]] = []
                                self.VariableTable[father.children[2].symbol_info[1]].append(val)

                                self.var_num[father.children[2].symbol_info[1]] = dict()
                                self.var_num[father.children[2].symbol_info[1]][scope[-1][0]] = [0, father.children[
                                    2].symbol_info]
                            else:
                                # 判断是否有作用域相同的标识符
                                if self.CheckScope(father.children[2].symbol_info[1], scope[-1][0]):
                                    self.errors.append(
                                        [father.children[2].symbol_info[2], father.children[2].symbol_info[3],
                                         "'%s'变量名字已声明" % father.children[2].symbol_info[1]])
                                else:
                                    self.VariableTable[father.children[2].symbol_info[1]].append(val)

                                    self.var_num[father.children[2].symbol_info[1]][scope[-1][0]] = [0,
                                                                                                     father.children[
                                                                                                         2].symbol_info]
                        elif father.children[0].name == '数组':
                            if len(father.children[0].children) == 4:
                                arr.row = father.children[0].children[1].value
                            else:
                                arr.row = father.children[0].children[4].value
                                arr.col = father.children[0].children[1].value
                            if father.children[0].children[-1].symbol_info[1] in self.FunctionTable:
                                self.errors.append(
                                    [father.children[0].children[-1].symbol_info[2], father.children[0].children[-1].symbol_info[3],
                                     "'%s'变量名和函数重复" % father.children[0].children[-1].symbol_info[1]])
                            elif father.children[0].children[-1].symbol_info[1] not in self.ArrayTable:
                                self.ArrayTable[father.children[0].children[-1].symbol_info[1]] = []
                                self.ArrayTable[father.children[0].children[-1].symbol_info[1]].append(arr)

                            else:
                                # 判断是否有作用域相同的标识符
                                if self.CheckScope(father.children[0].children[-1].symbol_info[1], scope[-1][0]):
                                    self.errors.append(
                                        [father.children[0].children[-1].symbol_info[2], father.children[0].children[-1].symbol_info[3],
                                         "'%s'变量名字已声明" % father.children[0].children[-1].symbol_info[1]])
                                else:
                                    self.ArrayTable[father.children[0].children[-1].symbol_info[1]].append(arr)
                        elif father.children[0].name == '变量初值':
                            if len(father.children[2].children) == 4:
                                arr.row = father.children[2].children[1].value
                            else:
                                arr.row = father.children[2].children[4].value
                                arr.col = father.children[2].children[1].value
                            if father.children[2].children[-1].symbol_info[1] in self.FunctionTable:
                                self.errors.append(
                                    [father.children[2].children[-1].symbol_info[2], father.children[2].children[-1].symbol_info[3],
                                     "'%s'变量名和函数重复" % father.children[2].children[-1].symbol_info[1]])
                            elif father.children[2].children[-1].symbol_info[1] not in self.ArrayTable:
                                self.ArrayTable[father.children[2].children[-1].symbol_info[1]] = []
                                self.ArrayTable[father.children[2].children[-1].symbol_info[1]].append(arr)

                            else:
                                # 判断是否有作用域相同的标识符
                                if self.CheckScope(father.children[2].children[-1].symbol_info[1], scope[-1][0]):
                                    self.errors.append(
                                        [father.children[2].children[-1].symbol_info[2], father.children[2].children[-1].symbol_info[3],
                                         "'%s'变量名字已声明" % father.children[2].children[-1].symbol_info[1]])
                                else:
                                    self.ArrayTable[father.children[2].children[-1].symbol_info[1]].append(arr)
                    elif father.name == '布尔表达式' or father.name == '布尔项' or father.name == '布尔因子':
                        if len(father.children) == 1:
                            father.value = father.children[0].value
                    elif father.name == '函数声明参数':
                        if len(father.leaves) == 1:
                            father.type = father.children[0].type
                            father.parameters = father.children[0].parameters
                        else:
                            father.type = father.children[-1].type + ',' + father.children[0].type
                            father.parameters = father.children[0].parameters + 1
                    elif father.name == '函数声明参数列表':
                        father.type = father.children[0].type
                        father.parameters = father.children[0].parameters
                    elif father.name == '函数声明':
                        if father.children[-2].symbol_info[1] in self.VariableTable:
                            self.errors.append(
                                [father.children[-2].symbol_info[2], father.children[-2].symbol_info[3],
                                 "'%s'函数和变量重名" % father.children[-2].symbol_info[1]])
                        elif father.children[-2].symbol_info[1] in self.ConstantTable:
                            self.errors.append(
                                [father.children[-2].symbol_info[2], father.children[-2].symbol_info[3],
                                 "'%s'函数和常量重名" % father.children[-2].symbol_info[1]])
                        elif father.children[-2].symbol_info[1] in self.FunctionTable:
                            self.errors.append(
                                [father.children[-2].symbol_info[2], father.children[-2].symbol_info[3],
                                 "'%s'函数名字已声明" % father.children[-2].symbol_info[1]])
                        elif father.children[-2].symbol_info[1] in self.ArrayTable:
                            self.errors.append(
                                [father.children[-2].symbol_info[2], father.children[-2].symbol_info[3],
                                 "'%s'函数名字和数组重名" % father.children[-2].symbol_info[1]])
                        else:
                            fun = FunctionInfo()
                            if father.children[-1].name != 'void':
                                fun.type = father.children[-1].type
                            else:
                                fun.type = 'void'
                            fun.para_type = father.children[2].type
                            fun.para_num = father.children[2].parameters
                            self.FunctionTable[father.children[-2].symbol_info[1]] = fun
                        # print(father.children)
                    elif father.name == '数字常量':
                        if father.children[0].name == 'integer':
                            father.type = 'int'
                        elif father.children[0].name == 'float':
                            father.type = 'float'
                        father.value = father.children[0].symbol_info[1]
                    elif father.name == '加减表达式' or father.name == '算术表达式' or father.name == '表达式':
                        if len(father.children) == 1:
                            father.value = father.children[0].value
                    elif father.name == '字符型常量':
                        father.value = ord(father.children[0].symbol_info[1])
                        # 把字符型转为int类型
                        father.type = 'int'
                    elif father.name == '常量' or father.name == '因子':
                        father.value = father.children[0].value
                        father.type = father.children[0].type
                    elif father.name == '项':
                        if len(father.children) == 1:
                            father.type = father.children[0].type
                            father.value = father.children[0].value
                        elif father.children[1].symbol_info[1] == '%':
                            # 整除符号要求两边都为int
                            if father.children[0].type == 'float' or father.children[-1].type == 'float':
                                self.errors.append(
                                    [father.children[1].symbol_info[2], father.children[1].symbol_info[3],
                                     "'%'要求两边类型为integer"])
                            elif father.children[0].value == '0':
                                self.errors.append(
                                    [father.children[1].symbol_info[2], father.children[1].symbol_info[3],
                                     "除数不为0"])
                            else:
                                father.type = father.children[0].type
                        elif father.children[1].symbol_info[1] == '/':
                            if father.children[0].value == '0':
                                self.errors.append(
                                    [father.children[1].symbol_info[2], father.children[1].symbol_info[3],
                                     "除数不为0"])
                            elif father.children[0].type == 'float' or father.children[-1].type == 'float':
                                father.type = 'float'
                            else:
                                father.type = 'int'
                        else:
                            if father.children[0].type == 'float' or father.children[-1].type == 'float':
                                father.type = 'float'
                            else:
                                father.type = 'int'
                    elif father.name == '变量':
                        #print('2222')
                        if father.children[0].name == 'identifier':
                            father.value = father.children[0].symbol_info[1]
                        else:
                            father.value = father.children[0].value
                        if father.children[0].name == 'identifier' and not self.IsDeclare(father.children[0].symbol_info[1], scope[-1][0]):
                            self.errors.append(
                                [father.children[0].symbol_info[2], father.children[0].symbol_info[3],
                                 "变量'%s'未声明" % father.children[0].symbol_info[1]])
                        elif father.children[0].name == '数组' and not self.IsDeclare(father.children[-1].children[-1].symbol_info[1], scope[-1][0]):
                            self.errors.append(
                                [father.children[-1].children[-1].symbol_info[2], father.children[-1].children[-1].symbol_info[3],
                                 "变量'%s'未声明" % father.children[-1].children[-1].symbol_info[1]])
                        else:
                            if father.children[0].name == 'identifier' and father.children[0].symbol_info[1] in self.var_num:
                                for r in self.var_num[father.children[0].symbol_info[1]]:
                                    leng = len(scope[-1][0])
                                    hh = False
                                    for w in range(leng):
                                        if scope[-1][0][0:leng - w] == r:
                                            self.var_num[father.children[0].symbol_info[1]][r][0] += 1
                                            hh = True
                                            break
                                    if hh:
                                        break
                        #print('1111')
                    elif father.name == '常量声明':
                        if father.children[-1].name == '常量声明':
                            father.type = father.children[-1].type
                        else:
                            father.type = father.children[-2].type
                        if self.CheckScope(father.children[-3].symbol_info[1], scope[-1][0]):
                            self.errors.append(
                                [father.children[-3].symbol_info[2], father.children[-3].symbol_info[3],
                                 "'%s'常量名字已声明" % father.children[-3].symbol_info[1]])
                        else:
                            con = ConstantInfo()
                            con.type = father.type
                            con.scope = scope[-1][0]
                            con.value = father.children[0].value
                            if father.children[-3].symbol_info[1] not in self.ConstantTable:
                                self.ConstantTable[father.children[-3].symbol_info[1]] = []
                            self.ConstantTable[father.children[-3].symbol_info[1]].append(con)
                    elif father.name == '函数调用':
                        if father.children[-1].symbol_info[1] not in self.FunctionTable:
                            self.errors.append(
                                [father.children[-1].symbol_info[2], father.children[-1].symbol_info[3],
                                 "'%s'函数未声明" % father.children[-1].symbol_info[1]])
                        elif self.FunctionTable[father.children[-1].symbol_info[1]].para_num != father.children[
                            1].parameters:
                            print(father.children[
                            1].parameters)
                            self.errors.append(
                                [father.children[-1].symbol_info[2], father.children[-1].symbol_info[3],
                                 "'%s'函数参数个数不匹配" % father.children[-1].symbol_info[1]])
                        else:
                            father.type = self.FunctionTable[father.children[-1].symbol_info[1]].type
                    elif father.name == '实参':
                        if len(father.children) == 1:
                            father.parameters = 1
                        else:
                            father.parameters = father.children[0].parameters + 1
                    elif father.name == '实参列表':
                        father.parameters = father.children[0].parameters
                    elif father.name == '函数定义参数':
                        val = VariableInfo()
                        val.type = father.type
                        val.scope = scope[-1][0] + ',' + str(scope[-1][1])
                        if len(father.children) == 2:
                            father.type = father.children[-1].type
                            father.parameters = 1

                            if father.children[0].symbol_info[1] not in self.VariableTable:
                                self.VariableTable[father.children[0].symbol_info[1]] = []
                                self.VariableTable[father.children[0].symbol_info[1]].append(val)
                            else:
                                # 判断是否有作用域相同的标识符
                                if self.CheckScope(father.children[0].symbol_info[1], val.scope):
                                    self.errors.append(
                                        [father.children[0].symbol_info[2], father.children[0].symbol_info[3],
                                         "'%s'变量名字已声明" % father.children[0].symbol_info[1]])
                                else:
                                    self.VariableTable[father.children[0].symbol_info[1]].append(val)
                        else:
                            father.type = father.children[-1].type + ',' + father.children[0].type
                            father.parameters = father.children[0].parameters + 1
                            if father.children[2].symbol_info[1] not in self.VariableTable:
                                self.VariableTable[father.children[2].symbol_info[1]] = []
                                self.VariableTable[father.children[2].symbol_info[1]].append(val)
                            else:
                                # 判断是否有作用域相同的标识符
                                if self.CheckScope(father.children[2].symbol_info[1], val.scope):
                                    self.errors.append(
                                        [father.children[2].symbol_info[2], father.children[2].symbol_info[3],
                                         "'%s'变量名字已声明" % father.children[2].symbol_info[1]])
                                else:
                                    self.VariableTable[father.children[2].symbol_info[1]].append(val)
                    elif father.name == '函数定义参数列表':
                        father.type = father.children[0].type
                        father.parameters = father.children[0].parameters
                    elif father.name == '函数定义':
                        if father.children[-2].symbol_info[1] not in self.FunctionTable:
                            self.errors.append(
                                [father.children[-2].symbol_info[2], father.children[-2].symbol_info[3],
                                 "'%s'函数未声明" % father.children[-2].symbol_info[1]])
                        else:
                            if father.children[-1].name == 'void':
                                father.children[-1].type = 'void'
                            if father.children[-1].type != self.FunctionTable[
                                father.children[-2].symbol_info[1]].type:
                                self.errors.append(
                                    [father.children[-2].symbol_info[2], father.children[-2].symbol_info[3],
                                     "'%s'函数返回类型与声明不一致" % father.children[-2].symbol_info[1]])
                            if father.children[2].parameters != self.FunctionTable[
                                father.children[-2].symbol_info[1]].para_num:
                                self.errors.append(
                                    [father.children[-2].symbol_info[2], father.children[-2].symbol_info[3],
                                     "'%s'函数参数个数与声明不一致" % father.children[-2].symbol_info[1]])
                            elif father.children[2].type != self.FunctionTable[
                                father.children[-2].symbol_info[1]].para_type:
                                self.errors.append(
                                    [father.children[-2].symbol_info[2], father.children[-2].symbol_info[3],
                                     "'%s'函数参数与声明不一致" % father.children[-2].symbol_info[1]])

                    elif father.name == '赋值表达式':
                        if father.children[-1].name == 'identifier':
                            if not self.IsDeclare(father.children[-1].symbol_info[1], scope[-1][0]):
                                self.errors.append(
                                    [father.children[-1].symbol_info[2], father.children[-1].symbol_info[3],
                                     "'%s'变量未声明" % father.children[-1].symbol_info[1]])
                            elif self.IsConst(father.children[-1].symbol_info[1], scope[-1][0]):
                                self.errors.append(
                                    [father.children[-1].symbol_info[2], father.children[-1].symbol_info[3],
                                     "'%s'为不可变常量" % father.children[-1].symbol_info[1]])
                            else:
                                if father.children[-1].symbol_info[1] in self.var_num:
                                    for r in self.var_num[father.children[-1].symbol_info[1]]:
                                        leng = len(scope[-1][0])
                                        hh = False
                                        for w in range(leng):
                                            if scope[-1][0][0:leng - w] == r:
                                                self.var_num[father.children[-1].symbol_info[1]][r][0] += 1
                                                hh = True
                                                break
                                        if hh:
                                            break
                        else:
                            if not self.IsDeclare(father.children[-1].children[-1].symbol_info[1], scope[-1][0]):
                                self.errors.append(
                                    [father.children[-1].children[-1].symbol_info[2], father.children[-1].children[-1].symbol_info[3],
                                     "'%s'变量未声明" % father.children[-1].children[-1].symbol_info[1]])
                stack_symbol.append(production[0:idx])
                stack_node.append(father)
                stack_num.append(node_index)
                stack_state.append(int(self.parsing_table[stack_state[-1]][stack_symbol[-1]]))
                node_index += 1
            elif status == 'acc':
                for i in self.var_num:
                    for j in self.var_num[i]:
                        if self.var_num[i][j][0] == 0:
                            self.warning.append([self.var_num[i][j][1][2], self.var_num[i][j][1][3], "'%s'变量声明却未使用"%self.var_num[i][j][1][1]])
                print("接受")
                self.node = stack_node.pop()
                break
            else:
                stack_node.append(Node(name, symbol_info=token[index]))
                self.dot.node(str(node_index), token[index][1])
                stack_num.append(node_index)
                node_index += 1
                if name == '{':
                    scope.append([scope[-1][0] + ',' + str(scope[-1][1]), 0])
                elif name == '}':
                    scope.pop()
                    scope[-1][1] += 1
                index += 1
                stack_symbol.append(name)
                stack_state.append(int(status))
            print(stack_symbol)
            print(stack_state)
            #input()
        # print(self.var_num)
        print(self.function_array_list)

    # 语法树
    def PrintParseTree(self):
        self.dot.render('tree.gv', view=False, format='png', directory='Syntax_Tree')
        '''tree = ''
        for pre, fill, node in RenderTree(self.node):
            tree += ("%s%s\n" % (pre, node.name))
        return tree'''

    def IntermediateCodeGenerator(self, token):
        self.code.clear()
        self.function_array_list.clear()
        self.global_array_list.clear()
        self.function_jubu_list.clear()
        self.function_param_list.clear()
        # 符号列表
        sign_list = []
        for i in token:
            if i[0] == 'keyword' or i[0] == 'Boundary' or i[0] == 'operator':
                name = i[1]
            else:
                name = i[0]
            if name == '||':
                name = 'or'
            sign_list.append(name)
        # 语法树栈
        stack_node = []
        # 状态栈
        stack_state = [0]
        # 符号栈
        stack_symbol = ['#']
        # token下标
        index = 0
        # 初始范围
        scope = [['0', 0]]
        # 中间代码下标
        index_code = 0
        # 计数
        count = 0
        # 记录if语句需要回填的栈
        stack_if = []
        # 记录for语句的循环入口
        stack_for = []
        # 记录break语句的栈，记录break跳出的那行行数和当前循环层数
        stack_break = []
        # 循环层数
        loop_count = 0
        # 记录continue跳出的那行行数和当前循环层数
        stack_continue = []
        # if语句总出口
        stack_if_total = []
        # for语句第三部分
        stack_for_3 = []
        #
        flag_if = True
        over = 0
        # 栈关于函数参数
        para = []
        # 是否在函数内部
        fun_flag = False
        fun_name = None
        # 布尔真出口
        bool_true = []
        # 布尔假出口
        bool_false = []
        while index < len(sign_list):
            name = sign_list[index]
            # print(token[index])
            # print(name)
            # print(stack_state[-1])
            # expected = list(self.parsing_table[stack_state[-1]].keys())
            # print(expected)
            # print()
            status = self.parsing_table1[stack_state[-1]][name]
            if status[0] == 'r':
                production = self.reduction1[int(status[1:])]
                idx = production.find(':')
                father = Node(production[0:idx])
                if idx + 1 < len(production):
                    prod = production[idx + 1:].split(' ')
                    for i in range(len(prod)):
                        stack_state.pop()
                        stack_symbol.pop()
                        stack_node.pop().parent = father
                    if father.name == '数字常量' or father.name == '变量' or father.name == '关系运算符':
                        #print(father.children[0])
                        if len(father.children) == 1:
                            father.value = father.children[0].symbol_info[1]
                        elif len(father.children) == 4:
                            father.value = father.children[-1].symbol_info[1]+'['+father.children[-3].value+']'
                        else:
                            col = 0
                            for i in self.ArrayTable[father.children[-1].symbol_info[1]]:
                                if scope[-1][0].startswith(i.scope):
                                    col = i.col
                            self.code.append(['*', father.children[-3].value, col, 'T' + str(count)])
                            self.code.append(['+', 'T' + str(count), father.children[-6].value, 'T' + str(count + 1)])
                            index_code += 2
                            count += 2
                            father.value = father.children[-1].symbol_info[1] + '[' + 'T' + str(count - 1) + ']'
                    elif father.name == '数组':
                        if len(father.children) == 4:
                            father.value = father.children[-1].symbol_info[1]+'['+father.children[-3].value+']'
                        else:
                            col = 0
                            for i in self.ArrayTable[father.children[-1].symbol_info[1]]:
                                if scope[-1][0].startswith(i.scope):
                                    col = i.col
                            self.code.append(['*', father.children[-3].value, col, 'T' + str(count)])
                            self.code.append(['+', 'T' + str(count), father.children[-6].value, 'T' + str(count + 1)])
                            index_code += 2
                            count += 2
                            father.value = father.children[-1].symbol_info[1] + '[' + 'T' + str(count - 1) + ']'
                            # father.value = father.children[-1].symbol_info[1] + '[' + father.children[-3].value + ']'+'['+father.children[-5].value+']'
                    elif father.name == '常量' or father.name == '算术表达式':
                        father.value = father.children[0].value
                    elif father.name == '因子':
                        if len(father.children) == 1:
                            father.value = father.children[0].value
                        else:
                            father.value = father.children[1].value
                    elif father.name == '项' or father.name == '加减表达式':
                        if len(father.children) == 1:
                            father.value = father.children[0].value
                        elif len(father.children) == 2 and is_number(father.children[0].value):
                            father.value = '-'+father.children[0].value
                        elif len(father.children) == 2:
                            father.value = 'T' + str(count)  # 修改2
                            self.code.append(
                                ['-', father.children[0].value, '',
                                 father.value])
                            index_code += 1
                            count += 1
                        else:
                            #print(father.children)
                            father.value = 'T'+str(count)  # 修改2
                            self.code.append([father.children[1].name, father.children[2].value, father.children[0].value, father.value])
                            index_code += 1
                            count += 1
                        #print(father.value)
                    elif father.name == '算术表达式' or father.name == '表达式':
                        father.value = father.children[0].value
                        #print(father.value)
                        #print(father.children)
                    elif father.name == '赋值表达式':
                        if len(bool_true) != 0:  # 有布尔表达式
                            for i in bool_true:
                                self.code[i][3] = index_code
                        if len(bool_false) != 0:
                            for i in bool_false:
                                self.code[i][3] = index_code + 2
                            bool_true.clear()
                            bool_false.clear()
                            self.code.append([father.children[1].name, '1', '', father.children[-1].value])
                            self.code.append(['j', '', '', index_code + 3])
                            self.code.append([father.children[1].name, '0', '', father.children[-1].value])
                            index_code += 3
                        else:
                            self.code.append(
                                [father.children[1].name, father.children[0].value, '',
                                 father.children[-1].value])
                            index_code += 1
                        father.value = father.children[0].value
                    elif father.name == '布尔因子':
                        if len(father.children) == 1:
                            father.value = father.children[0].value
                        elif len(father.children) == 3:
                            father.value = father.children[1].value
                        else:
                            father.value = 'T'+str(count)  # 修改1
                            self.code.append(['!', father.children[0].value, '', father.value])
                            index_code += 1
                            count += 1
                    elif father.name == '布尔项' or father.name == '布尔表达式':
                        if len(father.children) == 1:
                            father.value = father.children[0].value
                        elif father.name == '布尔项' and father.children[0].value is not None:
                            self.code.append(['jnz', father.children[0].value, '', index_code + 2])
                            self.code.append(['j', '', '', -1])
                            bool_false.append(index_code + 1)
                            if sign_list[index] == 'or':
                                bool_true.append(index_code)
                                self.code.pop()
                                bool_false.pop()
                                index_code -= 1
                            index_code += 2
                            # print(exit_code)
                        elif father.name == '布尔表达式' and father.children[0].value is not None:
                            self.code.append(['jz', father.children[0].value, '', index_code + 2])
                            self.code.append(['j', '', '', 0])  # 跳到真出口
                            bool_true.append(index_code + 1)
                            if sign_list[index] != 'or':
                                bool_false.append(index_code)
                                self.code.pop()
                                bool_true.pop()
                                index_code -= 1
                            index_code += 2

                    elif father.name == '布尔项or':
                        if father.children[1].value is not None:
                            self.code.append(['jz', father.children[1].value, '', index_code + 2])
                            self.code.append(['j', '', '', 0])  # 跳到真出口
                            bool_true.append(index_code + 1)
                            index_code += 2
                        else:
                            for i in bool_false:
                                self.code[i][3] = index_code
                            bool_false.clear()

                    elif father.name == '布尔项and':
                        if father.children[1].value is not None:
                            self.code.append(['jnz', father.children[1].value, '', index_code + 2])
                            self.code.append(['j', '', '', -1])  # 跳到假出口
                            bool_false.append(index_code + 1)
                            index_code += 2

                    elif father.name == '关系表达式':
                        print('tttttttttttttttttttttttt')
                        print(sign_list[index])
                        if sign_list[index] != 'or':
                            self.code.append(
                                ['j' + father.children[1].value, father.children[2].value, father.children[0].value,
                                 index_code + 2])
                            self.code.append(['j', '', '', -1])
                            bool_false.append(index_code + 1)
                            index_code += 2
                        else:
                            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                            self.code.append(
                                ['j' + father.children[1].value, father.children[2].value, father.children[0].value,
                                 0])  # 跳转真出口
                            # self.code.append(['j', '', '', exit_code])
                            bool_true.append(index_code)
                            index_code += 1
                            print(bool_true)
                    elif father.name == '变量声明':
                        if fun_flag:
                            if len(father.children) >= 3 and father.children[-3].name == 'identifier':
                                self.function_jubu_list[fun_name].append(father.children[-3].symbol_info[1])
                            elif father.children[-2].name == 'identifier':
                                self.function_jubu_list[fun_name].append(father.children[-2].symbol_info[1])
                            elif len(father.children) >= 3 and father.children[-3].name == '数组':
                                if len(father.children[-3].children) == 4:
                                    self.function_array_list[fun_name].append([father.children[-3].children[-1].symbol_info[1], father.children[-3].children[1].value, ''])
                                else:
                                    self.function_array_list[fun_name].append([father.children[-3].children[-1].symbol_info[1], father.children[-3].children[4].value, father.children[-3].children[1].value])
                            elif father.children[-2].name == '数组':
                                if len(father.children[-2].children) == 4:
                                    self.function_array_list[fun_name].append(
                                        [father.children[-2].children[-1].symbol_info[1],
                                         father.children[-2].children[1].value, ''])
                                else:
                                    self.function_array_list[fun_name].append(
                                        [father.children[-2].children[-1].symbol_info[1],
                                         father.children[-2].children[4].value, father.children[-2].children[1].value])
                        else:
                            if len(father.children) >= 3 and father.children[-3].name == '数组':
                                if len(father.children[-3].children) == 4:
                                    self.global_array_list.append([father.children[-3].children[-1].symbol_info[1], father.children[-3].children[1].value, ''])
                                else:
                                    self.global_array_list.append([father.children[-3].children[-1].symbol_info[1], father.children[-3].children[4].value, father.children[-3].children[1].value])
                            elif father.children[-2].name == '数组':
                                if len(father.children[-2].children) == 4:
                                    self.global_array_list.append(
                                        [father.children[-2].children[-1].symbol_info[1],
                                         father.children[-2].children[1].value, ''])
                                else:
                                    self.global_array_list.append(
                                        [father.children[-2].children[-1].symbol_info[1],
                                         father.children[-2].children[4].value, father.children[-2].children[1].value])
                        if len(father.children) == 4 or len(father.children) == 5:
                            if len(bool_true) != 0:  # 有布尔表达式
                                for i in bool_true:
                                    self.code[i][3] = index_code
                            if len(bool_false) != 0:
                                for i in bool_false:
                                    self.code[i][3] = index_code + 2
                                bool_true.clear()
                                bool_false.clear()
                                self.code.append([father.children[1].name, '1', '', father.children[-1].symbol_info[1]])
                                self.code.append(['j', '', '', index_code + 3])
                                self.code.append([father.children[1].name, '0', '', father.children[-1].symbol_info[1]])
                                index_code += 3
                            else:
                                if father.children[0].name == '表达式':
                                    self.code.append(
                                        ['=', father.children[0].value, '', father.children[2].symbol_info[1]])
                                    index_code += 1
                    elif father.name == '常量声明':
                        if fun_flag:
                            self.function_jubu_list[fun_name].append(father.children[2].symbol_info[1])
                        self.code.append(['=', father.children[0].value, '', father.children[2].symbol_info[1]])
                        index_code += 1

                    elif father.name == 'if无else':
                        print(stack_symbol[-1])
                        if stack_symbol[-1] != 'if有else':
                            stack_if_total.append([])
                        # exit_true = index_code
                        if father.children[1].value is not None:
                            self.code.append(['jz', father.children[1].value, '', -1])
                            bool_false.append(index_code)
                            index_code += 1
                        if len(bool_true) != 0:  # 有布尔表达式
                            for i in bool_true:
                                self.code[i][3] = index_code
                        stack_if.append(bool_false.copy())
                        bool_true.clear()
                        bool_false.clear()
                    elif father.name == 'if有else' or father.name == '带if的循环语句有else':
                        stack_if_total[-1].append(index_code)
                        self.code.append(['j', '', '', index_code])
                        index_code += 1
                        q = stack_if.pop()
                        for i in q:
                            self.code[i][3] = index_code
                        flag_if = False
                    elif father.name == 'if语句' and name != 'else' or father.name == '带if的循环语句' and name != 'else':  # if语句结束
                        if len(stack_if_total) != 0:
                            q = stack_if_total.pop()
                            # print(q)
                            for i in q:
                                self.code[i][3] = index_code
                        if flag_if:
                            if len(stack_if) != 0:
                                q = stack_if.pop()
                                for i in q:
                                    self.code[i][3] = index_code
                        flag_if = True
                    elif father.name == 'for语句(0)':
                        loop_count += 1
                        # print(index_code)
                    elif father.name == 'for语句(1)':
                        stack_for.append([index_code, []])
                    elif father.name == 'for语句(2)':
                        if len(bool_true) != 0:  # 有布尔表达式
                            for i in bool_true:
                                self.code[i][3] = index_code
                        stack_for[-1][1].extend(bool_false.copy())
                        bool_false.clear()
                        bool_true.clear()
                        over = index_code
                    elif father.name == 'for语句(3)':
                        shizi = []
                        for yy in range(index_code - over):
                            shizi.append(self.code.pop())
                        stack_for_3.append(shizi)
                        index_code = over
                    elif father.name == 'for语句' or father.name == 'while语句':
                        if father.name == 'for语句':
                            q = stack_for_3.pop()
                            for i in range(len(q)):
                                self.code.append(q.pop())
                                index_code += 1
                        q = stack_for.pop()
                        self.code.append(
                            ['j', '', '', q[0]])
                        index_code += 1
                        for i in q[1]:
                            self.code[i][3] = index_code
                        if len(stack_break) > 0 and stack_break[-1][1] == loop_count:
                            self.code[stack_break[-1][0]][3] = index_code
                            stack_break.pop()
                        if len(stack_continue) > 0 and stack_continue[-1][1] == loop_count:
                            self.code[stack_continue[-1][0]][3] = q[0]
                            stack_continue.pop()
                        loop_count -= 1
                    elif father.name == 'break语句':
                        # 暂时不知道跳出口，记0
                        self.code.append(
                            ['j', '', '', 0])
                        stack_break.append([index_code, loop_count])
                        index_code += 1
                    elif father.name == 'continue语句':
                        stack_continue.append([index_code, loop_count])
                        self.code.append(
                            ['j', '', '', 0])
                        index_code += 1
                    elif father.name == 'while(1)' or father.name == 'do(1)':
                        loop_count += 1
                        stack_for.append([index_code, []])
                    elif father.name == 'while(2)':
                        #print(sign_list[index])
                        '''if father.children[1].value is not None:
                            self.code.append(['jz', father.children[1].value, '', exit_code])
                            exit_code = index_code - 1
                            index_code += 1'''
                        if sign_list[index] != ';':
                            if father.children[1].value is not None:  # 表达式不是布尔表达式
                                self.code.append(['jz', father.children[1].value, '', -1])
                                bool_false.append(index_code)
                                index_code += 1
                            if len(bool_true) != 0:  # 有布尔表达式
                                for i in bool_true:
                                    self.code[i][3] = index_code
                            stack_for[-1][1].extend(bool_false.copy())
                            bool_false.clear()
                            bool_true.clear()
                        else:
                            print(bool_true)
                            print(stack_for)
                            if father.children[1].value is not None:  # 表达式不是布尔表达式
                                self.code.append(['jnz', father.children[1].value, '', 0])
                                bool_true.append(index_code)
                                index_code += 1
                            loop_count -= 1
                            stack_for.pop()
                            if len(bool_true) != 0:  # 有布尔表达式
                                for i in bool_true:
                                    self.code[i][3] = stack_for[-1][0]
                            if len(bool_false) != 0:  # 有布尔表达式
                                for i in bool_false:
                                    self.code[i][3] = index_code
                                if self.code[-1][0] == 'j':
                                    for i in bool_false[:-1]:
                                        self.code[i][3] = index_code-1
                                    self.code.pop()
                                    self.code[-1][3] = stack_for[-1][0]
                                    index_code -= 1
                                elif self.code[-1][0] == 'jz':
                                    self.code[-1][0] = 'jnz'
                                    self.code[-1][3] = stack_for[-1][0]
                            stack_for.pop()
                            bool_false.clear()
                            bool_true.clear()
                    elif father.name == '实参':
                        self.code.append(['para', father.children[0].value, '', ''])
                        index_code += 1
                    elif father.name == 'return语句':
                        if father.children[1].value is None:
                            self.code.append(['ret', '', '', ''])
                        else:
                            self.code.append(['ret', father.children[1].value, '', ''])
                        index_code += 1
                    elif father.name == '函数调用':
                        if self.FunctionTable[father.children[-1].symbol_info[1]].type != 'void':
                            self.code.append(['call', father.children[-1].symbol_info[1], '', 'T' + str(count)])
                            father.value = 'T' + str(count)
                            count += 1
                        else:
                           self.code.append(['call', father.children[-1].symbol_info[1], '', ''])
                        index_code += 1
                    elif father.name == '函数(2)':
                        fun_name = father.children[0].symbol_info[1]
                        if fun_name not in self.function_jubu_list:
                            self.function_jubu_list[fun_name] = []
                        if fun_name not in self.function_array_list:
                            self.function_array_list[fun_name] = []
                        self.code.append([father.children[0].symbol_info[1], '', '', ''])
                        index_code += 1
                    elif father.name == '函数(1)':
                        print(para)
                        self.function_param_list[fun_name] = para.copy()
                        para.clear()
                        fun_flag = True
                    elif father.name == '函数定义':
                        if self.FunctionTable[fun_name].type == 'void':
                            self.code.append(['ret', '', '', ''])
                        fun_flag = False
                    elif father.name == '函数定义参数':
                        # self.code.append(['pop', father.children[-2].symbol_info[1], '', ''])
                        para.append(father.children[-2].symbol_info[1])
                        # index_code += 1
                    elif father.name == '主函数':
                        self.code.append(['main', '', '', ''])
                        index_code += 1
                    elif father.name == '程序(1)' or father.name == '程序(2)':
                        self.code.append(['sys', '', '', ''])
                        index_code += 1
                    # elif father
                    #elif
                #print(self.code)
                # print()
                stack_symbol.append(production[0:idx])
                stack_node.append(father)
                stack_state.append(int(self.parsing_table1[stack_state[-1]][stack_symbol[-1]]))
            elif status == 'acc':
                print("接受")
                # self.node = stack_node.pop()
                break
            else:
                stack_node.append(Node(name, symbol_info=token[index]))
                if name == '{':
                    scope.append([scope[-1][0] + ',' + str(scope[-1][1]), 0])
                elif name == '}':
                    scope.pop()
                    scope[-1][1] += 1
                index += 1
                stack_symbol.append(name)
                stack_state.append(int(status))
            print(stack_symbol)
        print(self.function_array_list)
        print(self.global_array_list)
        print(self.function_jubu_list)


'''f = open('test.txt', 'r', encoding='utf-8')
lr1 = CLRParser()
lr1.input(f.read())
lr1.Action_and_GoTo_Table()
lr1.draw_graphic()'''