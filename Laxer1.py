import chardet


class wordnode:  # 保存单词 行号 种别码
    def __init__(self):
        self.word = ""
        self.pos = 0
        self.id = 0


class LexicalAnalysis():
    def __init__(self, text):
        self.text = text
        self.text_len = len(text)
        self.wordline = 1  # 从第一行开始
        self.wordstr = "{}\t{}\t{}\t\n".format("行号", "单词", "种别码")
        self.errorlist = ""
        self.wordlist = []
        self.idx = 0
        self.stack_Parentheses = []  # 检测小括号是否配对
        self.stack_Middle_brackets = []  # 检测中括号是否配对
        self.stack_Curly_brackets = []  # 检测大括号是否配对
        self.check_parentheses_time = 0
        self.check_Middle_brackets = 0
        self.check_Curly_brackets = 0
        self.readFile("keyword.txt", "c语言种别码.txt")
        self.Type = {"int", "float", "char", "double", "void", "long", "unsigned", "string"}
        self.previous = ""
        self.fu_flag = [' ', '\n', '\b', '\t', '=', '(']
        self.other_token = ['{', '}', ';', ',', '(', ')', '[',
                            ']', '!', '*', '/', '%', '+', '-',
                            '<', '<=', '>', '>=', '==', '!=', '&&',
                            '||', '=', '.', '&', '|', '*=', '/=',
                            '+=', '-=', '++', '--']
        self.jielist = ['\n', '\b', '\t', ' ', ',', ';', ']', '}', ')', '=']
        self.textCheck()

    # 读入种别码到字典中 "标识符 种别码"形式
    def readFile(self, file1, file2):
        self.keyword_dist = {}  # 关键字
        self.id_list = {}  # 标识符 变量 数字
        fopen = open(file1)
        for line in fopen.readlines():
            line = line.replace("\n", "")
            sample = line.split(' ')
            self.keyword_dist[sample[0]] = sample[1]
        fopen = open(file2, encoding='utf-8')
        for line in fopen.readlines():
            line = line.replace("\n", "")
            sample = line.split(' ')
            self.id_list[sample[0]] = sample[1]

    def textCheck(self):
        # 输出文本
        # print(self.text)
        while self.idx < self.text_len:
            ch = self.text[self.idx]
            # 标识符判断
            if ch.isalpha() or ch == '_':
                self.identifier_Check()
            # 整数判断
            elif ch.isdigit():
                self.isdigit_Check()
            elif ch == '/':
                self.zhushi_Check()
            elif ch == '\'':
                self.dan_Check()
            elif ch == '"':
                self.shuang_Check()
            elif ch in ['&', '|']:
                self.yufei_Check()
            elif ch in ['+', '-', '*', '%', '<', '>', '=', '^', '*', '!']:
                self.pan_Check()
            elif ch in ['(', ')', '[', ']', '{', '}', ',', ';', '#']:
                self.yunandjie_Check()
            elif ch == '\n':
                self.wordline += 1
                self.previous = ch
                self.idx += 1
            elif ch == ' ' or ch == '\b' or ch == '\t' or ch == '\r':
                self.previous = ch
                self.idx += 1
            else:
                self.error(self.idx)
                self.idx += 1

    # 识别关键字
    def identifier_Check(self):
        state, start = self.init_start()
        while state != 2:
            ch = self.text[self.idx]
            if state == 0:
                if ch.isalpha() or ch == "_":
                    self.idx += 1
                    state = 1
                else:
                    self.error()
                    break
            elif state == 1:
                if ch.isalpha() or ch.isdigit() or ch == "_":
                    self.idx += 1
                else:
                    state = 2
            self.previous = ch
        node = wordnode()  # 保存关键字
        node.word = self.text[start:self.idx]  # 截取单词
        node.pos = self.wordline
        # 关键字 or 标识符
        if self.keyword_dist.get(node.word) is None:
            node.id = self.id_list.get("标识符")
        else:
            node.id = self.keyword_dist.get(node.word)
        # node.id 在文件中搜索种别码
        self.wordlist.append(node)
        # 回退一个符号

    # 识别数字
    def isdigit_Check(self):
        state, start = self.init_start()
        while self.idx < self.text_len:
            ch = self.text[self.idx]
            if state == 0:
                if ch == '0':
                    state = 10
                elif ch.isdigit():
                    state = 1
                self.idx += 1
            elif state == 1:
                if ch.isdigit():
                    self.idx += 1
                elif ch == '.':
                    state = 2
                    self.idx += 1
                elif ch in self.jielist:
                    state = 9
                elif ch.isalpha():
                    self.error(start)
                    self.idx += 1
                    return
                else:
                    self.save_word(start, "整数")
                    return
            elif state == 2:
                if ch.isdigit():
                    state = 3
                    self.idx += 1
                else:
                    self.idx -= 1
                    self.error(start)
                    self.idx += 1
                    return
            elif state == 3:
                if ch.isdigit():
                    self.idx += 1
                elif ch == 'E' or ch == 'e':
                    state = 4
                    self.idx += 1
                elif ch in self.jielist:
                    state = 8
                else:
                    self.error(start)
                    self.idx += 1
                    return
            elif state == 4:
                if ch == '+' or ch == '-':
                    state = 5
                    self.idx += 1
                elif ch.isdigit():
                    state = 6
                    self.idx += 1
                else:
                    self.error(start)
                    return
            elif state == 5:
                if ch.isdigit():
                    state = 6
                    self.idx += 1
                else:
                    self.error(start)
                    return
            elif state == 6:
                if ch.isdigit():
                    self.idx += 1
                elif ch in self.jielist:
                    state = 7
                else:
                    self.error(start)
                    self.idx += 1
                    return
            elif state == 7:
                self.save_word(start, "指数")
                return
            elif state == 8:
                self.save_word(start, "小数")
                return
            elif state == 9:
                self.save_word(start, "整数")
                return
            elif state == 10:
                if '1' <= ch <= '7':
                    state = 11
                    self.idx += 1
                elif ch == 'x' or ch == 'X':
                    state = 13
                    self.idx += 1
                elif ch == '.':
                    state = 2
                    self.idx += 1
                elif ch in self.jielist:
                    state = 16
                elif ch == '0':
                    state = 17
                    self.idx += 1
                else:
                    self.save_word(start, "整数")
                    return
            elif state == 11:
                if '0' <= ch <= '7':
                    self.idx += 1
                elif ch in [' ', '\n', '\b', '\t']:
                    state = 12
                else:
                    self.error(start)
                    self.idx += 1
                    return
            elif state == 12:
                self.save_word(start, "八进制")
                self.idx -= 1
                return
            elif state == 13:
                if ('0' <= ch <= '9') or ('a' <= ch <= 'f') or ('A' <= ch <= 'F'):
                    state = 14
                    self.idx += 1
                else:
                    self.error(start)
                    return
            elif state == 14:
                if ('0' <= ch <= '9') or ('a' <= ch <= 'f') or ('A' <= ch <= 'F'):
                    self.idx += 1
                elif ch in self.jielist:
                    state = 15
                else:
                    self.error(start)
                    return
            elif state == 15:
                self.save_word(start, "十六进制")
                return
            elif state == 16:
                self.save_word(start, "整数")
                return
            elif state == 17:
                if ch == '0':
                    self.idx += 1
                elif ch == '.':
                    state = 2
                    self.idx += 1
                else:
                    self.error(start)
                    self.idx += 1
                    return
            self.previous = ch

    # 识别注释
    def zhushi_Check(self):
        state, start = self.init_start()
        while self.idx < self.text_len:
            ch = self.text[self.idx]
            if state == 0:
                if ch == '/':  # 单行注释
                    state = 1
                    self.idx += 1
            elif state == 1:
                if ch == '/':
                    state = 2
                elif ch == '*':
                    state = 4
                else:
                    state = 3
                self.idx += 1
            # 终态:单行注释
            elif state == 2:
                while ch != '\n' and (self.idx + 1 < self.text_len):
                    self.idx += 1
                    ch = self.text[self.idx]
                    if ch == '\n':
                        self.wordline += 1
                self.idx += 1
                break
            # 终态:除号
            elif state == 3:
                self.idx -= 1
                self.save_word(start, '/')
                return
            elif state == 4:
                if ch != '*':
                    if ch == '\n':
                        self.wordline += 1
                elif ch == '*':
                    state = 5
                self.idx += 1
            elif state == 5:
                if ch != '/':
                    state = 4
                elif ch == '/':
                    state = 6
                self.idx += 1
            # 终态:多行注释
            elif state == 6:
                return
            else:
                # 如果出现/*没有收尾情况 报错
                self.error(start)
            self.previous = ch

    # 识别单引号
    def dan_Check(self):
        state, start = self.init_start()
        while self.idx < self.text_len:
            ch = self.text[self.idx]
            if state == 0:
                if ch == '\'':
                    state = 1
                    self.idx += 1
            elif state == 1:
                if ch == '\'':
                    self.error(start)
                    self.idx += 1
                    return
                elif ch == '\\' or ch == '%':
                    state = 4
                else:
                    state = 2
                self.idx += 1
            elif state == 2:
                if ch != '\'':
                    self.error(start)
                    return
                else:
                    self.idx += 1
                    state = 3
            elif state == 3:
                self.save_word(start, "字符")
                break
            elif state == 4:
                if ch in ['\\', '%', '\'', 'n', 'r', 't', '"']:
                    state = 5
                    self.idx += 1
                else:
                    self.error(start)
                    return
            elif state == 5:
                if ch == '\'':
                    state = 3
                else:
                    self.error(start)
                    break
            self.previous = ch

    def shuang_Check(self):
        state, start = self.init_start()
        while self.idx < self.text_len:
            ch = self.text[self.idx]
            if state == 0:
                if ch == '"':
                    state = 1
                    self.idx += 1
            elif state == 1:
                if ch == '"':
                    state = 2
                    self.idx += 1
                elif ch == '\n':
                    self.idx -= 1
                    self.error(start)
                    self.idx += 1
                    return
                else:
                    self.idx += 1
            elif state == 2:
                self.save_word(start, "字符串")
                return
            self.previous = ch

    def yufei_Check(self):
        state, start = self.init_start()
        while self.idx < self.text_len:
            ch = self.text[self.idx]
            if state == 0:
                if ch == '&' or ch == '|':
                    pre = ch
                    state = 1
                    self.idx += 1
            elif state == 1:
                if pre == ch:
                    state = 2
                    self.idx += 1
                elif pre != ch and (ch in ['&', '|']):
                    self.error(start)
                    self.idx += 1
                    break
                else:
                    # '&' or '|'
                    self.save_word(start, pre)
                    return
            elif state == 2:
                if ch == '&':
                    self.save_word(start, '&&')
                else:
                    self.save_word(start, '||')
                return
            self.previous = ch

    def pan_Check(self):
        state, start = self.init_start()
        while self.idx < self.text_len:
            ch = self.text[self.idx]
            if state == 0:
                if ch in ['+', '%', '<', '>', '=', '^', '*', '!']:
                    state = 1
                    pre = ch
                    self.idx += 1
                elif ch == '-' and self.previous in self.fu_flag:
                    print('000000000111111')
                    state = 8
                    pre = ch
                    self.idx += 1
                elif ch == '-' and self.previous not in self.fu_flag:
                    state = 1
                    pre = ch
                    self.idx += 1
            elif state == 1:
                if pre == '=' and ch == '-':
                    self.save_word(start, pre)
                    start=self.idx
                    state = 8
                    self.idx += 1
                elif ch == '=':
                    state = 2
                    self.idx += 1
                elif ch == pre:
                    if ch in ['+', '-']:
                        pre = ch
                        state = 3
                    elif ch in ['<', '>']:
                        pre = ch
                        state = 4
                    self.idx += 1
                elif pre == '!' and ch != '=':
                    self.error(start)
                    self.idx += 1
                    break
                else:
                    state = 5
            elif state == 2:
                if ch == '=':
                    self.error(start)
                    self.idx += 1
                    break
                else:
                    self.save_word(start, pre + '=')
                    return
            elif state == 3:
                self.save_word(start, pre + pre)
                return
            elif state == 4:
                if ch == '=':
                    state = 7
                    self.idx += 1
                else:
                    state = 6
            elif state == 5:
                self.save_word(start, pre)
                return
            elif state == 6:
                self.save_word(start, pre)
                return
            elif state == 7:
                self.save_word(start, pre + pre + '=')
                return
            elif state == 8:
                if ch.isdigit():
                    print('-------')
                    state = 8
                    self.idx += 1
                else:
                    self.save_word(start, "负数")
                    return
            self.previous = ch
            print(self.previous)

    def check_parentheses(self, text):
        stack = []
        for char in text:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack

    def check_Middle_brackets__(self, text):
        stack = []
        for char in text:
            if char == '[':
                stack.append(char)
            elif char == ']':
                if not stack:
                    return False
                stack.pop()
        return not stack

    def check_Curly_brackets__(self, text):
        stack = []
        for char in text:
            if char == '{':
                stack.append(char)
            elif char == '}':
                if not stack:
                    return False
                stack.pop()
        return not stack

    def yunandjie_Check(self):
        start = self.idx
        ch = self.text[self.idx]
        self.previous = ch
        if ch == '(' and self.check_parentheses_time == 0:
            ts = self.check_parentheses(self.text[self.idx:])
            self.check_parentheses_time += 1
            # print(ts)
            if not ts:
                st = "Error: 小括号不匹配\n"
                self.errorlist += st
        elif ch == '[' and self.check_Middle_brackets == 0:
            ts = self.check_Middle_brackets__(self.text[self.idx:])
            self.check_Middle_brackets += 1
            # print(ts)
            if not ts:
                st = "Error: 中括号不匹配\n"
                self.errorlist += st
        elif ch == '{' and self.check_Curly_brackets == 0:
            ts = self.check_Curly_brackets__(self.text[self.idx:])
            self.check_Curly_brackets += 1
            # print(ts)
            if not ts:
                st = "Error: 大括号不匹配\n"
                self.errorlist += st

        self.idx += 1
        self.save_word(start, ch)

    def error(self, start):
        ch = self.text[self.idx]
        while ch not in ['\n', '\t', '\b', ' ']:
            self.idx += 1
            if self.idx < self.text_len:
                ch = self.text[self.idx]
            else:
                break
        str = "Error: 第{}行出现错误 \"{}\"\n".format(self.wordline, self.text[start:self.idx])
        self.errorlist += str

    def save_word(self, start, name):  # 开始位置 以及 识别的类别
        node = wordnode()
        node.word = self.text[start:self.idx]
        if node.word.strip() == "||":
            node.word = "or"
        node.pos = self.wordline
        node.id = self.id_list.get(name)
        self.wordlist.append(node)

    def init_start(self):
        state = 0
        start = self.idx  # 记录开始索引 以便字符串切片
        return state, start

    def print_out(self):
        lbword = []
        for i in self.wordlist:
            lbword.append([i.pos, i.word, i.id])
            str = "{}\t{}\t{}\t\n".format(i.pos, i.word, i.id)
            self.wordstr += str
        # print('词法分析:', lbword)
        return self.wordstr, self.errorlist, lbword


# coding=utf-8
def check_charset(file_path):
    import chardet
    with open(file_path, "rb") as f:
        data = f.read(1000)
        charset = chardet.detect(data)['encoding']
    return charset

# filename = r'全部测试程序\01编译器测试用例\test00.txt'
# filename = 'D:\pythonProject\pythonProject\负数测试.txt'
# with open(filename, encoding=check_charset(filename)) as f:
#     text = f.read()
#     a = LexicalAnalysis(text)  # 读入文章
#     c, d, e = a.print_out()
#     print(c)
#     print(d)
#     print(e)
