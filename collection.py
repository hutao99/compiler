class FirstAndFollow:
    def __init__(self):
        self.first = dict()
        self.last = dict()
        # 非终结符和产生式
        self.Formula = dict()
        self.begin = ''

    def input(self, data):
        # 处理文法
        carve = list(filter(None, data.split('\n')))
        carve = [k for k in carve if ':' in k]
        index = carve[0].find(':')
        begin = carve[0][0:index]
        self.begin = begin.replace(" ", "")
        for i in carve:
            index = i.find(':')
            if i[0:index].replace(" ", "") not in self.Formula:
                self.Formula[i[0:index].replace(" ", "")] = i[index+1:]
                self.first[i[0:index].replace(" ", "")] = []
                self.last[i[0:index].replace(" ", "")] = []
            else:
                self.Formula[i[0:index].replace(" ", "")] = self.Formula[i[0:index].replace(" ", "")] + '|' + i[index + 1:]
        self.last[self.begin].append('#')
        self.First_()
        self.Last_()

    def First_(self):
        # 第一次先求出能一次找到的First集合
        for i in self.Formula:
            production = self.Formula[i]
            for j in production.split('|'):
                word = [k for k in j.split(' ') if k != '']
                if word[0] not in self.Formula:
                    self.first[i].append(word[0])
        flag = True
        while flag:
            flag = False
            for i in self.Formula:
                production = self.Formula[i]
                for j in production.split('|'):
                    word = [k for k in j.split(' ') if k != '']
                    for n in word:
                        # 是非终结符
                        if n in self.Formula:
                            for m in self.first[n]:
                                if m not in self.first[i]:
                                    flag = True
                                    self.first[i].append(m)
                        else:
                            # 是终结符就跳出
                            break
                        # 没有空字符就不用处理后面的非终结符
                        if 'ε' not in self.first[n]:
                            break

    def Last_(self):
        flag = True
        # 在lastvt集合变化时执行
        while flag:
            flag = False
            for i in self.Formula:
                production = self.Formula[i]
                # 对产生式分割
                for j in list(filter(None, production.split('|'))):
                    # 去除元素为空的字符
                    word = list(filter(None, j.split(' ')))
                    length = len(word)
                    for k in range(length):
                        # 如果是非终结符
                        if word[k] in self.Formula:
                            if k+1 < length:
                                # 非终结符的下一个也是非终结符，把下一个的first集合加入当前非终结符的last
                                if word[k+1] in self.Formula:
                                    for n in self.first[word[k+1]]:
                                        # 为空把后面一个的再后面一个first集合加入当前last
                                        if n == 'ε' and k+2 < length:
                                            # 是非终结符
                                            if word[k+2] in self.Formula:
                                                for e in self.first[word[k+2]]:
                                                    if e != 'ε' and e not in self.last[word[k]]:
                                                        flag = True
                                                        self.last[word[k]].append(e)
                                            # 不是非终结符
                                            elif word[k+2] not in self.last[word[k]]:
                                                flag = True
                                                self.last[word[k]].append(word[k+2])

                                        # 把没有的符号加入last中
                                        elif n not in self.last[word[k]] and n != 'ε':
                                            # 说明集合变化了，需要再循环一次
                                            flag = True
                                            self.last[word[k]].append(n)
                                        # 最后一个字符为非终结符且其中含有空字符
                                        if n == 'ε' and k + 1 == length-1:
                                            for y in self.last[i]:
                                                if y not in self.last[word[k]]:
                                                    flag = True
                                                    self.last[word[k]].append(y)
                                elif word[k+1] not in self.last[word[k]]:
                                    self.last[word[k]].append(word[k+1])
                    # 是非终结符且是最后一个符号
                    if word[length - 1] in self.Formula:
                        for y in self.last[i]:
                            if y not in self.last[word[length - 1]]:
                                flag = True
                                self.last[word[length - 1]].append(y)


class FirstVTAndLastVT:
    def __init__(self):
        self.first = dict()
        self.last = dict()
        # 非终结符和产生式
        self.Formula = dict()
        self.begin = ''
        self.All_symbols = []

    def input(self, data):
        carve = list(filter(None, data.split('\n')))
        carve = [k for k in carve if ':' in k]
        index = carve[0].find(':')
        begin = carve[0][0:index]
        self.begin = begin.replace(" ", "")
        self.Formula[self.begin+"'"] = '# ' + self.begin + ' #'
        self.first[self.begin + "'"] = []
        self.last[self.begin + "'"] = []
        # 处理文法
        for i in list(filter(None, data.split('\n'))):
            index = i.find(':')
            if i[0:index].replace(" ", "") not in self.Formula:
                self.Formula[i[0:index].replace(" ", "")] = i[index+1:]
                self.first[i[0:index].replace(" ", "")] = []
                self.last[i[0:index].replace(" ", "")] = []
            else:
                self.Formula[i[0:index].replace(" ", "")] = self.Formula[i[0:index].replace(" ", "")] + '|' + i[index + 1:]
        self.FirstVT()
        self.LastVT()

    def FirstVT(self):
        flag = True
        while flag:
            flag = False
            for i in self.Formula:
                production = self.Formula[i]
                # 对产生式分割
                for j in list(filter(None, production.split('|'))):
                    # 去除元素为空的字符
                    word = list(filter(None, j.split(' ')))
                    # P->a...
                    if word[0] not in self.Formula:
                        if word[0] not in self.first[i]:
                            flag = True
                            self.first[i].append(word[0])
                    # P->Ra...
                    elif word[0] in self.Formula:
                        for k in self.first[word[0]]:
                            if k not in self.first[i]:
                                flag = True
                                self.first[i].append(k)
                        # P->Ra...
                        if len(word) >= 2 and word[1] not in self.Formula and word[1] not in self.first[i]:
                            flag = True
                            self.first[i].append(word[1])

    def LastVT(self):
        flag = True
        while flag:
            flag = False
            for i in self.Formula:
                production = self.Formula[i]
                # 对产生式分割
                for j in list(filter(None, production.split('|'))):
                    # 去除元素为空的字符
                    word = list(filter(None, j.split(' ')))
                    length = len(word)
                    # P->...a
                    if word[length - 1] not in self.Formula:
                        if word[length - 1] not in self.last[i]:
                            flag = True
                            self.last[i].append(word[length - 1])
                    # P->...Q
                    elif word[length - 1] in self.Formula:
                        for k in self.last[word[length - 1]]:
                            if k not in self.last[i]:
                                flag = True
                                self.last[i].append(k)
                        # P->...aQ
                        if len(word) >= 2 and word[length - 2] not in self.Formula and word[length - 2] not in self.last[i]:
                            flag = True
                            self.last[i].append(word[length - 2])

    # 优先表
    def Table(self):
        is_opg = True
        sequence = dict()
        # 去重
        operator = set()
        for i in self.Formula:
            production = self.Formula[i]
            # 对产生式分割
            for j in list(filter(None, production.split('|'))):
                # 去除元素为空的字符
                word = list(filter(None, j.split(' ')))
                for k in word:
                    if k not in self.Formula:
                        operator.add(k)
        print(operator)
        # 为每个符号构建下标
        p = 0
        for i in list(operator):
            sequence[i] = p
            p += 1
        length = len(operator)
        precedence_table = [['' for j in range(length)] for i in range(length)]
        print(sequence)
        for i in self.Formula:
            production = self.Formula[i]
            # 对产生式分割
            for j in list(filter(None, production.split('|'))):
                word = list(filter(None, j.split(' ')))
                l = len(word)
                for k in range(l):
                    # P->...ab...
                    if k + 1 < l and word[k] not in self.Formula and word[k+1] not in self.Formula:
                        if precedence_table[sequence[word[k]]][sequence[word[k+1]]] == '':
                            precedence_table[sequence[word[k]]][sequence[word[k+1]]] = '='
                        else:
                            is_opg = False
                    # P->...aB...
                    if k + 1 < l and word[k] not in self.Formula and word[k+1] in self.Formula:
                        for m in self.first[word[k+1]]:
                            if precedence_table[sequence[word[k]]][sequence[m]] == '':
                                precedence_table[sequence[word[k]]][sequence[m]] = '<'#
                            else:
                                is_opg = False
                    # P->...Ab...
                    if k + 1 < l and word[k] in self.Formula and word[k+1] not in self.Formula:
                        for m in self.last[word[k]]:
                            if precedence_table[sequence[m]][sequence[word[k+1]]] == '':
                                precedence_table[sequence[m]][sequence[word[k+1]]] = '>'#
                            else:
                                is_opg = False
                    # P->...aQb...
                    if k + 2 < l and word[k] not in self.Formula and word[k+1] in self.Formula and word[k+2] not in self.Formula:
                        if precedence_table[sequence[word[k]]][sequence[word[k + 2]]] == '':
                            precedence_table[sequence[word[k]]][sequence[word[k + 2]]] = '='
                        else:
                            is_opg = False
        return sequence, precedence_table, is_opg

    def is_in_Formula(self, lmp):
        for i in self.Formula:
            production = self.Formula[i]
            for j in list(filter(None, production.split('|'))):
                # 去除元素为空的字符
                word = list(filter(None, j.split(' ')))
                if len(lmp) != len(word):
                    continue
                else:
                    flag = True
                    for k in range(len(lmp)):
                        if lmp[k] in self.Formula and word[k] in self.Formula:  # 非终结符匹配
                            continue
                        elif lmp[k] == word[k]:  # 非终结符匹配
                            continue
                        else:  # 不匹配
                            flag = False
                            break
                    if flag:
                        return True
        return False

    # 算符优先分析
    def OP(self, sequence, precedence_table, expression):
        info = ""
        stack = [expression[0]]
        symbol = [expression[0]]
        index = 1
        stack_total = []
        action = []
        remainder = []
        priority = []
        while index < len(expression):
            stack_total.append(stack.copy())
            remainder.append(expression[index:].copy())
            i = expression[index]
            sign = symbol[-1]
            if sign == '#' and sign == i:
                print("接受表达式")
                info = "接受表达式"
                break
            elif precedence_table[sequence[sign]][sequence[i]] == '<' or precedence_table[sequence[sign]][sequence[i]] == '=':
                priority.append(precedence_table[sequence[sign]][sequence[i]])
                action.append('移进')
                stack.append(i)
                symbol.append(i)
                index += 1
            # 规约
            elif precedence_table[sequence[sign]][sequence[i]] == '>':
                priority.append('>')
                action.append('归约')
                length = len(stack)
                flag = True
                lmp = []
                # 求最左素短语
                idx = 0
                for j in range(length - 1, -1, -1):
                    if stack[j] == sign:
                        idx = j
                        break
                symbol_previous = stack[idx]
                for j in range(idx - 1, -1, -1):
                    if stack[j] not in self.Formula and precedence_table[sequence[stack[j]]][sequence[symbol_previous]] == '<':
                        lmp = stack[j+1:]
                        break
                    if stack[j] not in self.Formula:
                        symbol_previous = stack[j]
                # 检查最左素短语是否在产生式的右部
                if self.is_in_Formula(lmp):
                    flag = False
                    for k in range(len(lmp)):
                        stack.pop()
                        if lmp[k] not in self.Formula:
                            symbol.pop()
                stack.append(self.begin)
                # 规约不了，报错
                if flag:
                    print("没有产生式可以归约")
                    info = "没有产生式可以归约"
                    break
            else:
                # 没有优先级关系报错
                print("栈顶符号与输入符号无优先关系，分析失败")
                info = "栈顶符号与输入符号无优先关系，分析失败"
                break
        return stack_total, info, action, remainder, priority


'''pp = FirstVTAndLastVT()
pp.input('S: ( R ) | a | â ˆ §\nR: T\nT: S , T | S')
print(pp.first)
print(pp.last)
pp.Table()'''
