import Chuan_Tac

#chuyển sang dạng chính tắc
def changeIntoAugmentedForm():
    c = Chuan_Tac.c
    A = Chuan_Tac.A
    B = Chuan_Tac.B
    X = Chuan_Tac.X;
    compare = Chuan_Tac.compare
    firstWord = Chuan_Tac.firstWord
    freeVar = Chuan_Tac.freeVar

    result = []
    Chuan_Tac.changeIntoStandardForm()
    newCompare, newW = [], []
    count = 1
    #xử lý các ràng buộc
    for i in range(len(A)):
        row = A[i]
        comp = compare[i]
        if(len(row) > 1):
            if(comp == '>=' or comp == '<='):
                newW.append('w' + str(count))
                count = count + 1
                comp = '='
            else:
                newW.append('0.0')
            newCompare.append(comp)
    #xuất ra output dạng chuỗi
    #hàm mục tiêu
    temp1 = str(c[0]) + X[0] + ' '
    for i in range(1, len(c)):
        if c[i] == 0: continue
        if c[i] > 0:
            temp1 = temp1 + '+ ' + str(c[i]) + X[i] + ' '; 
        elif c[i] < 0:
            temp1 = temp1 + str(c[i])[:1] + ' ' + str(c[i])[1:] + X[i] + ' ';
    result.append(firstWord + ' ' + temp1)
    #các ràng buộc
    for i in range(len(A)):
        temp2 = ''
        for j in range(len(A[i])):
            varName = X[j] 
            if A[i][j] == 0: continue
            if A[i][j] > 0 and temp2 != '':
                temp2 = temp2 + '+ ' + str(A[i][j]) + varName + ' ' 
            elif(A[i][j] > 0 and temp2 == ''):
                temp2 = temp2 + str(A[i][j]) + varName + ' ' 
            elif A[i][j] < 0 and j > 0:
                temp2 = temp2 + str(A[i][j])[:1] + ' ' + str(A[i][j])[1:] + varName + ' '
            else:
                temp2 = temp2 + str(A[i][j]) + varName + ' '
        result.append(temp2 + ' + ' + newW[i] + ' ' + newCompare[i] + ' ' + str(B[i]))
    for var in X:
        if "'" in var:
            origin = var[:-1]
            result.append(f"{var} >= 0 với {var} = -{origin}")
        elif '+' in var or '-' in var: 
            origin = var[:-1]
            if origin in freeVar:
                result.append(f"{var} >= 0")
            else:
                result.append(f"{var} >= 0")
        else:
            result.append(f"{var} >= 0")
    for w in newW:
        if(w != '0'):
            result.append(f"{w} >= 0")
    return '\n'.join(result)