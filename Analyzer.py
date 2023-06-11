import ply.lex as lex


class Analyzer:
    def __init__(self):
        f = open('种别码.txt', 'r', encoding='utf-8')
        self.type = dict()
        self.record = []
        for i in f.readlines():
            cut = i.split()
            self.type[cut[0]] = int(cut[1])
        self.errors = []
        self.type[' '] = 305
        self.type['\n'] = 306

    def getColumn(self, string, index):
        col = 1
        for i in range(index, 0, -1):
            if string[i] == '\n':
                break
            col += 1
        return col

    def Lexical(self, string):
        index = [0, 1]
        assist = ['>', '<', '=', '!']
        if ord(string[index[0]]) == 65279:  # 去除utf-8标识符
            index[0] += 1
        while string[index[0]] != '\0':
            # print("%d,%d" % (index[0], index[1]))
            if string[index[0]] == ' ' or string[index[0]] == '\t' or string[index[0]] == '\r':
                index[0] += 1
                continue
            elif string[index[0]] == '\n':
                index[0] += 1
                index[1] += 1
            elif string[index[0]].isalpha() or string[index[0]] == '_':
                self.IdentifierOrKeyword(string, index)
            elif string[index[0]].isdigit():
                self.digit(string, index)
            elif string[index[0]] == "'":
                self.ischaracter(string, index)
            elif string[index[0]] == '"':
                self.isstring(string, index)
            elif string[index[0]] == '/':
                self.slash(string, index)
            elif string[index[0]] in assist:
                self.operator(string, index)
            elif string[index[0]] == '&' or string[index[0]] == '|':
                self.logic(string, index)
            elif string[index[0]] in self.type:
                self.record.append(
                    [string[index[0]], index[1], self.getColumn(string, index[0]), self.type[string[index[0]]]])
                index[0] += 1
            else:
                self.errors.append([index[1], self.getColumn(string, index[0]), '"%s"未识别字符' % string[index[0]]])
                index[0] += 1

    def IdentifierOrKeyword(self, string, index):  # 标识符和保留字
        start = index[0]
        index[0] += 1
        state = 1
        while state != 2:
            if string[index[0]].isalpha() or string[index[0]] == '_' or string[index[0]].isdigit():
                state = 1
                index[0] += 1
            else:
                state = 2
        word = string[start:index[0]]
        information = [word, index[1], self.getColumn(string, index[0] - 1)]
        if word in self.type:
            information.append(self.type[word])
        else:
            information.append(700)
        self.record.append(information)

    def digit(self, string, index):
        start = index[0]
        state = 0
        typenum = 0
        while True:
            # print(state)
            if state == 0:
                if string[index[0]] != '0':
                    state = 1
                else:
                    state = 3
            elif state == 1:
                if string[index[0]].isdigit():
                    index[0] += 1
                    continue
                elif string[index[0]] == 'E' or string[index[0]] == 'e':
                    state = 10
                elif string[index[0]] in self.type and ((self.type[string[index[0]]] >= 301 and self.type[string[index[0]]] <= 306) or (self.type[string[index[0]]] >= 201 and self.type[string[index[0]]] <= 219)):
                    # state = 15
                    typenum = 400
                    break
                elif string[index[0]] == '&' or string[index[0]] == '|':
                    typenum = 400
                    break
                elif string[index[0]] == '.':
                    state = 8
                else:
                    state = 16
                    # 出错
                    break
            elif state == 3:
                if string[index[0]] >= '0' and string[index[0]] <= '7':
                    index[0] += 1
                    continue
                elif string[index[0]] == 'X' or string[index[0]] == 'x':
                    state = 5
                elif string[index[0]] == '.':
                    state = 8
                elif string[index[0]] in self.type and ((self.type[string[index[0]]] >= 301 and self.type[string[index[0]]] <= 306) or (self.type[string[index[0]]] >= 201 and self.type[string[index[0]]] <= 219)):
                    typenum = 400  # 7进制整数
                    # state = 4
                    break
                else:
                    state = 16
                    break
            elif state == 5:
                if (ord(string[index[0]]) >= ord('a') and ord(string[index[0]]) <= ord('f')) or (ord(string[index[0]]) >= ord('A') and ord(string[index[0]]) <= ord('F')) or string[index[0]].isdigit():
                    state = 6
                else:
                    state = 16  # 出错
                    break
            elif state == 6:
                if (ord(string[index[0]]) >= ord('a') and ord(string[index[0]]) <= ord('f')) or (ord(string[index[0]]) >= ord('A') and ord(string[index[0]]) <= ord('F')) or string[index[0]].isdigit():
                    index[0] += 1
                    continue
                elif string[index[0]] in self.type and ((self.type[string[index[0]]] >= 301 and self.type[string[index[0]]] <= 306) or (self.type[string[index[0]]] >= 201 and self.type[string[index[0]]] <= 219)):
                    # state=7
                    typenum = 400  # 16进制整数
                    break
                else:
                    state = 16  # 出错
                    break
            elif state == 8:
                if string[index[0]].isdigit():
                    state = 9
                else:
                    state = 16
                    # 出错
                    break
            elif state == 9:
                if string[index[0]].isdigit():
                    index[0] += 1
                    continue
                elif string[index[0]] == 'E' or string[index[0]] == 'e':
                    state = 10
                elif string[index[0]] in self.type and ((self.type[string[index[0]]] >= 301 and self.type[string[index[0]]] <= 306) or (self.type[string[index[0]]] >= 201 and self.type[string[index[0]]] <= 219)):
                    typenum = 800
                    # state=15
                    break
                else:
                    state = 16
                    # 出错
                    break
            elif state == 10:
                if string[index[0]] == '+' or string[index[0]] == '-':
                    state = 11
                elif string[index[0]].isdigit():
                    state = 12
                else:
                    state = 16
                    # 出错
                    break
            elif state == 11:
                if string[index[0]].isdigit():
                    state = 12
                else:  # 出错
                    state = 16
                    break
            elif state == 12:
                if string[index[0]].isdigit():
                    index[0] += 1
                    continue
                elif string[index[0]] in self.type and ((self.type[string[index[0]]] >= 301 and self.type[string[index[0]]] <= 306) or (self.type[string[index[0]]] >= 201 and self.type[string[index[0]]] <= 219)):
                    typenum = 900
                    break
                else:
                    state = 16
                    # 出错
                    break
            index[0] += 1
        word = string[start:index[0]]
        if state == 16:
            word = string[start:index[0]]
            self.errors.append([index[1], self.getColumn(string, index[0]), word+'加后一个字符不构成数字'])
            return
        information = [word, index[1], self.getColumn(string, index[0] - 1), typenum]
        self.record.append(information)

    def ischaracter(self, string, index):  # 读入单个字符
        start = index[0]
        index[0] += 1
        state = 1
        c = ['n', 't', 'r', '\'', '\\']
        while True:
            cha = string[index[0]]
            if state == 1:
                if cha == '\'':
                    state = 2
                    break
                elif cha == '\n' or cha == '\0':
                    state = 3
                    break
                elif cha == '\\':
                    state = 4
                else:
                    state = 5
            elif state == 5:
                if cha == '\'':
                    state = 6
                    index[0] += 1
                else:
                    # state=7
                    state = 3
                break
            elif state == 4:
                if cha in c:
                    state = 9
                else:
                    state = 8
                    break
            elif state == 9:
                if cha == '\'':
                    state = 10
                    index[0] += 1
                else:
                    state = 11
                break
            index[0] += 1
        word = string[start:index[0]]
        errormessage = ''
        if state == 3:
            errormessage = '缺少右单引号'
        elif state == 2 or state == 7 or state == 11:
            errormessage = '单引号内至少包含一个字符'
        elif state == 8:
            errormessage = '没有这个转义字符'
        if errormessage == '':
            self.record.append([word[1:-1], index[1], self.getColumn(string, index[0]), 500])
        else:
            self.errors.append([index[1], self.getColumn(string, index[0]), errormessage])

    def isstring(self, string, index):
        state = 1
        start = index[0]
        index[0] += 1
        while True:
            cha = string[index[0]]
            if state == 1:
                if cha == '\\':
                    state = 2
                elif cha == '\n' or cha == '\0':
                    state = 3
                    break
                elif cha == '"':
                    state = 4
                    index[0] += 1
                    break
            elif state == 2:
                if cha == '\n' or cha == '\0':
                    state = 3
                    break
                else:
                    state = 1
            index[0] += 1
        word = string[start:index[0]]
        if state == 3:
            errormessage = '缺少右引号'
            self.errors.append([index[1], self.getColumn(string, index[0]-1), errormessage])
        else:
            self.record.append([word[1:-1], index[1], self.getColumn(string, index[0]-1), 600])

    def slash(self, string, index):
        state = 1
        # start=index[0]
        index[0] += 1
        cha = string[index[0]]
        if cha == '/':
            index[0] += 1
            while string[index[0]] != '\n' and string[index[0]] != '\0':
                index[0] += 1
            return
        elif cha == '*':
            state = 3
        else:
            self.record.append(['/', index[1], self.getColumn(string, index[0]), self.type['/']])
            return
        index[0] += 1
        while string[index[0]] != '\0':
            if string[index[0]] == '\n':
                index[1] += 1
            cha = string[index[0]]
            if state == 3:
                if cha != '*':
                    pass
                else:
                    state = 4
            elif state == 4:
                if cha != '/':
                    state = 3
                else:
                    # state=5
                    break
            index[0] += 1
        if string[index[0]] == '\0':
            self.errors.append([index[1], self.getColumn(string, index[0] - 1), '注释未闭合'])
        else:
            index[0] += 1

    def operator(self, string, index):
        index[0] += 1
        if string[index[0]] == '=':
            c = string[index[0]-1:index[0]+1]
            index[0] += 1
        else:
            c = string[index[0] - 1:index[0]]
        self.record.append([c, index[1], self.getColumn(string, index[0] - 1), self.type[c]])

    def logic(self, string, index):
        e = index[0]
        if string[e] == '&' and string[e+1] == '&':
            self.record.append(['&&', index[1], self.getColumn(string, index[0]), self.type['&&']])
            index[0] += 2
        elif string[e] == '|' and string[e+1] == '|':
            self.record.append(['||', index[1], self.getColumn(string, index[0]), self.type['||']])
            index[0] += 2
        elif string[e] == '&':
            self.record.append(['&', index[1], self.getColumn(string, index[0]), self.type['&']])
            index[0] += 1
        else:
            self.errors.append([index[1], self.getColumn(string, index[0]), '后面需跟'+string[e]])
            index[0] += 1


def typefile(address):
    f = open(address, 'r', encoding='utf-8')
    ty = dict()  # 种别码
    for i in f.readlines():
        a = i.split()
        ty[a[0]] = a[1]
    f.close()
    return ty


class AnalyzerLex:
    tokens = (
        'keyword',  # 关键词
        'Boundary',  # 界符
        'integer',  # 整数
        'character',  # 字符
        'string',  # 字符串
        'identifier',  # 标识符
        'float',  # 实数
        'operator',  # 运算符
    )

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.ty = typefile("种别码.txt")
        self.error = []

    states = (
        ('multicomment', 'exclusive'),  # 多行注释
    )

    def t_START(self, t):  # 处理注释的状态开始
        r'\/\*'
        # 切换状态到 comment
        t.lexer.push_state('multicomment')

    def t_multicomment_END(self, t):  # 注释结尾
        r'\*\/'
        # 切换状态回到默认状态
        t.lexer.pop_state()

    t_multicomment_ignore = '.'

    def t_multicomment_line(self, t):  # 换行
        r'\n'
        t.lexer.lineno += 1

    def t_multicomment_error(self, t):
        t.lexer.skip(1)

    def t_multicomment_eof(self, t):  # 注释不闭合
        self.error.append(
            [t.lexer.lineno-1, self.find_column(t.lexer.lexdata, t), '注释未闭合'])
        t.lexer.pop_state()

    # 字符处理
    def t_character(self, t):
        r'\'.*\''
        t.value = t.value[1:-1]
        return t

    def t_character_error1(self, t):
        r'\'[^\n\']*\n'
        self.error.append(
            [t.lexer.lineno, self.find_column(t.lexer.lexdata, t), '缺少右单引号'])
        t.lexer.lineno += 1

    # 字符串处理
    def t_string(self, t):
        r'\".*\"'
        t.value = t.value[1:-1]
        return t

    def t_string_error1(self, t):
        r'\"[^\n\"]*\n'
        self.error.append(
            [t.lexer.lineno, self.find_column(t.lexer.lexdata, t), '缺少右引号'])
        t.lexer.lineno += 1
    ##############################

    def t_lineComment(self, t):  # 单行注释
        r'\/\/.*'
        pass

    def t_identifier(self, t):  # 关键词和标识符
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value in self.ty:
            t.type = 'keyword'
        return t

    def t_Boundary(self, t):  # 界符
        r'[{};,]'
        return t

    # r'(0(x|X)[0-9a-fA-F][0-9a-fA-F]*)|([1-9]\d*)|(0[0-7]*)'
    def t_integer_hex(self, t):  # 十六进制
        r'0x[0-9a-fA-F][0-9a-fA-F]*'
        t.type = 'integer'
        return t

    def t_exponent(self, t):  # 指数
        r'\d+\.\d+[Ee]([+-]\d|\d)\d*'
        t.type = 'float'
        return t

    def t_float(self, t):  # 小数
        r'\d+\.\d+'
        t.type = 'float'
        return t

    def t_integer(self, t):  # 十进制
        r'[1-9][0-9]*|0'
        return t

    def t_integer_oct(self, t):  # 八进制
        r'0[0-7][1-7]*'
        t.type = 'integer'
        return t

    def t_operator_1(self, t):
        r'<=|>=|==|!=|&&|\|\|'
        t.type = 'operator'
        return t

    def t_operator_2(self, t):
        r'[=+-/%!.()*><&|]|\[|\]'
        t.type = 'operator'
        return t

    def find_column(self, input, token):  # 列
        last_cr = input.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    t_ignore = ' \t\r'

    def t_error(self, t):  # 不识别字符处理
        self.error.append([t.lexer.lineno, self.find_column(
            t.lexer.lexdata, t), '"%s"不识别字符' % t.value[0]])
        t.lexer.skip(1)

    def t_newline(self, t):  # 换行处理
        r'\n'
        t.lexer.lineno += len(t.value)

    def input(self, data):
        return self.lexer.input(data)

    # 定义 Token 函数
    def token(self):
        return self.lexer.token()
