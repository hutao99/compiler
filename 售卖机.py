def error():
    print('投币错误请重新投币')

state=0
money=0
coin=[1,2,5]
while True:
    print("请选择矿泉水:\n 1、3块钱 2、4块钱 3、5块钱 ")
    num=x=int(input())
    if x==1:
        money=3
    elif x==2:
        money=4
    elif x==3:
        money=5
    else:
        print("选择错误")
        continue
    sum=0
    while True:
        x=int(input("请投入硬币:"))
        if x not in coin:
            error()
            continue
        sum+=x
        if state==0:
            if sum>=money:
                state=1
        if state==1:
            print("你得到一瓶%d块钱的矿泉水" % money)
            state=0
            break
    money = 0
