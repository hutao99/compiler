import string
lines = []
nonterminals = [] #非终结符
productions = {}
first = {}
follow_dict = {}
first_dict = {}
kong = []
print_dic = {'A1':"程序",'A2':'声明语句','A3':'复合语句','A4':'函数块','A5':'函数定义','A6':'函数类型','A7':'标识符','A8':'函数定义形参列表',
             'B1':'函数定义形参','B2':'变量类型','C1':'语句','C2':'执行语句','C3':'值声明','C4':'函数声明','C5':'常量声明','C6':'变量声明','C7':'常量类型','C8':'常量声明表','C9':'常量',
             'D1':'变量声明表','D2':'单变量声明','D3':'变量','D4':'表达式','D5':'函数声明形参列表','D6':'函数声明形参','D7':'数据处理语句','D8':'控制语句',
             'E1':'赋值语句','E2':'函数调用语句','E3':'赋值表达式','E4':'函数调用','E5':'语句表',
             'F1':'关系表达式','F2':'算术表达式','F3':'关系运算符','F4':'布尔表达式','F5':'布尔项','F6':'布尔因子',
             'G1':'项','G2':'因子','G3':'常量','G4':'变量','G5':'数值型常量','G6':'字符型常量','G7':'布尔常量','H1':'实参列表','H2':'实参',
             'I1':'if语句','I2':'for语句','I3':'while语句','I4':'dowhile语句','I5':'return语句','J6':'break语句','J7':'continue语句'}

# print(productions)
# print(nonterminals)
# print(len(nonterminals))


def compute_first(productions):
    first = {}

    # # 初始化终结符号的FIRST集
    # for terminal in terminals:
    #     first[terminal] = {terminal}

    # 初始化非终结符号的FIRST集
    for nonterminal in nonterminals:
        first[nonterminal] = set()

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
                    if symbol not in nonterminals:
                        if symbol not in first[left]:
                            first[left].add(symbol)
                            changed = True
                        break

                    # 如果是非终结符号，则将其FIRST集合并到左部符号的FIRST集中
                    elif symbol in nonterminals:
                        for s in first[symbol]:
                            if s != 'r' and s not in first[left]:
                                first[left].add(s)
                                changed = True

                        # 如果该非终结符号不能推导出空串，则退出循环
                        if 'r' not in first[symbol]:
                            break

                        # 否则，继续处理下一个符号
                        i += 1

                # 如果产生式右部的所有符号都能推导出空串，则将空串加入左部符号的FIRST集中
                else:
                    if 'r' not in first[left]:
                        first[left].add('r')
                        changed = True

        # 如果FIRST集不再发生变化，则退出循环
        if not changed:
            break

    return first


def compute_first_set(symbols):
    first_set = set()
    i = 0
    while i < len(symbols):
        symbol = symbols[i]
        if symbol not in nonterminals:
            first_set.add(symbol)
            break
        elif symbol in nonterminals:
            first_i = first[symbol] - {'r'}
            first_set |= first_i
            if 'r' not in first[symbol]:
                break
        else:
            raise ValueError(f"Invalid symbol: {symbol}")
        i += 1
    else:
        first_set.add('r')
    return first_set

# print('kong',kong)
def compute_follow( start_symbol):
    follow_sets = {symbol: set() for symbol in nonterminals}
    follow_sets[start_symbol].add('eof')
    updated = True

    while updated:
        updated = False
        # 遍历每个产生式
        for lhs,right in productions.items():

            for rhs in right:

                # 遍历产生式右部的每个符号
                for i in range(len(rhs)):
                    symbol = rhs[i]

                    # 如果该符号是非终结符且与当前处理的非终结符不同
                    if symbol in nonterminals and symbol != lhs:

                        # 将Follow集合添加到该符号后面的符号的First集合中
                        j = i + 1
                        while j < len(rhs):
                            next_symbol = rhs[j]
                            if next_symbol not in nonterminals:
                                follow_sets[symbol].update({next_symbol})
                                break
                            else:
                                follow_sets[symbol].update(first[next_symbol]-{'r'})
                            if 'r' not in first[next_symbol]:
                                break
                            j += 1

                        # 如果该符号是产生式的最后一个符号或者后面的符号的First集合不包含空串
                        if j == len(rhs)  :
                            # 将产生式左部非终结符的Follow集合添加到该符号的Follow集合中
                            if follow_sets[lhs].difference(follow_sets[symbol]):
                                updated = True
                                follow_sets[symbol].update(follow_sets[lhs])

        # 处理起始符号的Follow集合
        if start_symbol in nonterminals:
            if follow_sets[start_symbol].difference({'eof'}):
                updated = True
                follow_sets[start_symbol].add('eof')

    return follow_sets




def start():
    global first,first_dict,kong,follow_dict
    with open('文法.txt', 'r') as f:
        s = f.read()
        for production in s.split('\n'):
            left, right = production.split('->')
            left = left.strip()
            # 按照空格分割右部符号
            symbols_list = right.split(' | ')

            # 将左部和右部添加到字典中
            if left not in productions:
                productions[left] = []
                nonterminals.append(left)
            for symbols in symbols_list:
                productions[left].append(symbols.split())
    first = compute_first(productions)
    # 计算每个候选式的FIRST集
    for nonter, production in productions.items():
        first_dict[nonter] = []
        for rhs in production:
            first_set = compute_first_set(rhs)
            first_dict[nonter].append(list(first_set))

    for i in first:
        if 'r' in first[i]:
            kong.append(i)
    follow_dict = compute_follow('A1')
    for i in follow_dict:
        follow_dict[i] = list(follow_dict[i])
    return first_dict, follow_dict, print_dic, kong
