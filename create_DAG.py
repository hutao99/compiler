from graphviz import Digraph


'''
将四元式序列传入
codes = [('-', '1', '', 'T0'), ('=', 'T0', '', 'A')...] 或 cc [['=', '3', '', 'T0'], ['*', '2', 'T0', 'T1']形式的四元式序列 可以为空或'_'
调用Partition_Basic_Block函数
返回优化后的四元式   optimize_quaternion
例如：optimize_quaternion = Partition_Basic_Block(codes)

基本块内部DAG优化：需要传入code=[('-', '1', '', 'T0'), ('=', 'T0', '', 'A')...]或cc [['=', '3', '', 'T0'], ['*', '2', 'T0', 'T1'] 形式的四元式 可以为空或'_'
调用以下函数：
DAG = create_DAG(code)
codes = optimize(DAG)
print('optcodes:',codes)

'''
#DAG优化 单目运算 双目运算 赋值运算
def DAG_draw(codes):
    filename = './DAG/visible'
    dot = Digraph(filename, 'comment', None, None, 'png', None, "UTF-8", )
    dot.attr('node', shape='circle', size='20,5', color='black')
    idx = 1 # 从1编号
    #codes [{'label': '3.14', 'node_label': 'T0'}, {'label': '2', 'node_label': []}, {'label': '*', 'node_label': ' T1', 'left': 1, 'right': 0}
    for code in codes:# label|node_label
        if len(code['node_label']) != 0: # 如果有node_label
            s = code['label'] + '|' + ''.join(code['node_label'])
        else:
            s = code['label']
        if len(code['node_label']) == 0 and 'father' not in code:
            pass
        else:
            dot.node(str(idx), s) #编号  标签
        idx += 1
    # print('codes',codes)
    for i, code in enumerate(codes):
        if 'left' in code: # 双目运算先连接左结点
            dot.edge(str(i+1), str(code['left'] + 1))
        if 'right' in code: # 双目运算再连接右节点
            dot.edge(str(i+1), str(code['right'] + 1))
        if 'son' in code: # 单目连接
            dot.edge(str(i+1), str(code['son'][0] + 1))
    dot.render()

def conform(elem, e, left, right):
    # elem * e {'label': '3.14', 'node_label': ['T0']} left 1 right 0
    if 'left' not in e: # 如果结点没有左结点
        return False
    if left != e['left']: # 如果有左结点但结点列表不等于left
        return False
    if 'right' not in e:
        return  False
    if right != e['right']:
        return False
    if elem == e['label'] or elem in e['node_label']:
        return True
    else:
        return False


def isleaf(e): # 判断是否是叶子节点 如果有左或右或son节点 返回False 表明不是子节点
    if 'son' in e or 'left' in e or 'right' in e:
        return False
    else:
        return True


# 是否在DAG中
def is_in_DAG(DAG, elem, son = None, left = None, right = None):# elem +-*/
    if not son and not left and not right:
        for e in DAG:
            if elem == e['label'] or elem in e['node_label']:
                return True
    elif son:
        for e in DAG:
            if 'son' in e: #
                if (elem == e['label'] or elem in e['node_label']) and son in e['son']:
                    return True
    else:
        for e in DAG:
            if conform(elem, e, index_of_DAG(DAG, left), index_of_DAG(DAG, right)):
                return True
    return False

# #('=', ' 3.14', ' ', ' T0') 3.14是否为结点中
# def is_in_DAG2(DAG, elem, son = None, left = None, right = None):# elem +-*/
#     for e in DAG:
#         if elem == e['label']:
#             return True
#     return False
def index_of_DAG(DAG, x):
    if x not in ['+', '-', '/', '*','&&','||','!','@','>','<','>=','<=','!=','==']:
        for i, e in enumerate(DAG):
            if x in e['node_label'] or x == e['label']:
                return i
    return None

def is_in_label(DAG, elem):
    for e in DAG:
        if elem == e['label'] :
            return True
    return False

def is_operator_nodelabel(DAG,elem):
    for e in DAG:
        if elem in e['node_label'] and not (e['label'][0].isdigit()):#(%|temp) 左边是运算符
            return True
    return False

# 将字符串转换为对应类型的数字
def determine_number_type(string):
    if string.isdigit():
        return int(string)
    elif '.' in string or 'e' in string.lower():
        return float(string)

# 转换常量表达式
def conversion_constant_expression(codes:list):
    for j in range(len(codes)):
        temp = 0
        i = codes[j]
        # 对常数表达式做处理 如 [+,1,2,T0],[+,T0,4,x]->[=,7,,x]
        if i[1] not in ['','_'] and i[2] not in ['','_']:
            if (i[1][0].isdigit() or i[1][0] == '-') and (i[2][0].isdigit() or i[2][0] == '-'):
                if i[0] == '+':
                    temp = determine_number_type(i[1]) + determine_number_type(i[2])
                elif i[0] == '-':
                    temp = determine_number_type(i[1]) - determine_number_type(i[2])
                elif i[0] == '*':
                    temp = determine_number_type(i[1]) * determine_number_type(i[2])
                elif i[0] == '/':
                    temp = determine_number_type(i[1]) / determine_number_type(i[2])
                elif i[0] == '%':
                    temp = determine_number_type(i[1]) % determine_number_type(i[2])
                elif i[0] == '&&':
                    temp = determine_number_type(i[1]) and determine_number_type(i[2])
                elif i[0] == '||':
                    temp = determine_number_type(i[1]) or determine_number_type(i[2])
                elif i[0] == '>':
                    if determine_number_type(i[1]) > determine_number_type(i[2]):
                        temp = 1
                    else:
                        temp = 0
                elif i[0] == '<':
                    if determine_number_type(i[1]) < determine_number_type(i[2]):
                        temp = 1
                    else:
                        temp = 0
                elif i[0] == '>=':
                    if determine_number_type(i[1]) >= determine_number_type(i[2]):
                        temp = 1
                    else:
                        temp = 0
                elif i[0] == '<=':
                    if determine_number_type(i[1]) <= determine_number_type(i[2]):
                        temp = 1
                    else:
                        temp = 0
                elif i[0] == '==':
                    if determine_number_type(i[1]) == determine_number_type(i[2]):
                        temp = 1
                    else:
                        temp = 0
                elif i[0] == '!=':
                    if determine_number_type(i[1]) != determine_number_type(i[2]):
                        temp = 1
                    else:
                        temp = 0
                codes[j] = ['=', str(temp), '', i[3]]
        elif i[0]!= '=' and i[1] not in ['','_'] and i[2] in ['','_']and (i[1][0].isdigit() or i[1][0] == '-'):
            if i[0] == '!':
                temp = not determine_number_type(i[0])
            elif i[0] == '@' or i[0] == '-':
                i[0] = i[0].replace("@", "-")
                temp = - determine_number_type(i[1])
            codes[j] = ['=', str(temp), '', i[3]]
    return codes

#建立DAG
def create_DAG(codes: list): # start
    # 将四元式转变为列表形式 方便后面对列表进行改动
    l = []
    for i in codes:
        l.append(list(i))
    codes = l
    # 对常量表达式生成的四元式列表进行赋值四元式处理
    codes = conversion_constant_expression(codes)
    DAG = []
    global Active_variable
    # 记录活跃变量
    Active_variable = []
    for code in codes:
        flag = 0
        for i in code:
            i = str(i)
            if flag == 0:
                flag = 1
                continue
            if i in ['_',''] or i[0] == 'T' : # T是临时变量
                continue
            if not i[0].isdigit() and i not in Active_variable:
                Active_variable.append(i)
    for code in codes: # ('=', ' 3.14', ' ', ' T0')
        if code[0] == '=': # x = y
            if code[1] == code[3]:
                continue
            if is_in_DAG(DAG, code[3]):
                delete(DAG, code[3])
                pass
            if not is_in_DAG(DAG, code[1]):# code[1]不在DAG
                DAG.append({'label': code[1], 'node_label': [code[3]]})
            elif code[1] in Active_variable and not is_in_label(DAG,code[1]) and is_operator_nodelabel(DAG,code[1]): # 如果code【1】是活跃变量 且在DAG 且不在DAG label中
                DAG.append({'label': code[1], 'node_label': [code[3]]})
            # a = 1;b = 2;c = a;a = b;b = c;
            else:# 如果不为活跃变量 或为活跃变量 且在DAGlabel中
                append_node_label(DAG, code[1], code[3])
        elif code[0] == '@' or (code[0] == '-' and  (code[2] == '' or code[2] == '_')): # x = @ y
            if not is_in_DAG(DAG, code[1]):
                DAG.append({'label': code[1], 'node_label': []})
            if not is_in_DAG(DAG, code[0], son = code[1]):
                father = {'label': code[0], 'node_label': [code[3]]}
                link(DAG, father, son = code[1])
                if is_in_DAG(DAG, code[3]):
                    delete(DAG, code[3])
                    pass
                DAG.append(father)
        elif code[1] != '' and code[2] != '': # x = y op z
            if not is_in_DAG(DAG, code[0], left = code[1], right = code[2]):
                if is_in_DAG(DAG, code[3]):
                    delete(DAG, code[3])
                father = {'label': code[0], 'node_label': [code[3]]} # 建立结点
                DAG.append(father)
                if not is_in_DAG(DAG, code[1]):
                    DAG.append({'label': code[1], 'node_label': []})
                if not is_in_DAG(DAG, code[2]):
                    DAG.append({'label': code[2], 'node_label': []})
                link(DAG, father, left = code[1], right = code[2])
            else:
                if is_in_DAG(DAG, code[3]):
                    delete(DAG, code[3])
                    pass
                append_node_label(DAG, code[0], code[3], code[1], code[2])

    return DAG
def append_node_label(DAG, label, node_label,left = None, right = None):
    if left and right:
        lr = index_of_DAG(DAG, left)
        rg = index_of_DAG(DAG, right)
        for elem in DAG:
            if elem['label'] == label or label in elem['node_label']:
                if 'left' in elem and lr == elem['left'] and \
                    'right' in elem and rg == elem['right']:
                    elem['node_label'].append(node_label)
                    return
    else:
        for elem in DAG:
            if elem['label'] == label or label in elem['node_label']:
                elem['node_label'].append(node_label)
                return

def delete(DAG, label): # 从结点列表里面删除
    for e in DAG:
        if label in e['node_label']:
            e['node_label'].remove(label)

def link(DAG, father, son = None, left = None, right = None):
    fa = index_of_DAG(DAG, father)  # 父节点索引
    if son:
        e2 = index_of_DAG(DAG, son)
        if 'son' not in father:
            father['son'] = []
        father['son'].append(e2)
        if 'father' not in DAG[e2]:
            DAG[e2]['father'] = []
        if fa not in DAG[e2]['father']:
            DAG[e2]['father'].append(fa)
    else:
        lf,rg = index_of_DAG(DAG, left),index_of_DAG(DAG, right)
        if 'father' not in DAG[lf]:
            DAG[lf]['father'] = []
        if fa not in DAG[lf]['father']:
            DAG[lf]['father'].append(fa)
        if 'father' not in DAG[rg]:
            DAG[rg]['father'] = []
        if fa not in DAG[rg]['father']:
            DAG[rg]['father'].append(fa)
        father['left'],father['right'] = lf,rg


def optimize(DAG_node):
    global T_flag
    T_flag = []  # 根据后面a[T0] 先判断是否生成T0的四元式 再生成a[T0]的四元式
    # print('DAG_node:',DAG_node)
    global Active_variable
    # print('Active_variable:',Active_variable)
    T_quaternion = {} # a[T0]对应的四元式
    id = 1
    for e in DAG_node:
        new_label = [] # 记录活跃变量
        if e['node_label']:#标识符结点列表有记录
            for i in e['node_label']:
                if i in Active_variable:
                    new_label.append(i)
            if len(new_label) == 0:# 如果没有活跃变量 则标识符列表显示列表第一个元素
                new_label.append(e['node_label'][0])
        else: # 标识符结点为空 可能为叶子节点 也可能为中间结点 但临时变量跑了
            if not isleaf(e): # 如果不是叶子节点 新增变量进行标记
                new_label.append('t_'+str(id))
                id+=1
        e['node_label'] = new_label
    code = []
    for e in DAG_node:
        if 'son' in e:
            son = DAG_node[e['son'][0]]
            la = (e['label'], son['label'], '_', e['node_label'][0] ) if not son['node_label'] \
                                                                       or isleaf(son) else (e['label'], son['node_label'][0], '_', e['node_label'][0] )
            temp = e['node_label'][0]
            if temp[0] == 'T': #如果是T变量
                if temp not in T_flag:
                    T_flag.append(temp)
                code.append(la)
                if temp in T_quaternion:
                    code.append(T_quaternion[temp])
                    del T_quaternion[temp] #从字典中删除
            else:
                code.append(la)
        elif 'left' in e and 'right' in e:
            left = DAG_node[e['left']]
            right = DAG_node[e['right']]
            fun1 = left['label'] if not left['node_label'] or isleaf(left) else left['node_label'][0]
            fun2 = right['label'] if not right['node_label'] or isleaf(right) else right['node_label'][0]
            temp = e['node_label'][0]
            if temp[0] == 'T':  # 如果是T变量
                code.append((e['label'], fun1, fun2, e['node_label'][0]))
                if temp not in T_flag:
                    T_flag.append(temp)
                if temp in T_quaternion:
                    code.append(T_quaternion[temp])
                    del T_quaternion[temp]  # 从字典中删除
            else:
                code.append((e['label'], fun1, fun2, e['node_label'][0]))
        elif len(e['node_label']) >= 1:
            for i in e['node_label']:
                if i in Active_variable:
                    if '[' in i: #对数组变量做处理 a[T0]
                        t_index = i.find('T')
                        if t_index != -1:
                            num_str = i[t_index + 1:-1]
                        ss = 'T'+str(num_str)
                        if ss in T_flag:
                            code.append(('=', e['label'], '_', i))
                        else:
                            T_quaternion[ss] = ('=', e['label'], '_', i)
                    else: #不是数组变量
                        code.append(('=', e['label'], '_', i))
    # print('code:',code)
    return code

#切分基本块
def Partition_Basic_Block(codes):
    # print(codes)
    # 转化成列表形式
    new_codes = []
    for i in codes:
        new_codes.append(list(i))
    codes = new_codes
    filename = './Basic_Block/basic_block'
    dot = Digraph(filename, 'Basic_Block', None, None, 'png', None, "UTF-8")
    # 划分基本块
    basic_blocks = []
    flag = []  # 入口flag
    flag.append(0) #刚开始的语句是入口
    for i in range(len(codes)):
        if codes[i][0][0] == 'j':
            if int(codes[i][3]) not in flag: # 跳转语句跳转到的地方是入口
                flag.append(int(codes[i][3]))
            if (i + 1) < len(codes) and (i + 1) not in flag:  # 跳转语句的下一条语句也是入口
                flag.append(i + 1)
    flag.append(len(codes))
    # print(flag)
    flag.sort()  # 对列表进行排序
    # print('基本块切分序号列表',flag)

    j = 1
    # 当前基本块
    current_blocks = []
    for i in range(len(codes)):
        if i < flag[j]:
            current_blocks.append(codes[i])
        else:
            basic_blocks.append(current_blocks)
            current_blocks = []
            current_blocks.append(codes[i])
            j += 1
    if len(current_blocks)!=0:
        basic_blocks.append(current_blocks)
    # 基本块流程图
    # 基本块序号
    basic_number = 0
    idx = 0 # 四元式序号
    for code in basic_blocks:
        text = ''
        for c in code:
            text+=str(idx)+":"+str(c)+'\n'
            idx+=1
        dot.node(str(basic_number),text, fontname="SimHei",shape='rectangle')
        basic_number+=1

    max_basic_number = basic_number-1 #最后一个基本块的编号
    basic_number = 0

    for code in basic_blocks:
        if code[-1][0] in ['jnz','j<','j>','j>=','j<=','j==','j!=']: # 对跳转语句做处理 下一条 及跳转到的
            id = int(code[-1][3])
            basic_idx = flag.index(id)
            dot.edge(str(basic_number), str(basic_idx))
            if basic_idx < max_basic_number: # 不是最后一个基本块
                dot.edge(str(basic_number), str(basic_number + 1))
        elif code[-1][0] == 'jz' or code[-1][0] == 'j': # 跳转到下一条语句
            id = int(code[-1][3])
            basic_idx = flag.index(id)
            dot.edge(str(basic_number), str(basic_idx))
        else:
            if basic_number < max_basic_number:# 不是最后一个基本块
                dot.edge(str(basic_number),str(basic_number+1))
        basic_number+=1
    dot.render()
    return basic_blocks


#对程序中的所有基本块进行优化
def all_basic_optimize(basic_blocks):
    optimize_quaternion = []
    number = 0
    for code in basic_blocks:
        dag_block = []
        count = 0
        for c in code: # 遍历每一个四元式
            if c[0] in ['+', '-', '*', '/', '%', '=','&&','||','!','@','>','<','>=','<=','!=','==']:
                dag_block.append(c)
            else:
                if len(dag_block) == 1: # 优化四元式只有一条
                    count+=1
                    optimize_quaternion.append(dag_block[0])
                    dag_block = []
                elif len(dag_block) > 1: # 对四元式进行优化
                    DAG = create_DAG(dag_block) # 建立DAG
                    codes = optimize(DAG) # 优化后的DAG
                    count+=len(codes) # 优化后的四元式条数
                    for i in codes:
                        optimize_quaternion.append(list(i))
                    dag_block = []
                count+=1
                optimize_quaternion.append(c)
        if len(dag_block) == 1:  # 优化四元式只有一条
            count += 1
            optimize_quaternion.append(dag_block[0])
            dag_block = []
        elif len(dag_block) > 1:  # 对四元式进行优化
            DAG = create_DAG(dag_block)
            codes = optimize(DAG)
            count += len(codes)
            for i in codes:
                optimize_quaternion.append(list(i))
            dag_block = []

        # 更新跳转语句跳转四元式
        prelen = len(code) # 原先四元式条数
        count2 = prelen-count # 优化四元式条数
        for c1 in basic_blocks: # 更新四元式跳转语句
            for c2 in c1:
                if c2[0][0] == 'j':
                    l = list(c2)
                    if int(c2[3]) > number:
                        c2[3] = int(c2[3]) - count2
        number+=count

    #返回优化后的四元式列表
    return optimize_quaternion



def test1():#基本块内优化
    with open(r'D:\pythonProject\fundamentals of compiling\全部测试程序\14DAG测试用例\DAG_1.txt', 'r') as f:
        s = f.read()
        if s[0] == '(':
                lst = [tuple(x.strip() for x in line.strip("()").split(",")) for line in s.splitlines()]
                code = [tuple(x.strip() for x in _[1:-1].split(',')) for _ in s.split("\n")]
        else:
                code = [tuple(x.strip() for x in _.split(',')) for _ in s.split("\n")]
    DAG = create_DAG(code)
    codes = optimize(DAG)
    # print('optcodes:',codes)

def test2(): # 将程序划分为基本块，得到DAG优化代码
    global Active_variable
    # codes =[('=', '3', '_', 'T0'), ('*', '2', 'T0', 'T1'), ('+', 'R', 'r', 'T2'), ('*', 'T1', 'T2', 'A'), ('=', 'A', '_', 'B'), ('*', '2', 'T0', 'T3'), ('+', 'R', 'r', 'T4'), ('*', 'T3', 'T4', 'T5'), ('-', 'R', 'r', 'T6'), ('*', 'T5', 'T6', 'B'),('j', '', '', 11),('+', 'A', 'B', 'T1'), ('-', 'A', 'B', 'T2'), ('*', 'T1', 'T2', 'F'), ('-', 'A', 'B', 'T1'), ('-', 'A', 'C', 'T2'), ('-', 'B', 'C', 'T3'), ('*', 'T1', 'T2', 'T1'), ('*', 'T1', 'T3', 'G')]
    codes = [['main', '', '', ''], ['=', '0', '', 'sum'], ['*', '0', '3', 'T0'], ['+', 'T0', '0', 'T1'], ['=', '80', '', 'a[T1]'], ['*', '0', '3', 'T2'], ['+', 'T2', '1', 'T3'], ['=', '75', '', 'a[T3]'], ['*', '0', '3', 'T4'], ['+', 'T4', '2', 'T5'], ['=', '92', '', 'a[T5]'], ['*', '1', '3', 'T6'], ['+', 'T6', '0', 'T7'], ['=', '61', '', 'a[T7]'], ['*', '1', '3', 'T8'], ['+', 'T8', '1', 'T9'], ['=', '65', '', 'a[T9]'], ['*', '1', '3', 'T10'], ['+', 'T10', '2', 'T11'], ['=', '71', '', 'a[T11]'], ['*', '2', '3', 'T12'], ['+', 'T12', '0', 'T13'], ['=', '59', '', 'a[T13]'], ['*', '2', '3', 'T14'], ['+', 'T14', '1', 'T15'], ['=', '63', '', 'a[T15]'], ['*', '2', '3', 'T16'], ['+', 'T16', '2', 'T17'], ['=', '70', '', 'a[T17]'], ['*', '3', '3', 'T18'], ['+', 'T18', '0', 'T19'], ['=', '85', '', 'a[T19]'], ['*', '3', '3', 'T20'], ['+', 'T20', '1', 'T21'], ['=', '87', '', 'a[T21]'], ['*', '3', '3', 'T22'], ['+', 'T22', '2', 'T23'], ['=', '90', '', 'a[T23]'], ['*', '4', '3', 'T24'], ['+', 'T24', '0', 'T25'], ['=', '76', '', 'a[T25]'], ['*', '4', '3', 'T26'], ['+', 'T26', '1', 'T27'], ['=', '77', '', 'a[T27]'], ['*', '4', '3', 'T28'], ['+', 'T28', '2', 'T29'], ['=', '85', '', 'a[T29]'], ['=', '0', '', 'i'], ['j<', 'i', '3', 50], ['j', '', '', 66], ['=', '0', '', 'j'], ['j<', 'j', '5', 53], ['j', '', '', 60], ['*', 'j', '3', 'T32'], ['+', 'T32', 'i', 'T33'], ['+', 'sum', 'a[T33]', 'T34'], ['=', 'T34', '', 'sum'], ['+', 'j', '1', 'T31'], ['=', 'T31', '', 'j'], ['j', '', '', 51], ['/', 'sum', '5', 'T35'], ['=', 'T35', '', 'v[i]'], ['=', '0', '', 'sum'], ['+', 'i', '1', 'T30'], ['=', 'T30', '', 'i'], ['j', '', '', 48], ['+', 'v[0]', 'v[1]', 'T36'], ['+', 'T36', 'v[2]', 'T37'], ['/', 'T37', '3', 'T38'], ['=', 'T38', '', 'average'], ['para', '"math:    language:      C programming"', '', ''], ['call', 'write', '', ''], ['para', 'v[0]', '', ''], ['call', 'write', '', ''], ['para', 'v[1]', '', ''], ['call', 'write', '', ''], ['para', 'v[2]', '', ''], ['call', 'write', '', ''], ['para', '"total average:"', '', ''], ['call', 'write', '', ''], ['para', 'average', '', ''], ['call', 'write', '', ''], ['sys', '', '', '']]

    # cc = []
    # for i in codes:
    #     cc.append(i[1:])
    # print('cc:', cc)
    # codes=cc
    basic_blocks=Partition_Basic_Block(codes)
    optimize_quaternion = all_basic_optimize(basic_blocks)
    print('optimize_quaternion',optimize_quaternion)
    print(len(codes),len(optimize_quaternion))

def test3():
    codes = [[0, 'main', '_', '_', '_'], [1, '=', '100', '_', 'm'], [2, '/', 'max', '2', 'T0'], [3, '<', 'm', 'T0', 'T1'], [4, 'jnz', 'T1', '_', 9], [5, 'jz', 'T1', '_', 31], [6, '+', 'm', '1', 'T2'], [7, '=', 'T2', '_', 'm'], [8, 'j', '_', '_', 2], [9, '/', 'm', '100', 'T3'], [10, '=', 'T3', '_', 'a'], [11, '/', 'm', '10', 'T4'], [12, '%', 'T4', '10', 'T5'], [13, '=', 'T5', '_', 'b'], [14, '%', 'm', '10', 'T6'], [15, '=', 'T6', '_', 'c'], [16, '*', 'a', 'a', 'T7'], [17, '*', 'T7', 'a', 'T8'], [18, '*', 'b', 'b', 'T9'], [19, '*', 'T9', 'b', 'T10'], [20, '+', 'T8', 'T10', 'T11'], [21, '*', 'c', 'c', 'T12'], [22, '*', 'T12', 'c', 'T13'], [23, '+', 'T11', 'T13', 'T14'], [24, '==', 'm', 'T14', 'T15'], [25, 'jnz', 'T15', '_', 27], [26, 'jz', 'T15', '_', 30], [27, 'para', 'm', '_', '_'], [28, 'call', 'write', '_', 'T16'], [29, 'j', '_', '_', 30], [30, 'j', '_', '_', 6], [31, 'sys', '_', '_', '_']]
    cc = []
    for i in codes:
        cc.append(i[1:])
    print('cc:',cc)
    optimize_quaternion = Partition_Basic_Block(cc)
    print('optimize_quaternion', optimize_quaternion)

# test2()