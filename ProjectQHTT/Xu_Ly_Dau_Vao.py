#xử lý đầu vào và chuyển sang dạng chính tắc và chuẩn tắc
import re

def reset():
    global c, A, B, X, compare, firstWord, linesProcessing, freeVar, negativeVar, originFirstWord
    c = [] 
    A = [] #lưu các hệ số của các ràng buộc
    B = [] #lưu các số bên phải phép so sánh
    X = [] #lưu các biến 
    compare = [] #lưu các phép so sánh
    firstWord = '' #lưu xem hàm mục tiêu là max hay min
    originFirstWord = '' #dùng để lưu min hay max ban đầu để xử lý đơn hình
    linesProcessing = []
    freeVar = []
    negativeVar = []
def inputStringProcessing(s):
    global c, A, B, X, compare, firstWord, linesProcessing, freeVar, negativeVar, originFirstWord
    reset()
    strAfterProcess = []
    lines = []
    for line in s.strip().split('\n'):
        if line.strip() != '':
            lines.append(line.strip())
    if len(lines) <= 1:
        strAfterProcess.append("Bài toán không hợp lệ!!!")
        return strAfterProcess
    for i in range(len(lines)):
        #Thêm khoảng trắng giữa dấu +, - và biến, ví dụ 3x+2y => 3x + 2y 
        lines[i] = re.sub(r'([^\s])([+-])', r'\1 \2', lines[i])
        #Đảm bảo luôn có khoảng trắng giữa biến và dấu so sánh
        lines[i] = re.sub(r'(<=|>=|=)(\w+)', r'\1 \2', lines[i])
        lines[i] = re.sub(r'(\w+)(<=|>=|=)', r'\1 \2', lines[i])
    #kiểm tra định dạng
    matchAimFunction = re.match(r'^(max|min)\s+([+-]?\s*\d*(?:\.\d+)?\s*[a-z]\d+)(\s*[+-]\s*\d*(?:\.\d+)?\s*[a-z]\d+)*$',lines[0].strip())
    if not matchAimFunction: #ko đúng định dạng hàm mục tiêu
        strAfterProcess.append("Hàm mục tiêu không đúng định dạng!!!")
        return strAfterProcess
    #xử lý trường hợp các ràng buộc không đúng định dạng
    for i in range(1, len(lines)):
        checkConstraintForm = re.match(r'^([+-]?\s*\d*(?:\.\d+)?\s*[a-zA-Z]\d*\s*)+(<=|>=|=)\s*[-+]?\d+(?:\.\d+)?\s*$',lines[i])
        if not checkConstraintForm:
            strAfterProcess.append("Ràng buộc không đúng định dạng!!!")
            return strAfterProcess
    #tách ra từng phân tử trong 1 mảng để xử lý
    for line in lines:
        cutStr = line.strip()
        if cutStr:
            linesProcessing.append(cutStr)
    firstLine = linesProcessing[0]
    firstWord = (firstLine.split())[0]
    originFirstWord = firstWord
    linesProcessing[0] = (linesProcessing[0].replace(firstWord, '')).strip()
    boundedVars = set()
    for k in range(len(linesProcessing)):
        temp = linesProcessing[k].split()
        # Nếu dòng chỉ có 1 biến và dạng biến không âm, ví dụ: x1 >= 0, dùng re.match để kiểm tra định dạng của chuỗi
        if len(temp) == 3 and temp[1] in ('>=', '<=') and temp[2] == '0' and re.match(r'^[a-z]\w*$', temp[0]):
            var = temp[0]
            if var not in X:
                X.append(var)
            if var not in negativeVar and temp[1] == '<=':
                negativeVar.append(var)
            boundedVars.add(var)
            continue
        if len(temp) == 1:
            freeVar.append(temp[0])
            continue
        coefs = {}
        for i, j  in enumerate(temp):
            if j in ('>=', '<=', '='):
                B.append(float(temp[i + 1]))
                compare.append(j)
            else:
                if i > 0 and temp[i - 1] in ('+', '-'):
                    j = temp[i - 1] + j
                match = re.match(r'([+-]?\s*\d*(?:\.\d+)?)([a-z]\d*)', j)
                if match:
                    coefStr, var = match.groups()
                    if(coefStr in ('', '+')):
                        coef = 1.0
                    elif(coefStr == '-'):
                        coef = -1.0
                    else:
                        coef = float(coefStr)
                    if(k == 0):
                        c.append(float(coef))
                    else:
                        coefs[var] = coef
                    if(var not in X):
                        X.append(var)
        # Nếu là ràng buộc, không phải dòng hàm mục tiêu
        if k != 0 and coefs:
            # tạo đầy đủ hệ số theo biến X đã biết
            coefs = [coefs.get(var, 0.0) for var in X]
            A.append(coefs)
    #Kiểm tra xem có bao nhiêu biến rồi xử lý tiếp, bài toán cần ít nhất 2 biến trở lên
    if len(X) < 2 or len(c) < 2: 
        strAfterProcess.append("Bài toán phải có  2 biến trở lên!!!")
        return strAfterProcess
    constrainedVars = set()
    for k, comp in enumerate(compare):
        if comp in ('>=', '<=') and float(B[k]) == 0:
            for i, coef in enumerate(A[k]):
                if coef != 0:
                    constrainedVars.add(X[i])    
    constrainedVars.update(boundedVars)
    # Những biến không nằm trong constrainedVars là biến tự do
    for var in X:
        if var not in constrainedVars:
            freeVar.append(var)
    linesProcessing
    return linesProcessing