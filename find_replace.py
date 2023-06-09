# 定义需要替换的单词和对应的值
replace_dict = {'A1':"程序",'A2':'声明语句','A3':'复合语句','A4':'函数块','A5':'函数定义','A6':'函数类型','A7':'标识符','A8':'函数定义形参列表',
             'B1':'函数定义形参','B2':'变量类型','C1':'语句','C2':'执行语句','C3':'值声明','C4':'函数声明','C5':'常量声明','C6':'变量声明','C7':'常量类型','C8':'常量声明表','C9':'常量',
             'D1':'变量声明表','D2':'单变量声明','D3':'变量','D4':'表达式','D5':'函数声明形参列表','D6':'函数声明形参','D7':'数据处理语句','D8':'控制语句',
             'E1':'赋值语句','E2':'函数调用语句','E3':'赋值表达式','E4':'函数调用','E5':'语句表',
             'F1':'关系表达式','F2':'算术表达式','F3':'关系运算符','F4':'布尔表达式','F5':'布尔项','F6':'布尔因子',
             'G1':'项','G2':'因子','G3':'常量','G4':'变量','G5':'数值型常量','G6':'字符型常量','H1':'实参列表','H2':'实参',
             'I1':'if语句','I2':'for语句','I3':'while语句','I4':'dowhile语句','I5':'return语句','J6':'break语句','J7':'continue语句'}

# 打开需要替换的文档并读取内容
with open('文法.txt', 'r') as f:
    content = f.read()

# 遍历字典中的每个键值对，将文档中的所有出现该键的地方替换为对应的值
for key, value in replace_dict.items():
    content = content.replace(key, value)

# 将替换后的文本写入到原始文档中或者新建一个文档保存
with open('文法(详细).txt', 'w') as f:
    f.write(content)
