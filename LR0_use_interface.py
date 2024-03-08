from collection import FirstAndFollow
from graphviz import Digraph
from Analyzer import AnalyzerLex
from anytree import Node as AnyTreeNode, RenderTree
# 此LR0只用于自定义语法分析，不带有语义分析、错误修复以及中间代码生成


class Node(AnyTreeNode):
    def __init__(self, value, symbol_info=None, **kwargs):
        super().__init__(value, **kwargs)
        self.symbol_info = symbol_info
        self.type = None
        self.value = None
        self.parameters = 0


class CLRParser:
    def __init__(self):
        self.first = None
        # follow 集合
        self.follow = None
        # 产生式
        self.Formula = None
        # 文法开始符号
        self.begin = ''
        # 归约式,也是产生式
        self.reduction = []
        # 分析表
        self.parsing_table = dict()
        # 语法树根节点
        self.node = None
        # 终结状态
        self.Final_State = set()

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
        self.follow = p.last
        self.Formula = p.Formula
        self.begin = p.begin

    def Action_and_GoTo_Table(self):
        is_LR = True
        # 统计所有终结符
        terminal = set()
        for i in self.first:
            terminal.update(self.first[i])
        for i in self.follow:
            terminal.update(self.follow[i])
        terminal.discard('ε')
        terminal = list(terminal)
        # 用于归约式编号的字典
        reduction = dict()
        number = 1
        reduction[self.begin+"'"+ ':' + self.begin] = 0
        for key, value in self.Formula.items():
            print(key)
            print(value)
            for g in value.split('|'):
                word = [k for k in g.split(' ') if k != '']
                if word == ['ε']:
                    word = []
                if key + ':' + " ".join(word) not in reduction:
                    reduction[key + ':' + " ".join(word)] = number
                    number += 1
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
        stack = [[self.begin, ['.', self.begin]]]
        # 加入开始产生式
        state_family.append([self.begin+"'", ['.', self.begin]])
        prod_state[self.begin+"'"+'→'+"".join(['.', self.begin])] = label
        id0.append(label)
        label += 1

        while len(stack) > 0:  # 将所有终结符处理完毕
            h = stack.pop(0)
            prod = self.Formula[h[0]]
            inx = h[1].index('.')
            # .后面为非终结符，将非终结符的的产生式加入当前状态，同时去除相同状态内的相同元素
            for g in prod.split('|'):
                word = [k for k in g.split(' ') if k != '']
                if word == ['ε']:
                    word = []
                word.insert(0, '.')
                st = h[0]+'→'+''.join(word)
                if st not in prod_state:
                    prod_state[st] = label
                    label += 1
                # 在id0说明存在这个状态，直接跳过
                if prod_state[st] in id0:
                    continue
                id0.append(prod_state[st])
                state_family.append([h[0], word])
                if len(word) > 1 and word[1] in self.Formula:
                    stack.append([word[1], word])
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
        # number = 0
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
                    if len(status) != 1:
                        is_LR = False
                    self.Final_State.add(father)
                    # if i[0] + ':' + ' '.join(i[1][:-1]) not in reduction:
                        # print(i[0] + ':' + ' '.join(i[1][:-1]))
                    #    reduction[i[0] + ':' + ' '.join(i[1][:-1])] = number
                    #    number += 1
                    if i[0] + ':' + ' '.join(i[1][:-1]) == self.begin + "'" + ":" + self.Formula[self.begin + "'"]:
                        reduction_table.append([father, '#', reduction[i[0] + ':' + ' '.join(i[1][:-1])]])
                    else:
                        for q in terminal:
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
                    new_status.append(itemset)
                    st = status[j][0]+'→'+''.join(u)
                    if st not in prod_state:
                        prod_state[st] = label
                        label += 1
                    id_n.append(prod_state[st])
                    # 如果现在'.'后为非终结符，则需加入这个非终结符的状态,如果加入的这个'.'后也是非终结符则还需再加，直到不是非终结符
                    stack = []
                    if idx+2 < len(u) and u[idx+2] in self.Formula:  # 是非终结符
                        stack = [[u[idx+2], u]]
                    else:
                        continue
                    while len(stack) > 0:  # 将所有终结符处理完毕
                        h = stack.pop(0)
                        prod = self.Formula[h[0]]
                        inx = h[1].index('.')
                        for g in prod.split('|'):
                            word = [k for k in g.split(' ') if k != '']
                            if word == ['ε']:
                                word = []
                            word.insert(0, '.')
                            st = h[0] + '→' + ''.join(word)
                            if st not in prod_state:
                                prod_state[st] = label
                                label += 1
                            if prod_state[st] in id_n:
                                continue
                            id_n.append(prod_state[st])
                            new_status.append([h[0], word])
                            if len(word) > 1 and word[1] in self.Formula:
                                stack.append([word[1], word])
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

        lab = ''
        prod_state_exchange = {v: k for k, v in self.prod_state.items()}
        for i in range(len(self.status_include_num)):
            lab += 'I' + str(i) + ':\n'
            for j in self.status_include_num[i]:
                lab += prod_state_exchange[j] + '\n'
            lab += '\n'

        return is_LR, lab

    def draw_graphic(self):
        print(self.Final_State)
        prod_state_exchange = {v: k for k, v in self.prod_state.items()}
        dot = Digraph(comment='LR_Digraph')
        for i in range(len(self.status_include_num)):
            lab = 'I' + str(i) + '\n'
            for j in self.status_include_num[i]:
                lab += prod_state_exchange[j] + '\n'
            if i not in self.Final_State:
                dot.node(str(i), lab, fontname="SimHei", shape='rectangle')
            else:
                dot.node(str(i), lab, fontname="SimHei", shape='doublecircle')
        for i in self.direction:
            dot.edge(str(i[0]), str(i[2]), i[1], fontname="SimHei")
        dot.render('LR_Digraph.gv', view=False, format='png', directory='LR0_Digraph')

    def ControlProgram(self, token):
        self.dot.clear()

        # 节点标号
        node_index = 0
        stack_num = []

        # 符号列表
        sign_list = []

        # 界面展示信息
        information1 = []  # 符号栈
        information2 = []  # 状态栈
        information3 = []  # 动作信息
        information4 = []  # 剩余符号

        sign_list.extend(token)
        sign_list.append('#')

        # 语法树栈
        stack_node = []
        # 状态栈
        stack_state = [0]
        # 符号栈
        stack_symbol = ['#']
        # token下标
        index = 0
        print(sign_list)
        result = True
        while index < len(sign_list):
            information1.append(stack_symbol.copy())
            information2.append(stack_state.copy())
            information4.append(sign_list[index:].copy())
            name = sign_list[index]
            if name not in self.parsing_table[stack_state[-1]]:
                result = False
                break
            status = self.parsing_table[stack_state[-1]][name]
            information3.append(status)
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
                stack_symbol.append(production[0:idx])
                stack_node.append(father)
                stack_num.append(node_index)
                information3[-1] = information3[-1] + '   goto' + '%s' % self.parsing_table[stack_state[-1]][stack_symbol[-1]]
                stack_state.append(int(self.parsing_table[stack_state[-1]][stack_symbol[-1]]))
                node_index += 1
            elif status == 'acc':
                print("接受")
                self.node = stack_node.pop()
                break
            else:
                stack_node.append(Node(name, symbol_info=token[index]))
                self.dot.node(str(node_index), token[index])
                stack_num.append(node_index)
                node_index += 1
                index += 1
                stack_symbol.append(name)
                stack_state.append(int(status))
            print(stack_symbol)
            # information1.append(stack_symbol.copy())
            # information2.append(stack_state.copy())

        return information2, information1, information4, information3, result

    # 语法树
    def PrintParseTree(self):
        self.dot.render('tree.gv', view=False, format='png', directory='Syntax_Tree')



'''lr1 = CLRParser()
lr1.input('E:a A|b B\nA:c A|d\nB:c B|d')
t = lr1.Action_and_GoTo_Table()
print(t)
lr1.draw_graphic()'''
'''tokens = []
lex = AnalyzerLex()
lex.input('a b c')'''

#f = open('test.txt', 'r', encoding='utf-8')
'''lr1 = CLRParser()
lr1.input('S:a S|b S|c ')
lr1.Action_and_GoTo_Table()
tokens = []
lex = AnalyzerLex()
lex.input('a b c')
while True:
    tok = lex.token()
    if not tok:
        break
    tokens.append([tok.type, tok.value, tok.lineno,lex.find_column(tok.lexer.lexdata, tok)])
tokens.append(['keyword', '#'])
t1,t2,t3,t4 = lr1.ControlProgram(tokens)
lr1.draw_graphic()
print(t4)'''