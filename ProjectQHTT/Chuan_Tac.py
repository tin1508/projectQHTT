import Xu_Ly_Dau_Vao

#Chuyển sang dạng chuẩn tắc
def changeIntoStandardForm():
    global c, A, B, X, compare, firstWord, freeVar, negativeVar
    c = Xu_Ly_Dau_Vao.c
    A = Xu_Ly_Dau_Vao.A
    B = Xu_Ly_Dau_Vao.B
    X = Xu_Ly_Dau_Vao.X;
    compare = Xu_Ly_Dau_Vao.compare
    firstWord = Xu_Ly_Dau_Vao.firstWord
    freeVar = Xu_Ly_Dau_Vao.freeVar
    negativeVar = Xu_Ly_Dau_Vao.negativeVar

    result = []
    if firstWord == 'max':
        firstWord = '-min'
        for i in range(len(c)):
            c[i] = c[i] * (-1)
    # xử lý biến tự do
    for var in freeVar:
        if var in X:
            idx = X.index(var)
            posOperator = "\u207A"
            negOperator = "\u207B"
            posVar = f"{var}{posOperator}"
            negVar = f"{var}{negOperator}"
            X[idx:idx + 1] = [posVar, negVar]
            c[idx:idx + 1] = [c[idx], -c[idx]]
            for i in range(len(A)):
                if idx < len(A[i]):
                    A[i][idx:idx + 1] = [A[i][idx], -A[i][idx]]
    # xử lý biến âm
    for var in negativeVar:
        if var in X:
            idx = X.index(var)
            newVar = var + "'"
            X[idx] = newVar
            c[idx] = -c[idx]
            for i in range(len(A)):
                if idx < len(A[i]):
                    A[i][idx] = -A[i][idx]
    
    global newA, newB, newCompare
    newA, newB, newCompare = [], [], []
    # xử lý các ràng buộc
    for i in range(len(compare)):
        row = A[i]
        bValue = int(B[i])
        comp = compare[i]
        if len(row) > 1:
            if comp == '>=':
                bValue *= -1
                row = [-x for x in row]
                comp = '<='
            if comp == '=':
                newA.append(row[:])
                newB.append(bValue)
                newCompare.append('<=')
                newA.append([-x for x in row])
                newB.append(-bValue)
                newCompare.append('<=')
                continue
            newA.append(row[:])
            newB.append(bValue)
            newCompare.append(comp)
    
    # xuất ra output dạng chuỗi
    # hàm mục tiêu
    temp1 = str(c[0]) + X[0] + ' '
    for i in range(1, len(c)):
        if(c[i] == 0):
            continue;
        if(c[i] > 0):
            temp1 = temp1 + '+ ' + str(c[i]) + X[i] + ' '; 
        elif(c[i] < 0):
            temp1 = temp1 + str(c[i])[:1] + ' ' + str(c[i])[1:] + X[i] + ' ';
    result.append(firstWord + ' ' + temp1)
    # các ràng buộc
    for i in range(len(newA)):
        temp2 = ''
        for j in range(len(newA[i])):
            varName = X[j] 
            if newA[i][j] == 0: continue
            if newA[i][j] > 0 and temp2 != '':
                temp2 = temp2 + '+ ' + str(newA[i][j]) + varName + ' ' 
            elif(newA[i][j] > 0 and temp2 == ''):
                temp2 = temp2 + str(newA[i][j]) + varName + ' ' 
            elif A[i][j] < 0 and j > 0:
                temp2 = temp2 + str(newA[i][j])[:1] + ' ' + str(newA[i][j])[1:] + varName + ' '
            else:
                temp2 = temp2 + str(newA[i][j]) + varName + ' '
        temp2 += newCompare[i] + ' ' + str(newB[i])
        result.append(temp2)
    
    # ràng buộc biến >= 0
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
    return '\n'.join(result) 
#Trả ra kết quả để xử lý đơn hình, bland, 2 pha
def returnFormToSolveSimplexAndBland():  
    changeIntoStandardForm()
    newResult = []
    temp1 = [0]
    for i in range(len(c)):
        temp1.append(c[i])
    newResult.append(temp1)
    for i in range(len(newB)):
        temp2 = []
        temp2.append(newB[i])
        for j in range(len(newA[i])):
            temp2.append(-newA[i][j])
        newResult.append(temp2)
    return newResult
    