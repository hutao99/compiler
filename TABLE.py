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
        self.first = dict()
        self.last = dict()
        self.Formula = dict()
        self.begin = ''
        self.predict_table = dict()
        self.predict_table_ = dict()
        self.vn = []
        self.vt = []
        self.grammars = dict()
        self.flag = 0

    def input(self, data):
        # 种别码
        carve = list(filter(None, data.split('\n')))
        index = carve[0].find(':')
        begin = carve[0][0:index]
        self.begin = begin
        for i in carve:
            index = i.find(':')
            self.Formula[i[0:index]] = i[index + 1:]
            self.first[i[0:index]] = []
            self.last[i[0:index]] = []
        self.last[begin].append('#')
        self.get_vn_vt(data)
        self.First_()
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

    def First_(self):
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
                        if n in self.Formula:
                            for m in self.first[n]:
                                if m not in self.first[i]:
                                    flag = True
                                    self.first[i].append(m)
                        else:
                            # 是终结符就跳出
                            break
                        # 没有空字符就不用处理后面的非终结符
                        if '$' not in self.first[n]:
                            break

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
                                                for e in self.first[word[k + 2]]:
                                                    if e != '$' and e not in self.last[word[k]]:
                                                        flag = True
                                                        self.last[word[k]].append(e)
                                            # 不是非终结符
                                            elif word[k + 2] not in self.last[word[k]]:
                                                flag = True
                                                self.last[word[k]].append(word[k + 2])

                                        # 把没有的符号加入last中
                                        elif n not in self.last[word[k]] and n != '$':
                                            ## 说明集合变化了，需要再循环一次
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
                    out = self.first[next_value]
                    for i in out:
                        if i != '$':
                            self.predict_table[item][i] = next_t
                else:
                    self.predict_table[item][next_value] = next_t
        for k in self.grammars:
            for next_grammar in self.grammars[k]:
                next_k = next_grammar.split()[0]

                if next_k in self.grammars and "$" in self.first[next_k] or next_k == "$":
                    for fk in self.last[k]:
                        self.predict_table[k][fk] = next_grammar

    def get_predict_table_(self, data):
        for item in self.grammars:
            self.predict_table_[item] = {}
            for next_t in self.grammars[item]:
                next_value = next_t.split()[0]
                if next_value in self.grammars:
                    out = self.first[next_value]
                    for i in out:
                        if i != '$':
                            self.predict_table_[item][i] = item + '->' + next_t
                else:
                    self.predict_table_[item][next_value] = item + '->' + next_t
        for k in self.grammars:
            for next_grammar in self.grammars[k]:
                next_k = next_grammar.split()[0]
                if next_k in self.grammars and "$" in self.first[next_k] or next_k == "$":
                    for fk in self.last[k]:
                        self.predict_table_[k][fk] = k + '->' + next_grammar.replace(" ", "")

if __name__ == "__main__":
    test = Predictive_Analysis()
    path = "全部测试程序\\11LL(1)测试用例\LL1_1.TXT"
    grammar = str(open(path).read())
    grammar = grammar.replace('->', ':')
    test.input(grammar)
    con='i+i*i'
    # con+='#'
    # con = ""
    # Filepath = "D:\pythonProject\pythonProject\新版编译器测试用例\\test12.txt"
    # for line in open(Filepath, 'r', encoding='UTF-8-sig'):
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
