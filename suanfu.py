import sys
import operator
import copy

#终结符
class Suanfufirst:
    def __init__(self):
        #终结符
        self.terSymbol = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','=','+','-','*','@','/','(',')','^','#','%','>','<','>=','<=','==','!=','or','&&','&','!']
        #非终结符
        self.non_ter = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

        self.firstVT = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.lastVT = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.grammer = ['A -> A or B | B','B -> B && C | C','C -> C > D | C < D | C >= D | C <= D | C == D | C != D | D',
                        'D -> ! E | E','E -> E + T | E - T | T', 'T -> T * F | T / F | T % F | F','F -> @ P | P','P -> ( A ) | a']
        # self.grammer = ['E->E+T|E-T|T\n', 'T->T*F|T/F|T%F|F\n', 'F->(E)|a\n']
        # self.grammer = ['G->A=E\n', 'A->a\n', 'E->E+T|E-T|T\n', 'T->T*F|T/F|F\n', 'F->(E)|a\n']
        self.num,self.gra= self.chushihua(self.grammer)

    #求非终结符的firstVT集
    def first(self,gra_line): #'A->A and B|B'
        #开头的非终结符，所以求的是x的firstVT
        gra_line = gra_line.split()
        x = gra_line[0]
        ind = self.non_ter.index(x) # 获取在非终结符中的下角标 作为first的角标
        indexSET = []
        # 找到所有产生式右部的第一个字符，下标值返回列表indexSET1
        i = 0
        while i < len(gra_line):
            if gra_line[i] == '->' or gra_line[i] == '|':
                indexSET.append(i + 1)
            i += 1
        #判断符合P->a...或P->Qa...，以及P->Q...那个情况，注意gra_line[i]是当前遍历的字符
        for i in indexSET:
            if gra_line[i] in self.terSymbol and gra_line[i] not in self.firstVT[ind]: #在非终结符且不在firstVT中，进行添加操作 p->a
                self.firstVT[ind].append(gra_line[i])
            elif gra_line[i] in self.non_ter: # 在非终结符
                for f in self.firstVT[self.non_ter.index(gra_line[i])]:# 将非终结符中的first添加 P->Q
                    if f not in self.firstVT[ind]:
                        self.firstVT[ind].append(f)
                if (i+1) < len(gra_line) and gra_line[i + 1] in self.terSymbol and gra_line[i + 1] not in self.firstVT[ind]:# P->Qa
                    self.firstVT[ind].append(gra_line[i + 1])
        return self.firstVT

    #求lastVT集
    def last(self,gra_line):
        # 开头的非终结符，所以求的是x的lastVT
        gra_line = gra_line.split()
        x = gra_line[0]
        ind = self.non_ter.index(x)
        indexSET = []
        # 找到所有产生式右部的最后一个字符，下标值返回列表indexSET
        i = 0
        while i < len(gra_line):
            if gra_line[i] == '|':
                indexSET.append(i - 1)
            i += 1
        indexSET.append(len(gra_line)-1)
        # 判断符合P->...a或P->...aQ，以及P->...Q那个情况，注意gra_line[i]是当前遍历的字符
        for i in indexSET:
            if gra_line[i] in self.terSymbol and gra_line[i] not in self.lastVT[ind]:# p->...a
                self.lastVT[ind].append(gra_line[i])
            elif gra_line[i] in self.non_ter:#p->...Q
                for f in self.lastVT[self.non_ter.index(gra_line[i])]:
                    if f not in self.lastVT[ind]:
                        self.lastVT[ind].append(f)
                if gra_line[i - 1] in self.terSymbol and gra_line[i - 1] not in self.lastVT[ind]:#p->...aQ
                    self.lastVT[ind].append(gra_line[i - 1])
        return self.lastVT


    #获取文法中的所有右部
    def prostr(self,grammer):
        pro_str = []
        for gra_line in grammer:
            gra_line = gra_line.split()
            #先看每一行有几个产生式，把每一个产生式的开始索引加入pro_index
            pro_index = []
            i = 0
            while i < len(gra_line):
                if gra_line[i] == '->' or gra_line[i] == '|':
                    pro_index.append(i + 1)
                i += 1
            for p in pro_index:
                str = []
                for s in gra_line[p:]:
                    if s == '|':
                        break
                    else:
                        str.append(s)
                pro_str.append(str)
        return pro_str


    #构造优先关系表
    def table(self,grammer, num): # grammer:文法  num:文法中所有的终结符+-*/%
        #表头
        n = len(num) + 1
        #创建一个n行n列的空表
        gra = [[' ' for col in range(n)] for row in range(n)]
        #填充表头
        i = 1
        #将非终结符填充至第一行
        for c in num:
            gra[0][i] = c
            i += 1
        #将非终结符填充至第一列
        j = 1
        for r in num:
            gra[j][0] = r
            j += 1
        #填充表体
        pro_str = self.prostr(grammer) #得到所有表达式的所有右部候选式
        for str in pro_str: #遍历每一个候选式
            j = -1
            for i in range(len(str)-1):
                #i是当前元素，j是当前索引
                j += 1
                if str[i] in self.terSymbol and str[i + 1] in self.terSymbol: #  Xi vt xi+1 vt 则=
                    #查找对应角标
                    r = num.index(str[i]) + 1
                    c = num.index(str[i + 1]) + 1
                    if gra[r][c] == '·>' or gra[r][c] == '<·':
                        #print("该文法不是算符优先文法，请检查输入")
                        return False
                    else:
                        gra[r][c] = '=·'
                if i < (len(str) - 2) and str[i] in self.terSymbol and str[i + 2] in self.terSymbol and str[i + 1] in self.non_ter:#终结符 非终结符 终结符
                    r = num.index(str[i]) + 1
                    c = num.index(str[i + 2]) + 1
                    if gra[r][c] == '·>' or gra[r][c] == '<·':
                        #print("该文法不是算符优先文法，请检查输入")
                        return False
                    else:
                        gra[r][c] = '=·'
                if str[i] in self.terSymbol and str[i + 1] in self.non_ter:# 终结符 非终结符 小于
                    for a in self.firstVT[self.non_ter.index(str[j + 1])]:
                        r = num.index(str[i]) + 1
                        c = num.index(a) + 1
                        if gra[r][c] == '·>' or gra[r][c] == '=·':
                            #print("该文法不是算符优先文法，请检查输入")
                            return False
                        else:
                            gra[r][c] = '<·'
                if str[i] in self.non_ter and str[i + 1] in self.terSymbol:# 终结符 非终结符
                    for a in self.lastVT[self.non_ter.index(str[i])]:
                        r = num.index(a) + 1
                        c = num.index(str[i + 1]) + 1
                        if gra[r][c] == '=·' or gra[r][c] == '<·':
                            #print("该文法不是算符优先文法，请检查输入")
                            return False
                        else:
                            gra[r][c] = '·>'
        #添加#的行和列元素
        for a in self.firstVT[self.non_ter.index(grammer[0][0])]: # #《开始符号的firstVT中的元素
            r = num.index('#') + 1
            c = num.index(a) + 1
            gra[r][c] = '<·'
        for a in self.lastVT[self.non_ter.index(grammer[0][0])]:# 开始符号的firstVT中的元素》vt
            r = num.index(a) + 1
            c = num.index('#') + 1
            gra[r][c] = '·>'
        r = num.index('#') + 1
        c = num.index('#') + 1
        gra[r][c] = '=·'
        return gra


    #归约函数
    def reduce(self,str,grammer):
        #str是传进来的最左素短语 是否在文法右部
        p_s = self.prostr(grammer)
        for s in p_s:
            if len(s) != len(str):
                continue
            else:
                j = 0
                for i in s:
                    #如果是最后一个字符相比较了
                    if j + 1 == len(str):
                        if i in self.terSymbol and str[j] in self.terSymbol and i == str[j]:
                            return True
                        elif i in self.non_ter and str[j] in self.non_ter:
                            return True
                    else:
                        if i in self.terSymbol and str[j] in self.terSymbol and i == str[j]:
                            j += 1
                        elif i in self.non_ter and str[j] in self.non_ter:
                            j += 1
                        else:
                            break
        return False

        # 总控程序

    def master(self, count, placeid, ana_str, num, gra, digit_str): # 四元式传入编号 T变量编号
        stack = ['#']
        digit_stack = []
        id1 = 0
        ana_str.append('#')
        # print("当前栈中元素为：")
        # print(stack)
        # print("当前字符串为：")
        # print(ana_str)
        str_list = []
        while stack != ['#', 'N', '#']:
            if ana_str[0] == '#':
                stack.append('#')
                continue
            # 字符串第一个字符是非终结符，则加入栈
            if ana_str[0] in self.non_ter:
                stack.append(ana_str[0])
                ana_str = ana_str[1:]
            # j是stack中最上面终结符的下标
            if stack[-1] in self.terSymbol:
                j = len(stack) - 1
            else:
                j = len(stack) - 2
            # stack[j]是栈最上面的终结符,a是当前输入串的第一个字符（终结符
            a = ana_str[0]
            if stack[j] not in num or a not in num:
                #print("ERROR ----- ", stack[j])
                return False
            else:
                # 栈顶终结符优先级低于等于字符串第一个终结符
                if gra[num.index(stack[j]) + 1][num.index(a) + 1] == '<·' or gra[num.index(stack[j]) + 1][
                    num.index(a) + 1] == '=·':
                    stack.append(a)
                    # print("移进" + a)
                    if a == 'a':
                        digit_stack.append(digit_str[id1])
                        id1 += 1
                    ana_str = ana_str[1:]

                    if ana_str[0] in self.non_ter:
                        stack.append(ana_str[0])
                        ana_str = ana_str[1:]
                    j += 1
                    if stack[j] in self.non_ter:
                        j += 1
                    a = ana_str[0]
                if stack[j] not in num or a not in num:
                    print("ERROR")
                    return False
                else:
                    # 如果栈顶终结符优先级高于字符串第一个终结符
                    while gra[num.index(stack[j]) + 1][num.index(a) + 1] == '·>':
                        # 寻找最左素短语
                        str = []
                        if ana_str[0] in self.non_ter:
                            str.append(ana_str[0])
                            ana_str = ana_str[1:]
                        # 如果栈顶是非终结符
                        if stack[-1] in self.non_ter:
                            str.append(stack[-1])
                        while j >= 1:
                            # j是往下遍历的指针,b是减小之前的
                            # b记录当前栈顶非终结符，并将b加入最左素短语
                            b = stack[j]
                            str.append(b)
                            # 如果当前终结符的下一个是终结符，指向下一个，否则指向下下一个
                            if stack[j - 1] in self.terSymbol:
                                j -= 1
                            else:
                                str.append(stack[j - 1])
                                j -= 2
                            # 如果下一个终结符优先级小于当前终结符
                            if gra[num.index(stack[j]) + 1][num.index(b) + 1] == '<·':
                                break
                        str = str[::-1]
                        # 归约,str是最左素短语
                        if self.reduce(str, self.grammer) == True:
                            #print("将",str,"归约为N")
                            if len(str) != 1:
                                if str[1] == '=':
                                    str_list.append([count, str[1], digit_stack[-1], '_', 'T%s' % placeid])
                                    del digit_stack[len(digit_stack) - 1:]
                                    digit_stack.append('T%s' % placeid)
                                    count += 1
                                    placeid += 1
                                if str[0] == '!' or str[0] == '@': # !a @a
                                    str_list.append([count, str[0], digit_stack[-1], '_', 'T%s' % placeid])
                                    del digit_stack[len(digit_stack) - 1:]
                                    digit_stack.append('T%s' % placeid)
                                    count += 1
                                    placeid += 1
                                elif str[-1] != ')':
                                    # print(digit_stack, str[-1], str[1], str[-2])
                                    # print(count, str[1], digit_stack[-2], digit_stack[-1], 'T%s' % placeid)
                                    if str[1] == 'or':
                                        str_list.append([count, '||', digit_stack[-2], digit_stack[-1], 'T%s' % placeid])
                                    else:
                                        str_list.append([count, str[1], digit_stack[-2], digit_stack[-1], 'T%s' % placeid])
                                    del digit_stack[len(digit_stack) - 2:]
                                    digit_stack.append('T%s' % placeid)
                                    #print(digit_stack)
                                    count += 1
                                    placeid += 1
                            del stack[len(stack) - len(str):]
                            stack.append('N')  # 反正模糊归约，这个非终结符随便写个就行了8
                        else:
                            #print(stack)
                            print("归约失败")
                            return False
                    if gra[num.index(stack[j]) + 1][num.index(a) + 1] != '·>' \
                            and gra[num.index(stack[j]) + 1][num.index(a) + 1] != '=·' \
                            and gra[num.index(stack[j]) + 1][num.index(a) + 1] != '<·':
                        print("ERROR")
                        return False
                    # j已经指向栈顶第一个终结符
        #print('规约成功')
        #print('strlist',str_list)
        return [str_list, count, placeid] #四元式列表 接下来第几条四元式编号 T的编号


    #比较两个嵌套列表是否相等
    def cmp(self,SET1, SET2):
        i = 0
        while i < 26:
            if (operator.eq(SET1[i], SET2[i])) == False:
                return False
            else:
                i += 1
        return True

    def chushihua(self,grammer): # 传入文法
        # 循环求最终firstVT集
        first1 = copy.deepcopy(self.firstVT)
        for gr in grammer:
            self.first(gr)
        first2 = copy.deepcopy(self.firstVT)

        while not self.cmp(first1, first2):
            first1 = copy.deepcopy(self.firstVT)
            for gr in grammer:
                self.first(gr)
            first2 = copy.deepcopy(self.firstVT)

        #print("该文法的非终结符的firstVT集为：")
        # i = 0
        # for f in self.firstVT:
        #     if len(f) != 0:
        #         print('firstVT(' + self.non_ter[i] + '):', f)
        #     i += 1
        # print()

        # 循环求最终lastVT集
        last1 = copy.deepcopy(self.lastVT)
        for gr in grammer:
            self.last(gr)
        last2 = copy.deepcopy(self.lastVT)

        while not self.cmp(last1, last2):
            last1 = copy.deepcopy(self.lastVT)
            for gr in grammer:
                self.last(gr)
            last2 = copy.deepcopy(self.lastVT)

        # print("该文法的非终结符的lastVT集为：")
        # j = 0
        # for f in self.lastVT:
        #     if len(f) != 0:
        #         print('lastVT(' + self.non_ter[j] + '):', f)
        #     j += 1
        # print()

        num = []
        for gra_line in grammer:
            gra_line = gra_line.split()
            for gr in gra_line:
                if gr == '->':
                    flag = 0
                    continue
                elif gr in self.terSymbol and gr not in num:
                    num.append(gr)
        num.append('#') #将#添加至非终结符中
        # print('num',num)
        if self.table(grammer, num) != False:
            # print("该文法的优先关系表为：")
            gra = self.table(grammer, num)
            # for i in range(len(gra)):  # 控制行
            #     for j in range(len(gra[i])):  # 控制列
            #         print(gra[i][j], end='\t')
            #     print()
            # print()
        return num,gra


    def solve(self,count,placeid,ana_str,digit_str):#四元式编号 T变量编号 格式化字符串 数字字符串
            for i in range(len(ana_str) - 1):
                if ana_str[i] == '(' and ana_str[i + 1] == '-':
                    ana_str[i + 1] = '@'
            if ana_str[0] == '-':
                ana_str[0] = '@'
            print(ana_str)
            print("分析：",ana_str,digit_str)
            return self.master(count,placeid,ana_str, self.num,self.gra,digit_str)

# 正确的案例
# ss = Suanfufirst()
# ana_str = " - a + a or a"
# digit_str = ['a','1','1','4','5','2','b','c','8','9','2','b','c','8','9']
# ana_str = ana_str.split()
# print('ana_str',ana_str)
# print(ss.solve(0,0,ana_str,digit_str))# count t 字符串列表 数字列表

# [[[0, '@', 'a', '_', 'T0'], [1, '+', 'T0', '1', 'T1'], [2, '||', 'T1', '1', 'T2']], 3, 3]
# 问题排查 改正
# ss = Suanfufirst()
# ana_str = " a + a * ( - a )"
# digit_str = ['b','c','d']
# ana_str = ana_str.split()
# print('ana_str',ana_str)
# print(ss.solve(0,0,ana_str,digit_str))# count t 字符串列表 数字列表

