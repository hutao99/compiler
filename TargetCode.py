last = '''read:	push bp
	mov bp,sp
	mov bx,offset _msg_s
	call _print
	mov bx,offset _buff_s
	mov di,0
_r_lp_1:	mov ah,1
	int 21h
	cmp al,0dh
	je _r_brk_1
	mov ds:[bx+di],al
	inc di
	jmp short _r_lp_1
_r_brk_1:	mov ah,2
	mov dl,0ah
	int 21h
	mov ax,0
	mov si,0
	mov cx,10
_r_lp_2:	mov dl,ds:[bx+si]
	cmp dl,30h
	jb _r_brk_2
	cmp dl,39h
	ja _r_brk_2
	sub dl,30h
	mov ds:[bx+si],dl
	mul cx
	mov dl,ds:[bx+si]
	mov dh,0
	add ax,dx
	inc si
	jmp short _r_lp_2
_r_brk_2:	mov cx,di
	mov si,0
_r_lp_3:	mov byte ptr ds:[bx+si],0
	loop _r_lp_3
	mov sp,bp
	pop bp
	ret

write:	push bp
	mov bp,sp
	mov bx,offset _msg_p
	call _print
	mov ax,ss:[bp+4]
	mov bx,10
	mov cx,0
_w_lp_1:	mov dx,0
	div bx
	push dx
	inc cx
	cmp ax,0
	jne _w_lp_1
	mov di ,offset _buff_p
_w_lp_2:	pop ax
	add ax,30h
	mov ds:[di],al
	inc di
	loop _w_lp_2
	mov dx,offset _buff_p
	mov ah,09h
	int 21h
	mov cx,di
	sub cx,offset _buff_p
	mov di,offset _buff_p
_w_lp_3:	mov al,24h
	mov ds:[di],al
	inc di
	loop _w_lp_3
	mov ax,di
	sub ax,offset _buff_p
	mov sp,bp
	pop bp
	ret 2
_print:	mov si,0
	mov di,offset _buff_p
_p_lp_1:	mov al,ds:[bx+si]
	cmp al,0
	je _p_brk_1
	mov ds:[di],al
	inc si
	inc di
	jmp short _p_lp_1
_p_brk_1:	mov dx,offset _buff_p
	mov ah,09h
	int 21h
	mov cx,si
	mov di,offset _buff_p
_p_lp_2:	mov al,24h
	mov ds:[di],al
	inc di
	loop _p_lp_2
	ret
code ends
    end start
'''
first = '''assume cs:code,ds:data,ss:stack,es:extended

extended segment

	db 1024 dup (0)

extended ends

stack segment

	db 1024 dup (0)

stack ends
data segment

	_buff_p db 256 dup (24h)

	_buff_s db 256 dup (0)

	_msg_p db 0ah,'Output:',0

	_msg_s db 0ah,'Input:',0
'''

from LR import CLRParser


import Analyzer


class TargetCode:

    def __init__(self):
        self.code = ''

    def GetTargetCode(self, code_list, var, con, fun):
        self.code += first
        for i in range(len(code_list)):
            print(str(i)+':'+str(code_list[i]))
        identifier = dict()
        for i in var:
            for j in var[i]:
                if j.scope + ' ' + i not in identifier:
                    identifier[j.scope + ' ' + i] = 0
                    self.code += '    _%s dw ?\n' % i
                else:
                    identifier[j.scope + ' ' + i] += 1
                    self.code += '    _%s dw ?\n' % (i+str(identifier[j.scope + ' ' + i]))
        for i in con:
            for j in var[i]:
                if j.scope + ' ' + i not in identifier:
                    identifier[j.scope + ' ' + i] = 0
                    self.code += '    _%s dw ?\n' % i
                else:
                    identifier[j.scope + ' ' + i] += 1
                    self.code += '    _%s dw ?\n' % (i+str(identifier[j.scope + ' ' + i]))
        for i in code_list:
            for j in range(1, 4):
                print(i[j])
                if i[j] in con or i[j] in var:
                    i[j] = '_'+i[j]
                elif not isinstance(i[j], int) and len(i[j]) > 1 and i[j][0] == '-' and (i[j][1:] in con or i[j][1:] in var):
                    i[j] = '-' + '_' + i[j][1:]

        self.code += 'data ends\n'
        self.code += 'code segment\n'
        self.code += 'start:  mov ax, data\n    mov ds, ax\n'
        length = len(code_list)
        index = 0
        flag = 0
        flag1 = True
        bp_index = 2
        for i in range(length):
            self.code += '_' + str(index) + ':\n'
            if code_list[i][0] == '=':
                if code_list[i][1].isdigit():
                    self.code += '    mov %s, %s\n' % (code_list[i][3], code_list[i][1])
                elif code_list[i][1][0] != '$' and code_list[i][1] != 'return_value':
                    if code_list[i][1][0] != '-':
                        self.code += '    mov ax, %s\n' % code_list[i][1]
                        self.code += '    mov %s, ax\n' % code_list[i][3]
                    else:
                        self.code += '    mov ax, %s\n' % code_list[i][1][1:]
                        self.code += '    not ax\n'
                        self.code += '    add ax, 1\n'
                        self.code += '    mov %s, ax\n' % code_list[i][3]
                else:
                    self.code += '    pop ax\n'
                    self.code += '    mov %s, ax\n' % code_list[i][3]
                    flag -= 1
            elif code_list[i][0] == '+':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    self.code += '    pop ax\n'
                    flag -= 1
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    self.code += '    pop bx\n'
                    self.code += '    add ax, bx\n'
                    flag -= 1
                else:
                    self.code += '    add ax, %s\n' % code_list[i][2]
                self.code += '    push ax\n'
                flag += 1
            elif code_list[i][0] == '-':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                    self.code += '    sub ax, bx\n'
                else:
                    self.code += '    sub ax, %s\n' % code_list[i][2]
                self.code += '    push ax\n'
                flag += 1
            elif code_list[i][0] == '*':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    self.code += '    pop ax\n'
                    flag -= 1
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    self.code += '    pop bx\n'
                    self.code += '    mul bx\n'
                    flag -= 1
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                    self.code += '    mul bx\n'
                self.code += '    push ax\n'
                flag += 1
            elif code_list[i][0] == '/':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                self.code += '    mov dx, 0\n'
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                    self.code += '    div bx\n'
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                    self.code += '    div bx\n'
                self.code += '    push ax\n'
                flag += 1
            elif code_list[i][0] == '%':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                self.code += '    mov dx, 0\n'
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                    self.code += '    div bx\n'
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                    self.code += '    div bx\n'
                self.code += '    push dx\n'
                flag += 1
            elif code_list[i][0] == 'call':
                self.code += '    call %s\n' % code_list[i][1]
                self.code += '    push ax\n'
                flag += 1
            elif code_list[i][0] == 'para':
                if code_list[i][1][0] != '$' and code_list[i][1] != 'return_value':
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                    self.code += '    push ax\n'
            elif code_list[i][0] == 'j<':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                self.code += '    cmp ax, bx\n'
                self.code += '    jl _%s\n' % code_list[i][3]
            elif code_list[i][0] == 'j>':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                self.code += '    cmp ax, bx\n'
                self.code += '    jg _%s\n' % code_list[i][3]
            elif code_list[i][0] == 'j==':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                self.code += '    cmp ax, bx\n'
                self.code += '    je _%s\n' % code_list[i][3]
            elif code_list[i][0] == 'j<=':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                self.code += '    cmp ax, bx\n'
                self.code += '    jle _%s\n' % code_list[i][3]
            elif code_list[i][0] == 'j>=':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                self.code += '    cmp ax, bx\n'
                self.code += '    jge _%s\n' % code_list[i][3]
            elif code_list[i][0] == 'j!=':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    if flag == 2:
                        self.code += '    pop bx\n'
                    else:
                        flag -= 1
                        self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                if code_list[i][2][0] == '$' or code_list[i][2] == 'return_value':
                    if flag == 2:
                        self.code += '    pop ax\n'
                        flag = 0
                    else:
                        flag -= 1
                        self.code += '    pop bx\n'
                else:
                    self.code += '    mov bx, %s\n' % code_list[i][2]
                self.code += '    cmp ax, bx\n'
                self.code += '    jne _%s\n' % code_list[i][3]
            elif code_list[i][0] == 'jnz':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                self.code += '    cmp ax, 0\n'
                self.code += '    jne _%s\n' % code_list[i][3]
            elif code_list[i][0] == 'jz':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                self.code += '    cmp ax, 0\n'
                self.code += '    je _%s\n' % code_list[i][3]
            elif code_list[i][0] == 'j':
                self.code += '    jmp _%s\n' % code_list[i][3]
            elif code_list[i][0] == '!':
                if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                    self.code += '    pop ax\n'
                else:
                    self.code += '    mov ax, %s\n' % code_list[i][1]
                self.code += '    mov dx, 1\n'
                self.code += '    cmp ax, 0\n'
                self.code += '    je _NOT\n'
                self.code += '    mov dx,0\n'
                self.code += '    _NOT: push dx \n'
            elif code_list[i][0] in fun:
                self.code = self.code[0:-4]
                if flag1:
                    flag1 = False
                    self.code += '_' + str(index) + ':\n'
                    self.code += '    mov ah, 4ch\n    int 21h\n'
                self.code += '%s:\n' % code_list[i][0]
                self.code += '    push bp\n'
                self.code += '    mov bp, sp\n'
                self.code += '    sub sp,20\n'
                bp_index = 4
            elif code_list[i][0] == 'pop':
                # self.code += '    pop ax\n'
                self.code += '    mov ax,[bp+%d]\n' % bp_index
                self.code += '    mov %s, ax\n' % code_list[i][1]
                bp_index += 2
            elif code_list[i][0] == 'ret':
                if code_list[i][1] == '':
                    self.code += '    mov sp,bp\n'
                    self.code += '    pop bp\n'
                    self.code += '    ret\n'
                else:
                    if code_list[i][1][0] == '$' or code_list[i][1] == 'return_value':
                        self.code += '    pop ax\n'
                    else:
                        self.code += '    mov ax, %s\n' % code_list[i][1]
                    self.code += '    mov sp,bp\n'
                    self.code += '    pop bp\n'
                    self.code += '    ret\n'
            #elif code_list[i][0] == '/':
            index += 1

        if flag1:
            self.code += '_'+str(index)+':\n'
            self.code += '    mov ah, 4ch\n    int 21h\n'
            index += 1

        self.code += '_' + str(index) + ':\n'

        self.code += last

        return self.code




