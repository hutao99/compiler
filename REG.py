from graphviz import Digraph

# 生成nfa的状态转换图
def nfa_graph(start, end, result):    # 参数分别为开始节点， 结束节点和nfa 经过正规式转nfa后 初始节点和开始节点只有一个
    filename = './Reg_Graph/NFA'
    nfa_graph = Digraph(filename, 'NFA_graph', None, None, 'png', None, "UTF-8")
    nfa_graph.attr(rankdir="LR")  # 图从左到右 L -> R
    for value in result:
        if value[0] == start:  # 开始节点填满红色
            nfa_graph.node(str(value[0]), str(value[0]), fillcolor="red", style="filled")
        else:
            nfa_graph.node(str(value[0]), str(value[0]))
        if value[2] == end:  # 结束节点改成双圆
            nfa_graph.node(str(value[2]), str(value[2]), shape="doublecircle")
        else:
            nfa_graph.node(str(value[2]), str(value[2]))
        # 边
        nfa_graph.edge(str(value[0]), str(value[2]), label=value[1], rankdir="LR")
    nfa_graph.render()

def Lexical_Analysis(code, mfa, final_states):  # 依靠mfa对需要分析的代码code进行词法分析,final_states为终结状态集
    result = []  # 识别结果
    state = 0  # 现在所处的状态
    index1 = 0  # code[index1 : index] 为识别成功的单词
    for index, char in enumerate(code):
        if index < index1:
            continue
        if char == " " or char == "\n":  # 除去空格和换行符
            index1 += 1
        else:
            flag1 = 0
            for arc in mfa:
                if arc[0] == state and arc[1] == char:  # 找到开始状态和输入符号
                    state = arc[2]  # 进入下一个状态
                    flag1 = 1
                    break
            if flag1 == 0:  # 表示当前输入符有错
                index2 = index
                while index2 < len(code):  # 一直找到空格或者换行位置
                    if code[index2] not in [" ", "\n"]:
                        index2 += 1
                    else:
                        break
                result.append(code[index1: index2] + "识别错误")
                index1 = index2 + 1
                state = 0
            elif state not in final_states and index + 1 < len(code) and code[index + 1] in [" ", "\n"]:
                index2 = index
                while index2 < len(code):  # 一直找到不是空格和换行位置
                    if code[index2] in [" ", "\n"]:
                        index2 += 1
                    else:
                        break
                result.append(code[index1: index + 1] + "识别错误")
                index1 = index2 + 1
                state = 0
            elif state in final_states:  # 如果已经到达终结状态了就 判断是否还能继续识别下一个符号 不能就重新将state置0
                flag = 0
                for arc in mfa:
                    if state == arc[0] and index+1 < len(code) and (code[index + 1] == arc[1]):  # 能识别下一个符号
                        flag = 1
                        break
                if flag == 0:
                    print(index)
                    if index+1 < len(code) and (code[index + 1] not in [" ", "\n"]):  # 后面有错误的输入符
                        index2 = index
                        while index2 < len(code):   # 一直找到空格或者换行位置
                            if code[index2] not in [" ", "\n"]:
                                index2 += 1
                            else:
                                break
                        result.append(code[index1: index2] + "识别错误")
                        index1 = index2 + 1
                        state = 0
                    else:
                        result.append(code[index1: index + 1] + "识别成功")  # [index1: index]不包含index
                        index1 = index + 1
                        state = 0
    if state != 0 and (code[index1: len(code)] + "识别错误") not in result:
        result.append(code[index1: len(code)] + "识别错误")
    return result

"""
    多个nfa的合并，主要思路是：将多个nfa放在一个列表里nfa_uniong，将头两个nfa以或的形式 组合成新的一个nfa
    然后在nfa_union中删去头两个nfa，在nfa_union的第一个位置插入新的nfa， 当nfa_union的长度为1的时候表示合并完成
"""
def nfa_associate(nfa_union):
    id_max = 0
    while len(nfa_union) > 1:
        nfa1 = nfa_union[0]
        for index, arc in enumerate(nfa1):  # 对编号进行修改
            nfa1[index][0] += 1
            nfa1[index][2] += 1
            if nfa1[index][0] > id_max:
                id_max = nfa1[index][0]
            if nfa1[index][2] > id_max:
                id_max = nfa1[index][2]
        id_max += 1
        new_nfa = nfa1
        new_nfa.insert(0, [0, 'ε', new_nfa[0][0]])
        new_nfa.append([new_nfa[len(new_nfa) - 1][2], 'ε', id_max])
        end = id_max     # 记录结束状态,后面添加要用到
        nfa2 = nfa_union[1]
        add = id_max + 1
        for index, arc in enumerate(nfa2):  # 对编号进行修改
            nfa2[index][0] += add
            nfa2[index][2] += add
            if nfa2[index][0] > id_max:
                id_max = nfa2[index][0]
            if nfa2[index][2] > id_max:
                id_max = nfa2[index][2]
        new_nfa.append([0, 'ε', nfa2[0][0]])
        for arc in nfa2:
            new_nfa.append([arc[0], arc[1], arc[2]])
        id_max += 1
        new_nfa.append([new_nfa[len(new_nfa) - 1][2], 'ε', end])
        # 删除头两个nfa
        nfa_union.pop(0)
        nfa_union.pop(0)
        # 在第一个位置插入新的nfa
        nfa_union.insert(0, new_nfa)
    # 返回合并完成的nfa即剩下的最后一个
    return nfa_union[0]


class NfaDfaMfa:
    def __init__(self, text):
        self.text = text  # 输入串 即输入的正规式
        self.index = 0  # 输入符号串的下标
        self.max = 0  # 即将用到的状态, max = 2表示状态0和状态1已经被使用
        self.operator = ["|", "*", "(", ")", "·", "#"]  # 算符
        self.symbol_stack = []  # 符号栈,用列表实现栈
        self.state_stack = []  # 状态栈
        self.arc_queue = []  # 弧队列，用列表实现队列，这里是嵌套列表  [[2,'a',3]]表示 第一条弧为状态2由'a'到状态3
        # 优先符号表
        self.prior_table = [['>', '>', '<', '>', '<', '>'],
                            ['<', '>', '<', '>', '<', '>'],
                            ['<', '<', '<', '=', '<', 'error'],
                            ['>', '>', 'error', '>', '>', '>'],
                            ['>', '>', 'error', '>', '>', '>'],
                            ['<', '<', '<', 'error', '<', '=']]
        self.prior_table_assist = {'·': 0, '|': 1, '(': 2, ')': 3, '*': 4, '#': 5}
        # 对输入串进行改造
        self.final_text = ""
        for index, value in enumerate(text):
            self.final_text += value
            if value == ")":
                if index + 1 < len(text) and (text[index + 1] not in self.operator or text[index + 1] == "("):
                    self.final_text += "·"
            elif value == "*":
                if index + 1 < len(text) and (text[index + 1] not in self.operator or text[index + 1] == "("):
                    self.final_text += "·"
            elif value not in self.operator:
                if index + 1 < len(text) and (text[index + 1] not in self.operator or text[index + 1] == "("):
                    self.final_text += "·"
        self.final_text += "#"
        # print(self.final_text)

    # 正规式转换为NFA
    def reg_to_nfa(self):
        self.index = 0
        self.symbol_stack.append("#")
        # 输入字符不为#或者符号栈顶元素不为#
        while self.final_text[self.index] != "#" or self.symbol_stack[len(self.symbol_stack) - 1] != "#":
            # print(self.symbol_stack)
            value = self.final_text[self.index]
            # 当前输入字符是操作数
            if value not in self.operator:
                # print("压入" + value)
                self.arc_queue.append([self.max, value, self.max + 1])  # nfa的弧入队列
                self.state_stack.append(str(self.max))  # 起始结点入状态栈
                self.max += 2
                self.index += 1
            else:
                # 比较符号栈顶元素和输入字符的优先关系
                value1 = self.symbol_stack[len(self.symbol_stack) - 1]  # 符号栈顶元素
                row = self.prior_table_assist[value1]  # 符号栈顶元素对应的行
                col = self.prior_table_assist[value]  # 输入字符对应的列
                contact = self.prior_table[row][col]
                # print(value1 + '\t' + contact + '\t' + value)
                if contact == "<":  # 符号栈顶元素优先级低于输入字符
                    self.symbol_stack.append(value)  # 当前输入符号进符号栈
                    self.index += 1
                elif contact == "=":  # 优先级相等
                    self.symbol_stack.pop()  # 符号栈栈顶出栈
                    self.index += 1
                elif contact == ">":  # 符号栈顶元素优先级高于输入字符
                    symbol = self.symbol_stack.pop()  # 符号栈栈顶元素出栈
                    if symbol == "|":
                        # 状态栈2个栈顶元素出栈,构造s|t的表达式------产生新初始节点连接到s和t的起始节点，s和t的终结点连接到新终结点
                        s = self.state_stack.pop()
                        t = self.state_stack.pop()
                        # print(self.arc_queue)
                        # print(s)
                        # print(t)
                        """
                            新弧可能有多条, 因为 "·" 和 "*" 中添加了多条
                            或运算是分成两条分弧, 所以多条弧会对或运算产生影响
                            因此需要找到最长的（即最终的）弧来进行或运算
                            这里直接找到最后一个即可，因为添加弧的过程中每天新弧都比之前的弧长
                        """
                        # new_list = [self.max, 'ε']  # S|T应该当成一条弧
                        for index, arc in enumerate(self.arc_queue):  # 找到起始状态为 s 状态的弧
                            if arc[0] == int(s):
                                new_list = [self.max, 'ε']  # 与下文中的 new_list2 = [] 作用相同
                                # 构造新弧入队列
                                # new_list = [self.max, 'ε']
                                for point in arc:
                                    new_list.append(point)
                                new_list.append('ε')
                                new_list.append(self.max + 1)

                        for index, arc in enumerate(self.arc_queue):  # 找到起始状态为 t 状态的弧
                            if arc[0] == int(t):
                                # N(t)在 弧队列中有可能有多条,最后面的一条才是最完整的并且是目前需要用到的
                                new_list2 = []  #
                                for value in new_list:
                                    new_list2.append(value)  # 直接 new_list2 = new_list  会出错
                                # 构造新弧入队列
                                # new_list = [self.max, 'ε']
                                new_list2.append(self.max)
                                new_list2.append('ε')
                                for point in arc:
                                    new_list2.append(point)
                                new_list2.append('ε')
                                new_list2.append(self.max + 1)
                        # print(new_list2)
                        self.arc_queue.append(new_list2)
                        self.state_stack.append(self.max)  # 起始节点入状态栈
                        self.max += 2
                    elif symbol == "·":
                        # 状态栈2个栈顶元素出栈,构造s·t的表达式-------S的终节点变成T的起始节点
                        s = self.state_stack.pop()
                        t = self.state_stack.pop()
                        # print(self.arc_queue)
                        # print(s)
                        # print(t)
                        """
                        新弧可能有多条, 因为 "|" 中已经考虑到了有多条，所以这里全部添加不影响, 
                        且连接运算是直接在弧后面添加所以多条弧对连接运算也无影响（原来最长的添加完后还是最长的）最长就是最终的
                        """
                        new_list_total = []  # 新弧可能有多条
                        for index, arc in enumerate(self.arc_queue):  # 找到起始状态为 t 状态的弧
                            if arc[0] == int(t):
                                # 构造新弧入队列
                                new_list = arc[0:len(arc) - 1]  # 把除终结点以外的东西加入到新弧中
                                for index1, arc1 in enumerate(self.arc_queue):  # 找到起始状态为s状态的弧
                                    if arc1[0] == int(s):
                                        for point in arc1:
                                            new_list.append(point)  # s的弧压入到新弧

                                # [1,'a',2,'1','b','2'] 添加[3,'b',4]只执行上述操作会变成[1,'a',2,'1','b',3,'b',4]
                                for index2, state in enumerate(new_list):
                                    if state == arc[len(arc) - 1]:
                                        new_list[index2] = int(s)
                                # print(new_list)
                                new_list_total.append(new_list)
                        for new_list in new_list_total:
                            # print(new_list)
                            self.arc_queue.append(new_list)  # 新弧入队列
                        self.state_stack.append(int(t))  # 起始节点入状态栈

                    elif symbol == "*":
                        # 构造S*的nfa
                        s = self.state_stack.pop()
                        # print(s)
                        # print(self.arc_queue)
                        """
                            新弧可能有多条, 因为 "|" 中已经考虑到了有多条，所以这里全部添加不影响, 
                            且闭包运算和连接运算一样都是直接在弧后面添加所以多条弧对连接运算也无影响
                            （原来最长的添加完后还是最长的）最长的就是最终的
                        """
                        new_list_total = []  # 新弧可能有多条
                        for index, arc in enumerate(self.arc_queue):  # 找到起始状态为s状态的弧
                            if arc[0] == int(s):
                                new_list = [self.max, 'ε']
                                for point in arc:
                                    new_list.append(point)  # 依次加入s的各个节点
                                # s的终结点引空弧到新的终结点
                                new_list.append('ε')
                                new_list.append(self.max + 1)
                                # s的终结点引空弧到开始节点
                                end = arc[len(arc) - 1]
                                new_list.append(end)
                                new_list.append('ε')
                                new_list.append(arc[0])
                                # 新初始节点引空弧到终结点
                                new_list.append(self.max)
                                new_list.append('ε')
                                new_list.append(self.max + 1)
                                new_list_total.append(new_list)
                                # self.arc_queue.pop(index)
                        for new_list in new_list_total:
                            # print(new_list)
                            self.arc_queue.append(new_list)  # 新弧入队列
                        self.state_stack.append(self.max)  # 起始节点入状态栈
                        self.max += 2
                        # self.index += 1  # 下标加一读取下一个字符
                    else:
                        print("error")
        # print("----------------")
        # 把状态栈顶元素出栈，该元素的弧的起始节点为整个NFA的起始节点，该弧的终止节点为整个NFA的终止节点。
        final_nfa = []
        state = self.state_stack.pop()
        for arc in self.arc_queue:
            if arc[0] == int(state):  # 获取以arc[0]为初始节点的最长的弧（最后一个就是最长的）
                # print(arc)
                final_nfa = arc

        # 优化最终弧， 因为经过上述操作得到的最终弧中可能会出现  [1,'a',3] 这种直接由状态1跳到状态3的弧
        # print(final_nfa)
        Max = final_nfa[len(final_nfa) - 1]
        Min = 0
        while Min < Max:
            if Min not in final_nfa:  # 没有该状态
                for index, value in enumerate(final_nfa):
                    if type(value) == int and value > Min:  # 所有大于该状态数的自减1
                        final_nfa[index] -= 1
                Max -= 1  # 同时最大值也减一，Max肯定大于Min
            else:
                Min += 1
        # print(final_nfa)

        # 以起始状态，接收符号，结束状态的形式存储最终弧
        index = 0
        result = []
        while index < len(final_nfa):
            value = final_nfa[index]
            if type(value) == int:
                if index + 1 < len(final_nfa) and type(final_nfa[index + 1]) == int:
                    index += 1
                elif index + 1 < len(final_nfa):
                    result.append([value, final_nfa[index + 1], final_nfa[index + 2]])
                    index += 2
                else:
                    index += 1
        # print(final_nfa)
        # 结果写入文件
        f = open("NFA.txt", "w")
        f.write(self.text)
        f.write("\n起始状态\t接收符号\t结束状态\n")
        f.close()
        start = final_nfa[0]  # 开始节点
        end = final_nfa[len(final_nfa) - 1]  # 结束节点
        for value in result:
            with open('NFA.txt', 'a') as f:
                f.write(str(value[0]) + "\t" + value[1] + "\t" + str(value[2]) + "\n")
        with open('NFA.txt', 'a') as f:
            f.write("初始节点:\t" + str(start) + "\n终结节点:\t" + str(end))
        with open('MFA.txt', 'a') as f:
            f.write("\n")
        # # 生成nfa的状态转换图
        nfa_graph(start, end, result)

        # 返回nfa
        return result

    # NFA 转换为 DFA
    def nfa_to_dfa(self, nfa):
        assistant_key = []
        # 在NFA上添加新的初始状态和新的终结状态
        nfa.insert(0, [-1, 'ε', nfa[0][0]])
        nfa.append([nfa[len(nfa) - 1][2], 'ε', -2])  # -1 表示新的初始节点，-2 表示新的结束节点

        """
            用字典实现状态转换表,{[-1,4,2]: [[第一种输入符后的closure集],[第二种],[第n种]]}
            {[-1,4,2] : 0} 则表示该[-1,4,2]这个closure集未被处理（标记）
            {[-1,4,2] : [[],[第二种]]} 表示该closure集面对第一种符号的输入的closure集为空
            修改：
            发现列表是可变类型，不能做字典的键，这里采用辅助列表来实现 assistant_key = [[x,1,2],[],[]], [x,1,2]的下标0就代替其为键
        """
        # 求得nfa 的输入符号集
        symbol_input = []
        for value in nfa:
            if value[1] != 'ε' and value[1] not in symbol_input:  # 第二条件避免重复录入
                symbol_input.append(value[1])

        final_states = []  # 记录终结状态集,  dfa的初始状态只有一个且在本算法中为状态号为0，所以无需记录
        # 求得初始节点的closure集
        closure = self.get_closure([-1], nfa)
        # 初始节点的closure集入表的首行首列
        assistant_key.append(closure)
        state_transform_table = {len(assistant_key) - 1: []}
        # 如果初始节点同时也为终结节点  将其加入终结状态集
        if -2 in closure:
            final_states.append(0)  # 整个nfa的初始节点为0

        """
            构造状态转换表
            因为字典在迭代过程不能改变大小，所以我定义了表2，在一次迭代中发生的改变体现在表2上，迭代中一次遍历完成后判断表2是否发生了改变，
            如果没发生变化，继续迭代，如果发生了改变，将表2复制给表1同时结束本次迭代，重新开始新的迭代
            而为了解决 state_transform_table = state_transform_table_2.copy() 语句使得迭代终止(经过测试发现)
            我在最外层添加了一个while循环来控制迭代的继续和终止
        """
        flag = True
        while flag:  # 状态转换表有改变了就继续构造,没改变就结束
            times = 0  # 一次迭代中循环进行的次数
            for key, value in state_transform_table.items():  # 遍历字典
                times += 1  # 每进行一次该循环就加一, 本次迭代完了后如果 time 和 键的个数不同就改变flag的值
                state_transform_table_2 = state_transform_table.copy()
                for symbol in symbol_input:
                    # 求得输入symbol符号后的move集
                    j_move = self.get_move(assistant_key[key], nfa, symbol)  # assistant_key[key] 就是该行首列的状态集
                    # 该move集对应的closure集
                    closure = self.get_closure(j_move, nfa)
                    # 给当前行添加内容
                    if closure not in state_transform_table_2[key] or len(closure) == 0:
                        state_transform_table_2[key].append(closure)  # [[],[]] 形式要为列表套列表
                    # 如果该表的首列中没有该状态集就将该状态加入首列 且该状态集不能为空集
                    if len(closure) > 0 and closure not in assistant_key:
                        assistant_key.append(closure)
                        state_transform_table_2[len(assistant_key) - 1] = []
                        if -2 in closure:
                            final_states.append(len(assistant_key) - 1)  # 以编号的形式加入终结状态集

                # 判断表2是否发生了改变
                flag2 = 0
                for k, v in state_transform_table_2.items():
                    if k not in state_transform_table.keys():
                        flag2 = 1
                        break
                    elif v != state_transform_table[k]:  # 列表可以用！=直接判断是否相等
                        flag2 = 1
                        break
                if flag2 == 1:
                    state_transform_table = state_transform_table_2.copy()
                    break
            if times == len(state_transform_table.keys()):
                flag = False

        # 根据状态转换表构造dfa
        dfa = []
        for key, value in state_transform_table.items():
            for index, state in enumerate(value):
                if len(state) > 0:  # 输入α弧到的状态不为空 即该状态输入α弧指向其他状态
                    new_arc = [key, symbol_input[index]]  # symbol_input 和 字典中的键 是一一对应的
                    for key2, value2 in state_transform_table.items():
                        if state == assistant_key[key2]:  # 找到初始状态输入α弧到的结束状态,加入其编号
                            new_arc.append(key2)
                            break
                    dfa.append(new_arc)


        # 结果写入文件
        f = open("DFA.txt", "w")
        f.write(self.text)
        f.write("\n起始状态\t接收符号\t结束状态\n")
        f.close()
        for value in dfa:
            with open('DFA.txt', 'a') as f:
                f.write(str(value[0]) + "\t" + value[1] + "\t" + str(value[2]) + "\n")
        with open('DFA.txt', 'a') as f:
            f.write("初始节点:\t0\n终结节点:\t")
        for value in final_states:
            with open('DFA.txt', 'a') as f:
                f.write(str(value) + "\t")
        with open('MFA.txt', 'a') as f:
            f.write("\n")
        # 生成nfa的状态转换图
        filename = './Reg_Graph/DFA'
        dfa_graph = Digraph(filename, 'DFA_graph', None, None, 'png', None, "UTF-8")
        dfa_graph.attr(rankdir="LR")  # 图从左到右 L -> R
        for value in dfa:
            # 出发节点
            if value[0] == 0:  # 初始节点
                if value[0] in final_states:  # 又是终结节点
                    dfa_graph.node(str(value[0]), str(value[0]), fillcolor="red", style="filled", shape="doublecircle")
                else:
                    dfa_graph.node(str(value[0]), str(value[0]), fillcolor="red", style="filled")
            elif value[0] in final_states:  # 只是终结节点
                dfa_graph.node(str(value[0]), str(value[0]), shape="doublecircle")
            else:  # 非初始也非终结
                dfa_graph.node(str(value[0]), str(value[0]))
            # 到达节点, 到达节点不可能是初始节点
            if value[2] in final_states:  # 为终结节点
                dfa_graph.node(str(value[2]), str(value[2]), shape="doublecircle")
            else:
                dfa_graph.node(str(value[2]), str(value[2]))
            # 加边
            dfa_graph.edge(str(value[0]), str(value[2]), label=value[1])
        dfa_graph.render()

        # 返回dfa和终态集
        return dfa, final_states, symbol_input

    # 求得给定状态集合的move集即α弧转换(这里用symbol表示输入符号即α)
    def get_move(self, state_list, nfa, symbol):
        """
            状态集合I的a弧转换，Ia = ε-closure(J) ,其中J=move(I,a)，即所有可从I中的某一状态经过一条a弧而到达的状态的全体。
        """
        # state_list 为状态集 , 形式为 [1,3,4]
        move = []
        for state in state_list:  # 遍历转态集找状态
            for arc in nfa:  # 遍历nfa
                if arc[0] == state and arc[1] == symbol:  # 起始节点相同且输入符号也相同
                    move.append(arc[2])  # 结束节点入列表
        return move

    # 求得给定move集合的 closure 集即空弧转换（可传递的）
    def get_closure(self, move, nfa):
        """
            状态集合I的ε-闭包ε-closure(I)，是一状态集
            任何状态q ∈ I，则q ∈ ε-closure(I)；
            任何状态q ∈ I，则q经任意条 ε 弧而能到达的状态q′ ∈ ε-closure(I) 。
        """
        closure = []
        for state in move:
            if state not in closure:
                closure.append(state)  # 首先当前状态入队列
            for arc in nfa:
                if arc[0] == state and arc[1] == 'ε' and arc[2] not in move:  # 找到一条空弧转换
                    move.append(arc[2])  # 添加进状态表
        return closure

    # dfa的最小化
    def dfa_to_mfa(self, dfa, final_states, input_symbols):
        """
            主要思路: 以 ab*|b 举例，由dfa和 final_state得到初始的mfa为 [[0],[1,2,3]] 这里[0]是非终态集,[1,2,3]是终态集
            对maf进行循环处理：
                从列表mfa中得到一个等价状态集:
                    从所有输入符号中得到一个输入符号:
                        该等价状态集被分割就用新的结果等价状态将其替换  同时跳出本层循环
            而因为在遍历mfa的同时还对mfa进行了修改 需要重新遍历， 所以这里和nfa转dfa一样在最外层设置了一个while循环
        """
        # 列表形式存储mfa
        mfa = []
        # 通过nfa和终结状态集得到非终结状态集
        not_final_state = []
        for arc in dfa:
            if arc[0] not in final_states and arc[0] not in not_final_state:
                not_final_state.append(arc[0])
            if arc[2] not in final_states and arc[2] not in not_final_state:
                not_final_state.append(arc[2])
        mfa.append(not_final_state)
        mfa.append(final_states)
        # print("=================")
        # print(mfa)
        # print("=================")
        flag = True
        while flag:
            for index, states in enumerate(mfa):  # 得到等价状态集
                flag1 = 1  # 判断此次循环是否正常结束即没有被分割 , 正常结束就退出while循环
                for symbol in input_symbols:  # 得到一个输入符号
                    """
                        ab*|b 举例 得到初始mfa = [[0],[1,2,3]]
                        定义该状态经过输入符号到达的新状态集的汇总, 下标i表示第i+1个状态
                        如states = [1,2,3], symbol = b 时得到的 new_states_total = [[],[3],[3]]
                        说明状态1不接受输入符号b, 状态2和3接收b后到达同一状态3, 所以该等价状态集变成[[1],[2,3]]
                    """
                    new_states_total = []
                    for state in states:  # 从等价状态集中得到一个状态
                        new_states = []  # 定义该状态经过输入符号到达的新状态集
                        for arc in dfa:  # 遍历dfa 找到该状态经过输入符号到达的新状态
                            if arc[0] == state and arc[1] == symbol:
                                new_states.append(arc[2])
                                # new_states_total.append(arc[2])
                        new_states_total.append(new_states)
                    # print(mfa)
                    # print(states)
                    # print(new_states_total)
                    new_states_total2 = []  # 新的等价状态集来替换最外层的states
                    # 如果该等价状态集被分割了就找到分割后的等价状态集,用新的替换旧的, 通过双层遍历来实现
                    for index1, state1 in enumerate(states):
                        new_states = [state1]
                        for index2, state2 in enumerate(states):
                            if index2 == index1:  # 自己不与自己比较,小于避免重复比较
                                continue
                            elif len(new_states_total[index1]) > 0 and len(new_states_total[index2]) > 0:
                                for states3 in mfa:     # 二者输入符号α到达的状态集相同
                                    if new_states_total[index1][0] in states3 and new_states_total[index2][0] in states3:
                                        new_states.append(state2)
                                        break
                            elif len(new_states_total[index1]) == 0 and len(new_states_total[index2]) == 0:
                                new_states.append(state2)

                        new_states.sort()  # 对其按编号由小到大进行排序，方便后面判断是否为重复元素
                        if new_states not in new_states_total2:
                            new_states_total2.append(new_states)
                    # print(symbol)
                    # print(new_states_total2)
                    # print("========================")
                    # 被分割了就对其进行替换同时跳出输入符号这个循环, 前面算法保证了如果未被分割则二者相等
                    if len(new_states_total2) > 0 and new_states_total2[0] != states:
                        mfa.pop(index)  # 删除该等价状态集然后添加分割后的
                        for states2 in new_states_total2:
                            mfa.append(states2)
                        flag1 = 0
                        break
                if flag1 == 0:  # 遍历不正常结束，即由进行了一次分割
                    break
            if flag1 == 1:  # 遍历正常结束
                flag = False

        # 结合dfa对mfa进行优化 将其变成 [初始状态,输入符号,结束状态]的形式
        # 主要思想 如mfa = [[0,1],[2],[3,4]] 则将dfa中的所有0,1变成 0。 3,4变成3(第一个状态) 最后使编号从0递增处理一下即可
        final_mfa = []
        mfa.sort()
        for arc in dfa:
            new_arc = []
            for state in mfa:
                if arc[0] in state:  # 该状态集包含当前的 初始状态，算法保证了是一定存在的
                    new_arc.append(state[0])  # 以该状态集的第一个状态为起始状态
                    break
            new_arc.append(arc[1])  # 输入符号
            for state in mfa:
                if arc[2] in state:  # 该状态集包含当前的 初始状态，算法保证了是一定存在的
                    new_arc.append(state[0])  # 以该状态集的第一个状态为起始状态
                    break
            if new_arc not in final_mfa:  # 去除重复的
                final_mfa.append(new_arc)


        # 优化mfa编号 如将[2,'0',2,2,'1',2] 变成 [0,'0',0,0,'1',0] 即编号从小到大
        Max = 0
        for arc in final_mfa:
            if arc[0] > Max:
                Max = arc[0]
            if arc[2] > Max:
                Max = arc[2]
        Min = 0
        while Min < Max:
            flag = 0
            for arc in final_mfa:
                if arc[0] == Min or arc[2] == Min:
                    flag = 1
                    break
            if flag == 0:       # 说明mfa中没有 编号为Min的状态, 这时候将所有大于Min的状态编号减一
                for index, value in enumerate(final_mfa):
                    if value[0] > Min:
                        final_mfa[index][0] -= 1
                    if value[2] > Min:
                        final_mfa[index][2] -= 1
                    # 同时终结状态集中大于 Min的状态编号也要减一
                    for index2, value2 in enumerate(final_states):
                        if value2 > Min:
                            if final_states[index2] - 1 in final_states:
                                final_states.pop(index2)
                            else:
                                final_states[index2] -= 1
                Max -= 1    # 同时最大值减一
            else:
                Min += 1


        # 结果写入文件
        f = open("MFA.txt", "w")
        f.write(self.text)
        f.write("\n起始状态\t接收符号\t结束状态\n")
        f.close()
        for value in final_mfa:
            with open('MFA.txt', 'a') as f:
                f.write(str(value[0]) + "\t" + value[1] + "\t" + str(value[2]) + "\n")
        with open('MFA.txt', 'a') as f:
            f.write("初始节点:\t0\n终结节点:\t")
        for value in final_states:
            with open('MFA.txt', 'a') as f:
                f.write(str(value) + "\t")
        with open('MFA.txt', 'a') as f:
            f.write("\n")
        # 生成nfa的状态转换图
        filename = './Reg_Graph/MFA'
        mfa_graph = Digraph(filename, 'MFA_graph', None, None, 'png', None, "UTF-8")
        mfa_graph.attr(rankdir="LR")  # 图从左到右 L -> R
        for value in final_mfa:
            # 出发节点
            if value[0] == 0:  # 初始节点
                if value[0] in final_states:  # 又是终结节点
                    mfa_graph.node(str(value[0]), str(value[0]), fillcolor="red", style="filled",
                                   shape="doublecircle")
                else:
                    mfa_graph.node(str(value[0]), str(value[0]), fillcolor="red", style="filled")
            elif value[0] in final_states:  # 只是终结节点
                mfa_graph.node(str(value[0]), str(value[0]), shape="doublecircle")
            else:  # 非初始也非终结
                mfa_graph.node(str(value[0]), str(value[0]))
            # 到达节点, 到达节点不可能是初始节点
            if value[2] in final_states:  # 为终结节点
                mfa_graph.node(str(value[2]), str(value[2]), shape="doublecircle")
            else:
                mfa_graph.node(str(value[2]), str(value[2]))
            # 加边
            mfa_graph.edge(str(value[0]), str(value[2]), label=value[1])
        mfa_graph.render()

        # 修改终结状态集 如[7,8]合并成了[7] 就需要将8删掉
        for index, final_state in enumerate(final_states):
            flag = 0  # 0表示该终结状态需要被删掉
            for arc in final_mfa:
                if final_state == arc[2]:
                    flag = 1  # 有出现该终结状态
                    break
            if flag == 0:
                final_states.pop(index)

        # 返回mfa和终结状态集
        return final_mfa, final_states






if __name__ == '__main__':
    texts = str(open('keshe.txt').read())  # 从文件中读入数据并强转为字符串类型
    test = NfaDfaMfa(texts)
    nfa = test.reg_to_nfa()  # final_nfa 得到的nfa
    dfa, final_states, input_symbols = test.nfa_to_dfa(nfa)  # dfa,终态集和输入符号集
    dfa1 = [[0, 'a', 1], [0, 'b', 2], [1, 'a', 3], [1, 'b', 2], [2, 'a', 1], [2, 'b', 4], [3, 'a', 3], [3, 'b', 5],
           [4, 'a', 6], [4, 'b', 4], [5, 'a', 6], [5, 'b', 4], [6, 'a', 3], [6, 'b', 5]]
    final_state = [3, 4, 5, 6]
    input_symbols1 = ['a', 'b']
    mfa, final_states1 = test.dfa_to_mfa(dfa1, final_state, input_symbols1)
    print(mfa)
    print(final_states1)
    # texts = str(open('keshe.txt').read())  # 从文件中读入数据并强转为字符串类型
    # text = texts.split("\n")
    # print(text)
    # if len(text) > 1:  # 多个正规式
    #     # 方法1 自己把每行的正规式套上一个（）合并成一个正规式
    #     texts = ""
    #     for index, value in enumerate(text):
    #         print(value)
    #         if index < len(text) - 1:
    #             texts += "(" + value + ")|"
    #         else:
    #             texts += "(" + value + ")"
    #     test = NfaDfaMfa(texts)
    #     nfa = test.reg_to_nfa()  # final_nfa 得到的nfa
    #     dfa, final_states, input_symbols = test.nfa_to_dfa(nfa)  # dfa,终态集和输入符号集
    #     mfa, final_states = test.dfa_to_mfa(dfa, final_states, input_symbols)
    #     print("多个正规式")
    #
    #     # 方法2 合并每个正规式的nfa
    #     # nfas = []
    #     # for reg in text:
    #     #     test = NfaDfaMfa(reg)
    #     #     nfas.append(test.reg_to_nfa())
    #     # final_nfa = nfa_associate(nfas)
    #     #
    #     # first = final_nfa[0][0]
    #     # last = final_nfa[len(final_nfa) - 1][2]
    #     # nfa_graph(first, last, final_nfa)
    #     # test = NfaDfaMfa("")  # 只是为了实例化对象
    #     # dfa, final_states, input_symbols = test.nfa_to_dfa(final_nfa)  # dfa,终态集和输入符号集
    #     # mfa, final_states = test.dfa_to_mfa(dfa, final_states, input_symbols)
    # else:
    #     print("一个正规式")
    #     test = NfaDfaMfa(texts)
    #     nfa = test.reg_to_nfa()  # final_nfa 得到的nfa
    #     dfa, final_states, input_symbols = test.nfa_to_dfa(nfa)  # dfa,终态集和输入符号集
    #     mfa, final_states = test.dfa_to_mfa(dfa, final_states, input_symbols)

#   code = "case\naut"
#   test.Lexical_Analysis(mfa, code, final_states)
