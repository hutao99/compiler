import re

import Analyzer


class ASTNode:
    def __init__(self, Type, content=None):
        self.type = Type
        self.text = content
        self.child_node = list()

    def __str__(self):
        child_nodes = list()
        for child in self.child_node:
            child_nodes.append(child.__str__())
        out = "<{type}, {text}>".format(type=self.type, text=self.text)
        for child in child_nodes:
            if child:
                for item in child.split("\n"):
                    out = out + "\n     " + item

        return out

    def __repr__(self):
        return self.__str__()


class Predictive_Analysis:
    def __init__(self):
        self.follow_dict = None
        self.first = dict()
        self.last = dict()
        self.Formula = dict()
        self.productions = {}
        self.begin = ''
        self.predict_table = dict()
        self.predict_table_ = dict()
        self.vn = []
        self.vt = []
        self.grammars = dict()
        self.flag = 0
        self.first_dict = dict()
        self.nonterminals = []  # 非终结符
        self.kong = []

    def input(self, data):
        # 种别码
        carve = list(filter(None, data.split('\n')))
        index = carve[0].find(':')
        begin = carve[0][0:index]
        self.begin = begin
        print('-----------------')
        print(self.begin)
        for i in carve:
            index = i.find(':')
            self.Formula[i[0:index]] = i[index + 1:]
            self.first[i[0:index]] = []
            self.last[i[0:index]] = []
        self.last[begin].append('#')
        self.get_vn_vt(data)
        # self.First_()
        self.compute_first(self.productions)
        print('first', self.first)
        self.FIRST()
        print('first_dict', self.first_dict)
        # self.first=self.first_dict
        # self.FOLLOW()
        for i in self.first:
            if '$' in self.first[i]:
               self.kong.append(i)
        print('kong', self.kong)
        self.Last_()
        self.get_predict_table_(data)
        print("\n预测分析表\n")
        for i in self.predict_table_:
            print(i, self.predict_table_[i])
        self.get_predict_table(data)

        print(self.predict_table)

    def get_vn_vt(self, data):
        grammar_list = {}
        for line in re.split('\n', data):
            if ':' in line:
                if line.split(':')[0] not in self.vn:
                    self.vn.append(line.split(':')[0])
                for i in line.split(':')[1].split('|'):
                    if grammar_list.get(line.split(':')[0]) is None:
                        grammar_list[line.split(':')[0]] = []
                        grammar_list[line.split(':')[0]].append(i.strip(' '))
                    else:
                        grammar_list[line.split(':')[0]].append(i.strip(' '))

        for production in data.split('\n'):
            left, right = production.split(':')
            left = left.strip()
            # 按照空格分割右部符号
            symbols_list = right.split('|')

            # 将左部和右部添加到字典中
            if left not in self.productions:
                self.productions[left] = []
                self.nonterminals.append(left)
            for symbols in symbols_list:
                self.productions[left].append(symbols.split())
        self.nonterminals=list(set(self.nonterminals))
        self.grammars = grammar_list
        for i in self.grammars:
            print(i, self.grammars[i])
        for i in self.vn:
            for j in self.grammars[i]:
                data = j.split(" ")
                for temp in data:
                    if temp not in self.vt and temp not in self.vn and temp != '$':
                        self.vt.append(temp)
        self.vt.append('#')
        self.vt = list(set(self.vt))
        self.vn = list(set(self.vn))
        print('\n\n--------- 文法的非终结符为 ----------\n', self.vn,
              '\n\n--------- 文法的终结符为 ----------\n', self.vt)
        print(self.productions)

    def compute_first(self, productions):
        print(len(self.vn))
        # 初始化非终结符号的FIRST集
        for nonterminal in self.nonterminals:
            print(nonterminal)
            self.first[nonterminal] = set()

        # 重复处理直到FIRST集不再发生变化
        while True:
            changed = False

            # 处理每个产生式
            for left, rights in productions.items():
                for right in rights:
                    i = 0
                    # 处理产生式右部的每个符号
                    while i < len(right):
                        symbol = right[i]

                        # 如果是终结符号，则将其加入FIRST集
                        if symbol not in self.nonterminals:
                            if symbol not in self.first[left]:
                                self.first[left].add(symbol)
                                changed = True
                            break

                        # 如果是非终结符号，则将其FIRST集合并到左部符号的FIRST集中
                        elif symbol in self.nonterminals:
                            for s in self.first[symbol]:
                                if s != '$' and s not in self.first[left]:
                                    self.first[left].add(s)
                                    changed = True

                            # 如果该非终结符号不能推导出空串，则退出循环
                            if '$' not in self.first[symbol]:
                                break

                            # 否则，继续处理下一个符号
                            i += 1

                    # 如果产生式右部的所有符号都能推导出空串，则将空串加入左部符号的FIRST集中
                    else:
                        if '$' not in self.first[left]:
                            self.first[left].add('$')
                            changed = True

            # 如果FIRST集不再发生变化，则退出循环
            if not changed:
                break

    def compute_first_set(self, symbols):
        first_set = set()
        i = 0
        while i < len(symbols):
            symbol = symbols[i]
            if symbol not in self.nonterminals:
                first_set.add(symbol)
                break
            elif symbol in self.nonterminals:
                first_i = self.first[symbol] - {'$'}
                first_set |= first_i
                if '$' not in self.first[symbol]:
                    break
            else:
                raise ValueError(f"Invalid symbol: {symbol}")
            i += 1
        else:
            first_set.add('$')
        return first_set

    def FIRST(self):
        # 计算每个候选式的FIRST集
        for nonter, production in self.productions.items():
            self.first_dict[nonter] = []
            for rhs in production:
                first_set = self.compute_first_set(rhs)
                for i in list(first_set):
                    self.first_dict[nonter].append(i)

    def Last_(self):
        self.last[self.begin] = ["#"]
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
                    for k in range(length):
                        # 如果是非终结符
                        if word[k] in self.Formula:
                            if k + 1 < length:
                                # 非终结符的下一个也是非终结符，把下一个的first集合加入当前非终结符的last
                                if word[k + 1] in self.Formula:
                                    for n in self.first[word[k + 1]]:
                                        # 为空把后面一个的再后面一个first集合加入当前last
                                        if n == '$' and k + 2 < length:
                                            # 是非终结符
                                            if word[k + 2] in self.Formula:
                                                for e in self.first_dict[word[k + 2]]:
                                                    if e != '$' and e not in self.last[word[k]]:
                                                        flag = True
                                                        self.last[word[k]].append(e)
                                            # 不是非终结符
                                            elif word[k + 2] not in self.last[word[k]]:
                                                flag = True
                                                self.last[word[k]].append(word[k + 2])

                                        # 把没有的符号加入last中
                                        elif n not in self.last[word[k]] and n != '$':
                                            # 说明集合变化了，需要再循环一次
                                            flag = True
                                            self.last[word[k]].append(n)
                                        # 最后一个字符为非终结符且其中含有空字符
                                        if n == '$' and k + 1 == length - 1:
                                            for y in self.last[i]:
                                                if y not in self.last[word[k]]:
                                                    flag = True
                                                    self.last[word[k]].append(y)
                                elif word[k + 1] not in self.last[word[k]]:
                                    self.last[word[k]].append(word[k + 1])
                    # 是非终结符且是最后一个符号
                    if word[length - 1] in self.Formula:
                        for y in self.last[i]:
                            if y not in self.last[word[length - 1]]:
                                flag = True
                                self.last[word[length - 1]].append(y)

    def get_predict_table(self, data):
        for item in self.grammars:
            self.predict_table[item] = {}
            for next_t in self.grammars[item]:
                next_value = next_t.split()[0]
                if next_value in self.grammars:
                    out = self.first_dict[next_value]
                    for i in out:
                        if i != '$':
                            self.predict_table[item][i] = next_t
                else:
                    self.predict_table[item][next_value] = next_t
        for k in self.grammars:
            for next_grammar in self.grammars[k]:
                next_k = next_grammar.split()[0]

                if next_k in self.grammars and "$" in self.first_dict[next_k] or next_k == "$":
                    for fk in self.last[k]:
                        self.predict_table[k][fk] = next_grammar

    def get_predict_table_(self, data):
        for item in self.grammars:
            self.predict_table_[item] = {}
            for next_t in self.grammars[item]:
                next_value = next_t.split()[0]
                if next_value in self.grammars:
                    out = self.first_dict[next_value]
                    for i in out:
                        if i != '$':

                            self.predict_table_[item][i] = item + '->' + next_t
                else:
                    if(next_value=='{'):
                        print('---------------------------12222222222222222222')
                        print(item + '->' + next_t)
                    self.predict_table_[item][next_value] = item + '->' + next_t
                    print(self.predict_table_[item])
        for k in self.grammars:
            for next_grammar in self.grammars[k]:
                next_k = next_grammar.split()[0]
                if next_k in self.grammars and "$" in self.first_dict[next_k] or next_k == "$":
                    for fk in self.last[k]:
                        self.predict_table_[k][fk] = k + '->' + next_grammar


# coding=utf-8
def check_charset(file_path):
    import chardet
    with open(file_path, "rb") as f:
        data = f.read(1000)
        charset = chardet.detect(data)['encoding']
    return charset


if __name__ == "__main__":
    test = Predictive_Analysis()
    path = "全部测试程序\\11LL(1)测试用例\文法.TXT"
    grammar = str(open(path).read())
    grammar = grammar.replace('->', ':')
    test.input(grammar)
    con = 'i+i*i'
    # con+='#'
    # con = ""
    # Filepath = "D:\pythonProject\compiler\全部测试程序\\02已测试正确的编译器用例\\test2.2.txt"
    # for line in open(Filepath, 'r', encoding=check_charset(Filepath)):
    #     con += line
    lex = Analyzer.AnalyzerLex()
    lex.input(con)
    expression = []

    while True:
        tok = lex.token()
        if not tok:
            break
        s1 = ['operator', 'keyword', 'Boundary']
        s2 = ['integer', 'character', 'string', 'identifier', 'float']
        if tok.type in s1:
            expression.append([tok.value, tok.value])
        elif tok.type in s2:
            expression.append([tok.type, tok.value])
    expression.append(['#', '#'])
    print(expression)
    print(test.first_dict)
    print(test.last)
    print(test.predict_table_['A1'])
