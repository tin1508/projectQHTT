#xử lý đầu vào và chuyển sang dạng chính tắc và chuẩn tắc
import re

c = [] #lưu các hệ số của hàm mục tiêu
A = [] #lưu các hệ số của các ràng buộc
B = [] #lưu các số bên phải phép so sánh
X = [] #lưu các biến 
compare = [] #lưu các phép so sánh
firstWord = '' #lưu xem hàm mục tiêu là max hay min
linesProcessing = [];
freeVar = [];
negativeVar = [];
def inputStringProcessing(s):
    global c, A, B, X, compare, firstWord, linesProcessing, freeVar, negativeVar;
    lines = s.split('\n');
    #xử lý trường hợp nếu người dùng nhập vào 1 chuỗi rỗng
    if not lines: return;
    # chuẩn hóa các dòng để tác dòng ví dụ: x1 + x2>=0 => x1 + x2 >= 0
    for i in range(len(lines)):
        #Thêm khoảng trắng giữa dấu +, - và biến, ví dụ 3x+2y => 3x + 2y 
        lines[i] = re.sub(r'([^\s])([+-])', r'\1 \2', lines[i]);
        #Đảm bảo luôn có khoảng trắng giữa biến và dấu so sánh
        lines[i] = re.sub(r'(<=|>=|=)(\w+)', r'\1 \2', lines[i])
        #+4x1 => + 4x1
        lines[i] = re.sub(r'([+-])([^\s])', r'\1 \2', lines[i]);
    for line in lines:
        cutStr = line.strip();
        if cutStr:
            linesProcessing.append(cutStr);
    firstLine = linesProcessing[0];
    firstWord = (firstLine.split())[0];
    linesProcessing[0] = (linesProcessing[0].replace(firstWord, '')).strip();

    boundedVars = set();
    for k in range(len(linesProcessing)):
        temp = linesProcessing[k].split();
        # Nếu dòng chỉ có 1 biến và dạng biến không âm, ví dụ: x1 >= 0
        if len(temp) == 3 and temp[1] in ('>=', '<=') and temp[2] == '0' and re.match(r'^[a-z]\w*$', temp[0]):
            var = temp[0]
            if var not in X:
                X.append(var);
            if var not in negativeVar:
                negativeVar.append(var);
            boundedVars.add(var);
            continue
        if len(temp) == 1:
            freeVar.append(temp[0]);
            continue;
        coefs = {};
        for i, j  in enumerate(temp):
            if(j in ('>=', '<=', '=')):
                if temp[i + 1] != '0':
                    B.append(temp[i + 1])
                    compare.append(j)
            else:
                if(i > 0 and temp[i - 1] in ('+', '-')):
                    j = temp[i - 1] + j;
                match = re.match(r'([+-]?\d*)([a-z]\w*)', j);
                if(match):
                    coefStr, var = match.groups();
                    if(coefStr in ('', '+')):
                        coef = 1;
                    elif(coefStr == '-'):
                        coef = -1;
                    else:
                        coef = int(coefStr);
                    if(k == 0):
                        c.append(coef);
                    else:
                        coefs[var] = coef;
                    if(var not in X):
                        X.append(var);
        # Nếu là ràng buộc (không phải dòng hàm mục tiêu)
        if k != 0 and coefs:
            # tạo đầy đủ hệ số theo biến X đã biết
            coefs = [coefs.get(var, 0) for var in X];
            A.append(coefs);
    constrainedVars = set();
    for k, comp in enumerate(compare):
        if comp in ('>=', '<=') and int(B[k]) == 0:
            for i, coef in enumerate(A[k]):
                if coef != 0:
                    constrainedVars.add(X[i])    
    constrainedVars.update(boundedVars);
    # Những biến không nằm trong constrained_vars là biến tự do
    for var in X:
        if var not in constrainedVars:
            freeVar.append(var)
    return linesProcessing;
#chuyển sang dạng chuẩn tắc
def changeIntoStandard():
    global c, A, B, X, compare, firstWord, freeVar, negativeVar;
    result = [];
    if firstWord == 'max':
        firstWord = '-min';
        for i in range(len(c)):
            c[i] = c[i] * (-1);
    # xử lý biến tự do
    for var in freeVar:
        if var in X:
            idx = X.index(var)
            posVar = var + '+'
            negVar = var + '-'
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
    
    global newA, newB, newCompare;
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
        if c[i] == 0: continue;
        if c[i] > 0:
            temp1 = temp1 + '+ ' + str(c[i]) + X[i] + ' '
        else:
            temp1 = temp1 + str(c[i])[:1] + ' ' + str(c[i])[1:] + X[i] + ' '
    result.append(firstWord + ' ' + temp1)
    # các ràng buộc
    for i in range(len(newA)):
        temp2 = ''
        for j in range(len(newA[i])):
            varName = X[j] if j < len(X) else f"x{j+1}";
            if(A[i][j] == 0): continue;
            if(A[i][j] > 0 and temp2 != ''):
                temp2 = temp2 + '+ ' + str(A[i][j]) + varName + ' '; 
            elif(A[i][j] > 0 and temp2 == ''):
                temp2 = temp2 + str(A[i][j]) + varName + ' '; 
            elif(A[i][j] < 0 and j > 0):
                temp2 = temp2 + str(A[i][j])[:1] + ' ' + str(A[i][j])[1:] + varName + ' ';
            else:
                temp2 = temp2 + str(A[i][j]) + varName + ' ';
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
    return '\n'.join(result); 
#chuyển sang dạng chính tắc
def changeIntoCanonical():
    global c, A, B, X, compare, firstWord, linesProcessing, freeVar, negativeVar;
    result = [];
    changeIntoStandard();
    newCompare, newW = [], [];
    count = 1;
    #xử lý các ràng buộc
    for i in range(len(A)):
        row = A[i];
        comp = compare[i];
        if(len(row) > 1):
            if(comp == '>=' or comp == '<='):
                newW.append('w' + str(count));
                count = count + 1;
                comp = '=';
            else:
                newW.append('0');
            newCompare.append(comp);
    #xuất ra output dạng chuỗi
    #hàm mục tiêu
    temp1 = str(c[0]) + X[0] + ' ';
    for i in range(1, len(c)):
        if(c[i] == 0):
            continue;
        if(c[i] > 0):
            temp1 = temp1 + '+ ' + str(c[i]) + X[i] + ' '; 
        elif(c[i] < 0):
            temp1 = temp1 + str(c[i])[:1] + ' ' + str(c[i])[1:] + X[i] + ' ';
    result.append(firstWord + ' ' + temp1);
    #các ràng buộc
    for i in range(len(A)):
        temp2 = '';
        for j in range(len(A[i])):
            varName = X[j] if j < len(X) else f"x{j+1}";
            if(A[i][j] == 0): continue;
            if(A[i][j] > 0 and temp2 != ''):
                temp2 = temp2 + '+ ' + str(A[i][j]) + varName + ' '; 
            elif(A[i][j] > 0 and temp2 == ''):
                temp2 = temp2 + str(A[i][j]) + varName + ' '; 
            elif(A[i][j] < 0 and j > 0):
                temp2 = temp2 + str(A[i][j])[:1] + ' ' + str(A[i][j])[1:] + varName + ' ';
            else:
                temp2 = temp2 + str(A[i][j]) + varName + ' ';
        result.append(temp2 + ' + ' + newW[i] + ' ' + newCompare[i] + ' ' + str(B[i]));
    for var in X:
        if "'" in var:
            origin = var[:-1];
            result.append(f"{var} >= 0 với {var} = -{origin}");
        elif '+' in var or '-' in var: 
            origin = var[:-1];
            if origin in freeVar:
                result.append(f"{var} >= 0")
            else:
                result.append(f"{var} >= 0")
        else:
            result.append(f"{var} >= 0");
    for w in newW:
        if(w != '0'):
            result.append(f"{w} >= 0");
    return '\n'.join(result);
#trả về mảng để xử lý đơn hình và bland
def returnFormToSolveSimplex():
    global newA, newB;
    changeIntoStandard();
    newResult = [];
    for i in range(len(newB)):
        temp = [];
        temp.append(newB[i]);
        for j in range(len(newA[i])):
            temp.append(-newA[i][j]);
        newResult.append(temp);
    return newResult;
def reset():
    global c, A, B, X, compare, firstWord, linesProcessing, freeVar, negativeVar;
    c = [] 
    A = [] #lưu các hệ số của các ràng buộc
    B = [] #lưu các số bên phải phép so sánh
    X = [] #lưu các biến 
    compare = [] #lưu các phép so sánh
    firstWord = '' #lưu xem hàm mục tiêu là max hay min
    linesProcessing = [];
    freeVar = [];
    negativeVar = [];

if __name__ == "__main__":
    print("Enter a string:")
    s = ""
    while True:
        line = input()
        if line == "":
            break
        s += line + "\n"
    inputStringProcessing(s);
    print(returnFormToSolveSimplex());
