import re


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
        self.Formula = dict()
        self.productions = dict()
        self.begin = ''
        self.predict_table = dict()
        self.predict_table_ = dict()
        self.vn = []
        self.vt = []
        self.grammars = dict()
        self.flag = 0
        self.first_dict = dict()
        self.follow_table = dict()
        self.recorder = dict()
        self.nonterminals = []  # 非终结符
        self.kong = []
        self.has_intersection = False  # 判断First集合和Follow集合是否有交集

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
        self.get_vn_vt(data)
        self.compute_first(self.productions)
        print('first', self.first)
        self.FIRST()
        print('first_dict', self.first_dict)
        for i in self.first:
            if '$' in self.first[i]:
                self.kong.append(i)
        print('kong', self.kong)
        self.find_follow()
        print(self.follow_table)
        # 判断First集合和Follow集合是否有交集
        for i in self.first_dict:
            self.first_dict[i] = set(self.first_dict[i])
        for i in self.follow_table:
            self.follow_table[i] = set(self.follow_table[i])
        for i in range(len(self.vn)):
            if self.first_dict[self.vn[i]] & self.follow_table[self.vn[i]]:
                self.has_intersection = True
                return
        self.get_predict_table_()
        print("\n预测分析表\n")
        for i in self.predict_table_:
            print(i, self.predict_table_[i])
        self.get_predict_table()

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
            if ':' not in production:
                continue
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
        self.nonterminals = list(set(self.nonterminals))
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
        # self.vt.append('$')
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

    """
    recorder： 用于求follow集合的过程中特殊情况：
        非终结符的后继非终结符的first集合可能存在null
        eg： A -> BC     C -> D | $   D -> (A) | i
        那么在一次遍历过程中，因为C的first集合存在null，所以需要将follow（A）加入follow（B）
        （重点）但是！此时的follow（A），并不是完整的，它可能在后续的遍历中会继续更新自身的follow集合
        所以此时会出现遗漏的follow
        所以这里需要进行记录并更新
    """

    def init_record(self):
        for k in self.grammars:
            self.follow_table[k] = []
            self.recorder[k] = []
            for next_grammar in self.grammars[k]:
                last_k = next_grammar.split()[-1]  # 取列表中的倒数第一个元素
                if last_k in self.grammars and last_k != k:
                    self.recorder[k].append(last_k)

    """
    刷新订阅
    检测到某个follow集合更新时，对其订阅的所有产生式左部的follow集合进行更新
    简而言之：follow（A）发生了更新，那么曾经将follow（A）加入自身的B，C也更新其follow
    并且，这是一个递归过程
    """

    def update(self, k):
        for lk in self.recorder[k]:
            new_lk = self.mix_set(self.follow_table[k], self.follow_table[lk])
            if new_lk != self.follow_table[lk]:
                self.follow_table[lk] = new_lk
                self.update(lk)

    """
    合并两个list并且去重
    """

    def mix_set(self, A, B):
        return list(set(A + B))

    """
    查找所有非终结符follow
    """

    def find_follow(self):
        self.init_record()
        # 参考书上101页
        self.follow_table[self.begin] = ["#"]
        for k in self.grammars:
            for next_grammar in self.grammars[k]:
                next_k = next_grammar.split()

                for i in range(0, len(next_k) - 1):
                    if next_k[i] in self.grammars:
                        if next_k[i + 1] not in self.grammars:
                            """
                            101页第二条，将a(next_k[i + 1])加入FOLLOW[next_k[i]]中
                            如果后继字符不是终结符，加入
                            """
                            new_follow = self.mix_set([next_k[i + 1]], self.follow_table[next_k[i]])
                            if new_follow != self.follow_table[next_k[i]]:
                                self.follow_table[next_k[i]] = new_follow
                                self.update(next_k[i])
                        else:
                            # 101页第三条，将FIRST[next_k[i + 1]]中非null元素加入FOLLOW[next_k[i]]中
                            new_follow = self.mix_set(self.first_dict[next_k[i + 1]], self.follow_table[next_k[i]])
                            """
                            如果后继字符的first集合中含有null，recorder更新follow集合
                            """
                            if "$" in self.first_dict[next_k[i + 1]]:
                                new_follow = self.mix_set(self.follow_table[k], new_follow)
                                self.recorder[k].append(next_k[i])
                            # 101页第四条，将follow_table[item]加入FOLLOW[next_k[i]]中
                            if new_follow != self.follow_table[next_k[i]]:
                                self.follow_table[next_k[i]] = new_follow
                                self.update(next_k[i])
                """
                产生式左部的follow集合加入最后一个非终结符的follow集合
                """
                # 101页第四条，将follow_table[item]加入FOLLOW[next_k[i]]中
                if next_k[-1] in self.grammars:
                    if next_k[-1] not in self.follow_table:
                        self.follow_table[next_k[-1]] = []
                    if next_k[-1] != k:
                        self.follow_table[next_k[-1]] = self.mix_set(self.follow_table[next_k[-1]],
                                                                     self.follow_table[k])

        for k in self.follow_table:
            if "$" in self.follow_table[k]:
                self.follow_table[k].remove("$")

    def get_predict_table(self):
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
                    for fk in self.follow_table[k]:
                        self.predict_table[k][fk] = next_grammar

    def get_predict_table_(self):
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
                    self.predict_table_[item][next_value] = item + '->' + next_t
                    print(self.predict_table_[item])
        for k in self.grammars:
            for next_grammar in self.grammars[k]:
                next_k = next_grammar.split()[0]
                if next_k in self.grammars and "$" in self.first_dict[next_k] or next_k == "$":
                    for fk in self.follow_table[k]:
                        self.predict_table_[k][fk] = k + '->' + next_grammar

# coding=utf-8
def check_charset(file_path):
    import chardet
    with open(file_path, "rb") as f:
        data = f.read(1000)
        charset = chardet.detect(data)['encoding']
    return charset

# if __name__ == "__main__":
#     test = Predictive_Analysis()
#     path = "全部测试程序\\07LL1预测分析测试用例\用户分词模式案例\LL1_1.TXT"
#     grammar = str(open(path).read())
#     grammar = grammar.replace('->', ':')
#     test.input(grammar)
#     print(test.first_dict)
#     print('----------------')
#     print(test.follow_table)
