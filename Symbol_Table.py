'''
符号表的建立：
    遇见’,‘ ';'判断相关标志，对声明标志清零，并且填写符号表
'''
class CreateTableFlag:
    def __init__(self,Equal_Flag=0,value=None,type=None,name = None,Func_type_list=None,line = 0):
        self.Equal_Flag = 0 # 是否进行了赋值操作
        self.value = value # 变量常量值
        self.type =  type # 变量类型
        self.name = name #变量名
        self.Func_type_list = [] # 函数参数表
        self.ZK_Flag = 0
        self.line = 0

    def set_zero(self):
        self.type = None
        self.value = 0  # 变量常量值
        self.name = None  # 变量名
        self.Equal_Flag = 0  # 是否进行了赋值操作
        self.Func_type_list = []

    def set_zero1(self):
        self.value = 0  # 变量常量值
        self.Equal_Flag = 0  # 是否进行了赋值操作
        self.name = None  # 变量名
    def set_zero2(self): # 函数
        self.value = 0  # 变量常量值
        self.name = None  # 变量名
        self.Func_type_list = []

class node1: # 变量结点
    def __init__(self, type=None, name = None, value = None, scope = None,line = None):# 入口 变量类型 变量名 值 作用域
        self.address = None # 入口
        self.type = type
        self.name = name
        self.value = value
        self.scope = scope
        self.line = line
        self.n = None #下一个

#函数名是否先声明后定义
class node2:# 函数结点
    def __init__(self,type=None,name=None,paralist = None,line = None,paralist_name = None):#函数参数 返回类型 函数名  参数类型表
        self.address = None  # 函数入口
        self.parameter = 0 # 参数个数
        self.type = type # 函数类型
        self.name = name # 函数名字
        self.paralist = paralist # 参数列表
        self.paralist_name = paralist_name
        self.line = line
        self.n = None  # 下一个

# 链表实现函数符号表
class FunctionSymbolTable:
    def __init__(self):
        self.N = 0 # 变量表变量个数
        self.head = node2() #头结点
        self.iter = self.head
        self.text = ""
        super(FunctionSymbolTable, self).__init__()

    #声明检查 检查是否有该函数 不允许重复声明
    def get_func(self,funcname):
        item = self.head
        while item is not None:  # 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            if item.name == funcname:
                return true
            item = item.n
        return false

    #查找函数 并返回函数返回类型
    def get_func_type(self,name):
        item = self.head
        while item is not None:  # 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            if item.name == name:
                return item.type
            item = item.n
        return None #

    #检查函数调用 函数名 以及函数类型
    def check_function_call(self,funcname,funcargu_type): #函数名 实参 实参类型
        item = self.head
        while item is not None:
            if item.name == funcname[1]:
               if item.parameter!=len(funcargu_type):
                   return 'Warning: 第 %s 行 %s函数调用形参个数与声明不一致！\n' % (funcname[0],funcname[1])
               if item.paralist!=funcargu_type:
                   return 'Warning: 第 %s 行 %s函数调用形参类型与声明不一致！\n' % (funcname[0],funcname[1])
               return '' # 没有错误
            item = item.n
        return 'Warning: 第 %s 行 %s函数调用未声明！\n' % (funcname[0],funcname[1])


    # 检查函数定义
    def check_function_define(self,functon_information_list):
        funtype = functon_information_list[0]
        funcname = functon_information_list[1]
        func_xingcantypelist = functon_information_list[2]
        func_xingcannamelist = functon_information_list[3]
        line = functon_information_list[4]
        erro_information = "" #错误信息
        para_error = 0 #函数形参个数错误
        item = self.head
        while item is not None:  # 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            if item.name == funcname:
                if item.parameter!=len(func_xingcannamelist) and not para_error:
                    para_error = 1
                    erro_information += 'Warning: 第 %s 行 %s函数定义形参个数与声明不一致！\n' % (line,funcname)
                if item.paralist!=func_xingcantypelist and not para_error:
                    erro_information += 'Warning: 第 %s 行 %s函数定义形参类型与声明不一致！\n' % (line,funcname)
                break
            item = item.n
        if item == None:
            erro_information+='Warning:未声明 %s 函数！\n' % (funcname)
        return erro_information
    #　插入操作:先进行查找 如果链表中有该变量且作用域相同 则报错 反之 进行添加操作
    def put(self, node):
        if node.name in ['read','write']:
            return "Warning: 第 %s 行 函数名 %s 已声明函数！\n" % (node.line,node.name)
        item = self.head
        while item is not None:
            if item.name == node.name and item.paralist == node.paralist:# 参数列表是佛相同
                return "Warning: 第 %s 行 函数名 %s 不可重复声明函数！\n" % (node.line,node.name)
            item = item.n
        node.address = self.N
        #插入操作
        if self.head.name is None:# 头结点为空 头结点指向当前节点
            self.head = node
        else:
            node.n = self.head # 头结点不为空 头插法插入节点
            self.head = node
        self.N += 1
        return ""
    def lookAll(self):
        self.text = "函数符号表\n入口\t形参个数\t返回类型\t函数名\t形参类型列表\n"
        #print("函数符号表")
        #print("入口\t形参个数\t返回类型\t函数名\t形参类型列表")
        item = self.head
        while item is not None:  # 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            self.check(item)
            item = item.n
        return self.text
    def check(self,node):
        #if node == None:
            #print(None)
        # if isinstance(node, node1):
        #     print(node.address,node.parameter,node.type,node.name,node.value)
        # else:
        s = None
        if node.parameter != 0:
            s = ','.join(map(str, node.paralist))
        #print("%s\t%s\t%s\t%s\t%s" % (node.address, node.parameter, node.type, node.name, s))
        self.text+="%s\t%s\t%s\t%s\t%s\n" % (node.address, node.parameter, node.type, node.name, s)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter.n is not None:
            value = self.iter.value
            self.iter = self.iter.n
            return value
        else:
            self.iter = self.head
            raise StopIteration

    @property
    def size(self):
        return self.N


class VariableSymbolTable():# 记录常量以及变量表
    def __init__(self):
        self.N = 0 # 变量表变量个数
        self.M = 0 # 常量表变量个数
        self.head = node1() #变量表头结点
        self.head2 = node1() #常量表头结点
        self.iter = self.head
        self.text1 = ''
        super(VariableSymbolTable, self).__init__()

    #查找
    """
    先查找变量表 若变量表中不含有该变量，查找常量表，常量表中不含，则报错
    """
    def get(self, name, scope):
        item = self.head
        while item is not None:# 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            if item.name == name and item.scope in scope:
                return True
            item = item.n
        item = self.head2
        while item is not None:  # 常量名以及作用域相同
            if item.name == name and item.scope in scope:
                return True
            item = item.n
        return False

    def get_type(self,name,scope):
        item = self.head
        while item is not None:  # 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            if item.name == name and item.scope in scope:
                return item.type
            item = item.n
        item = self.head2
        while item is not None:  # 常量名以及作用域相同
            if item.name == name and item.scope in scope:
                return item.type
            item = item.n
        return None

    def if_constant(self,name,scope): #是否在常量表中
        item = self.head
        while item is not None:  # 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            if item.name == name and item.scope in scope:
                return False
            item = item.n
        item = self.head2
        while item is not None:  # 常量名以及作用域相同
            if item.name == name and item.scope in scope:
                return True
            item = item.n
        return False

    '''
    插入操作：
    1.先检查变量是否存在于常量表中，变量名及作用域
    2.检查是否存在于变量表
    3.若无，则根据flag进行插入操作
    '''
    def put(self, node, flag): # flag = 1 插入常量 为2插入变量
        item = self.head2
        while item is not None:
            if item.name == node.name and item.scope == node.scope: #变量名及作用域相同 芭比Q了
                return "Warning: 第 %s 行 %s 已声明常量 ！\n" % (node.line,node.name)
            item = item.n
        item = self.head
        while item is not None:
            if item.name == node.name and item.scope == node.scope: #变量名及作用域相同 芭比Q了
                return "Warning: 第 %s 行 %s 已声明变量 ！\n" % (node.line,node.name)
            item = item.n
        if flag == 1: # 插入常量
            node.address = self.M
            self.M += 1
            # 插入操作
            if self.head2.name is None:  # 头结点为空 头结点指向当前节点
                self.head2 = node
            else:
                node.n = self.head2  # 头结点不为空 头插法插入节点
                self.head2= node
        else:#即插入变量
            node.address = self.N
            self.N += 1
            #插入操作
            if self.head.name is None:# 头结点为空 头结点指向当前节点
                self.head = node
            else:
                node.n = self.head # 头结点不为空 头插法插入节点
                self.head = node
        return ""

    #查找 & 修改操作
    def modify(self,name,scope,value):
        item = self.head
        #查找操作
        while 1:
            while item is not None:

                if item.name == name and item.scope == scope:
                    item.value = value
                    #print(self.check(item))
                    return True
                item = item.n

            if len(scope)>1:#作用域逐层递减
                scope = scope[0:-2]
                item = self.head # 重新指向头结点
            else:
                #print("变量未声明!")
                return False
    def lookAll(self):
        self.text1 = "常量符号表\n"
        self.text1+="入口\t类型名\t常量名\t值\t作用域\n"
        item = self.head2
        while item is not None:  # 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            self.check(item)
            item = item.n
        self.text1 += "变量符号表\n"
        self.text1 += "入口\t类型名\t变量名\t值\t作用域\n"
        #print("变量符号表")
        #print("入口\t类型名\t变量名\t值\t作用域")
        item = self.head
        while item is not None:  # 变量名相同 作用域在其之上或者与其相同(长度小于或等于当前变量)
            self.check(item)
            item = item.n
        return self.text1

    def check(self,node):
        if node == None:
            return None
        #print("%s\t%s\t%s\t%s\t%s" % (node.address, node.type, node.name, node.value,node.scope))
        self.text1+="%s\t%s\t%s\t%s\t%s\n" % (node.address, node.type, node.name, node.value,node.scope)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter.n is not None:
            value = self.iter.value
            self.iter = self.iter.n
            return value
        else:
            self.iter = self.head
            raise StopIteration

    @property
    def size(self):
        return self.N



#测试
# if __name__ == '__main__':
#
#     sym = VariableSymbolTable()
#     node = node1(type = "int",name = 'a', scope='0')
#     node11 = node1(type = "int",name = 'b', scope='0')
#     node12 = node1(type="int", name='b', scope='0/1')
#     sym.put(node)
#     sym.put(node11)
#     sym.put(node12)
#     sym.get('a','0')
#     sym.modify('a','0',value=2)
#     sym.modify('b', '0/1/2', value=4)
#     sym.lookAll()

























