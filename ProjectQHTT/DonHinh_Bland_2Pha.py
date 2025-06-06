#code chức năng
import copy
import re
#Dieu kien dau vao
def getSymplex(equation, varVec, condition):
    size_col = max(len(equation[i]) for i in range(len(equation)))
    size_row = len(equation)
    variables = [
        "b"  if i == 0 else varVec[i - 1] 
        for i in range(size_col)
    ]
    Lefts = [
        "z"  if i == 0 else f"w" + chr(0x2080 + i) 
        for i in range(size_row)
    ]

    symplex = {
        "Variable" : variables,
        "Condition" : condition,
        "Equation" : [
            {"Left" : Lefts[i], "Right" : equation[i]}
            for i in range(size_row)
        ]
    }
    return symplex
def returnEquation(symplex):
    result = []
    variables = symplex["Variable"]
    for eq in symplex["Equation"]:
        left = eq["Left"]
        right = eq["Right"]
        b = right[0]
        terms = []
        for coef, var in zip(right[1:], variables[1:]):
            if coef == 0:
                terms.append("      ")  
            else:
                sign = "+" if coef > 0 else "-"
                coef_abs = abs(coef)
                if coef_abs == int(coef_abs):
                    if coef_abs == 1:
                        terms.append(f"{sign} {var}")
                    else:
                        terms.append(f"{sign} {int(coef_abs)}{var}")
                else:
                    terms.append(f"{sign} {coef_abs:.2f}{var}")
        rhs = " ".join(terms)
        result.append(f"{left} = {b:.2f}{' ' + rhs if rhs else ''}")
    return '\n'.join(result)
def findMinVariable(symplex):
    equation = symplex["Equation"][0]["Right"]
    min_value = min(equation[1:])
    min_index = equation[1:].index(min_value) + 1
    return  min_index
def findMinDivine(symplex, min_indexGetMin):
    size_row = len(symplex["Equation"])
    result = []
    for i in range(1, size_row): 
        Right = symplex["Equation"][i]["Right"]
        x_i = Right[min_indexGetMin]
        b = Right[0]
        if x_i < 0:
            num = b / abs(x_i)
            result.append((i,num))
    if not result:
        return None
    min_row = min(result, key=lambda x: x[1])[0]
    return min_row
def  infinitySolution(symplex, condition, outputCall):
    Right = symplex["Equation"][0]["Right"]
    checkValue = all(value >= 0 for value in Right[1:])
    for i in range(1, len(Right)):
        if Right[i] == 0 and checkValue:
            outputCall(f"Bởi vì hệ số {symplex["Variable"][i]} = {Right[i]:.0f}")
            size_row = len(symplex["Equation"])
            size_col = len(symplex["Equation"][0]["Right"])
            for i in range(size_row):
                if symplex["Equation"][i]["Left"] == "z" and condition == "max":
                    outputCall(f"{symplex["Equation"][i]["Left"]} : {-symplex["Equation"][i]["Right"][0]:.2f}")
                elif symplex["Equation"][i]["Left"] == "z" and condition == "min":
                    outputCall(f"{symplex["Equation"][i]["Left"]} : {symplex["Equation"][i]["Right"][0]:.2f}")
            #Xu ly dau
            size_col = len(symplex["Equation"][0]["Right"])
            if size_col == 2:
                variables = symplex["Variable"]
                for eq in symplex["Equation"][1:]: 
                    left = eq["Left"]
                    right = eq["Right"]
                    b = right[0]
                    if right[1] > 0:
                        outputCall(f"{variables[1]} >= {-b/right[1]}")
                    else:
                        if right[1] < 0:
                            outputCall(f"{variables[1]} <= {-b/-right[1]}")
            return True
    return False
def unboundedSolution(symplex, min_indexGetMin):
    if findMinDivine(symplex, min_indexGetMin) is None:
        return True
    return False
def stopSymplex(symplex):
    size_col = len(symplex["Equation"][0]["Right"])
    size_row = len(symplex["Equation"])
    count = 0
    for i in range(1,size_col):
        if symplex["Equation"][0]["Right"][i] < 0:
            return False
    return True
def updateLabel(symplex, min_indexGetMin, min_indexGetDivine):
    newVarCol = symplex["Variable"][min_indexGetMin]
    newVarRow = symplex["Equation"][min_indexGetDivine]["Left"]
    symplex["Variable"][min_indexGetMin] = newVarRow
    symplex["Equation"][min_indexGetDivine]["Left"] = newVarCol
def rotate(symplex, min_indexGetMin, min_indexGetDivine):
    size_row = len(symplex["Equation"])
    size_col = len(symplex["Equation"][0]["Right"])
    pivot_row = symplex["Equation"][min_indexGetDivine]["Right"]
    pivot_element = pivot_row[min_indexGetMin]
    new_symplex = copy.deepcopy(symplex)
    for i in range(size_row):
        if i != min_indexGetDivine:
             current_row = symplex["Equation"][i]["Right"]
             num = current_row[min_indexGetMin]/pivot_element
             new_row = [current_row[j] - num * pivot_row[j] for j in range(size_col)]
             symplex["Equation"][i]["Right"] = new_row
    new_pivot = [x/ (-pivot_element) for x in pivot_row]
    new_pivot[min_indexGetMin] = new_pivot[min_indexGetMin]/(-pivot_element)
    symplex["Equation"][min_indexGetDivine]["Right"] = new_pivot
    for i in range(size_row):
        if i != min_indexGetDivine:
            num  = new_symplex["Equation"][i]["Right"][min_indexGetMin]
            symplex["Equation"][i]["Right"][min_indexGetMin] = num/pivot_element
    updateLabel(symplex, min_indexGetMin, min_indexGetDivine)
    return symplex
def result(symplex, condition, outputCall):
    size_row = len(symplex["Equation"])
    size_col = len(symplex["Equation"][0]["Right"])
    for i in range(size_row):
        if symplex["Equation"][i]["Left"] == "z" and condition == "max":
            outputCall(f"{symplex["Equation"][i]["Left"]} : {-symplex["Equation"][i]["Right"][0]:.2f}")
        else:
            outputCall(f"{symplex["Equation"][i]["Left"]} : {symplex["Equation"][i]["Right"][0]:.2f}")
    for i in range(1, size_col):
        outputCall(f"{symplex["Variable"][i]} : {0}")

#Symplex
def solveSymplex(equation, condition, varVec, outputCall):
    outputCall("Symplex")
    symplex = getSymplex(equation, varVec, condition)
    outputCall(returnEquation(symplex))
    while True:
        if  infinitySolution(symplex, condition, outputCall):
            outputCall("Vô số nghiệm")
            break
        if stopSymplex(symplex):
            outputCall("Nghiệm duy nhất")
            result(symplex, condition, outputCall)
            break
        min_indexGetMin = findMinVariable(symplex)
        min_indexGetDivine = findMinDivine(symplex, min_indexGetMin)
        if unboundedSolution(symplex, min_indexGetMin):
            outputCall("Bài toán không giới nội")
            if symplex["Condition"] == "min":
                outputCall(f"z = {float('-inf')}")
            else:
                outputCall(f"z = {float('inf')}")
            break
        outputCall(f"Biến đầu vào: {symplex["Variable"][min_indexGetMin]}")
        outputCall(f"Biến đầu ra: {symplex["Equation"][min_indexGetDivine]["Left"]}")
        outputCall("-------------------------------------")
        symplex = rotate(symplex, min_indexGetMin, min_indexGetDivine)
        outputCall(returnEquation(symplex))
#Bland
def findMinVariableBland(symplex):
    equation = symplex["Equation"][0]["Right"]
    variable = symplex["Variable"]
    x_indices = [
        i for i, var in enumerate(variable[1:], start=1)
        if var.startswith("x") and equation[i] < 0
    ]
    if x_indices:
        return min(x_indices)  
    w_indices = [
        i for i, var in enumerate(variable[1:], start=1)
        if var.startswith("w") and equation[i] < 0
    ]
    if w_indices:
        return min(w_indices)
    return None
def solveBland(equation, condition, varVec, outputCall):
    outputCall("Bland")
    symplex = getSymplex(equation, varVec, condition)
    outputCall(returnEquation(symplex))
    while True:
        if  infinitySolution(symplex, condition, outputCall):
            outputCall("vô số nghiệm")
            break
        if stopSymplex(symplex):
            outputCall("Nghiệm duy nhất")
            result(symplex, condition, outputCall)
            break
        min_indexGetMin = findMinVariableBland(symplex)
        min_indexGetDivine = findMinDivine(symplex, min_indexGetMin)
        if unboundedSolution(symplex, min_indexGetMin):
            outputCall("Bài toán không giới nội")
            if symplex["Condition"] == "min":
                outputCall(f"z = {float('-inf')}")
            else:
                outputCall(f"z = {float('inf')}")
            break
        outputCall(f"Biến đầu vào: {symplex["Variable"][min_indexGetMin]}")
        outputCall(f"Biến đầu ra: {symplex["Equation"][min_indexGetDivine]["Left"]}")
        outputCall("-------------------------------------")
        symplex = rotate(symplex, min_indexGetMin, min_indexGetDivine)
        outputCall(returnEquation(symplex))
#Phase One
def get_index_from_var(var):
    # Tìm số thường liền sau x (vd: x1, x12)
    match = re.match(r'x(\d+)', var)
    if match:
        return int(match.group(1))
    # Nếu không có, thì thử tìm số subscript như trước
    subscript_map = {
        '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4',
        '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9'
    }
    subscript_chars = ''.join(ch for ch in var if ch in subscript_map)
    if subscript_chars:
        return int(''.join(subscript_map[ch] for ch in subscript_chars))
    return -1
def get_subscript_index(var):
    # Lấy phần chỉ số unicode subscript của biến
    # Ví dụ: var = 'x₁₀' -> lấy '₁₀'
    subscript_part = var[1:]  # cắt bỏ chữ 'x'
    return get_index_from_var(var)
def getPhaseOne(equation, varVec, condition):
    size_col = max(len(equation[i]) for i in range(len(equation)))
    size_row = len(equation)
    variables = [
        "b"  if i == 0 else varVec[i - 1] 
        for i in range(size_col)
    ]  + ["x" + chr(0x2080 + 0)]
    Lefts = [
        "z"  if i == 0 else f"w" + chr(0x2080 + i) 
        for i in range(size_row)
    ]
    if len(equation[0]) < size_col:
        num_zeros = size_col - len(equation[0])
        equation[0].extend([0] * num_zeros)        
    for i in range(max(len(equation[i]) for i in range(len(equation)))):
        equation[0][i] = 0
    for i in range(len(equation)):
        equation[i].append(1)
    symplex = {
        "Variable" : variables,
        "Condition" : condition,
        "Equation" : [
            {"Left" : Lefts[i], "Right" : equation[i]}
            for i in range(size_row)
        ]
    }
    return symplex
def solveTwoPhaseSymplex(equation, condition, varVec,  outputCall):
    #Pha 1
    size_col = max(len(equation[i]) for i in range(len(equation)))
    size_row = len(equation)
    copySymplex = getSymplex(equation, varVec, condition)
    copy_symplex = copy.deepcopy(copySymplex)
    symplex = getPhaseOne(equation, varVec, condition)
    outputCall(returnEquation(symplex))
    #min_indexGetMin
    min_indexGetMin = size_col
    #min_indexGetDivine
    size_row = len(symplex["Equation"])
    resultIndex = []
    for i in range(1, size_row): 
        Right = symplex["Equation"][i]["Right"]
        b = Right[0]
        if b < 0:
            resultIndex.append((i,b))
    if not resultIndex:
        outputCall("Không có dòng nào có hệ số âm bên phải trong pha 1.")
        return
    min_indexGetDivine = min(resultIndex, key=lambda x: x[1])[0]
    outputCall(f"Biến đầu vào: {symplex["Variable"][min_indexGetMin]}")
    outputCall(f"Biến đầu ra: {symplex["Equation"][min_indexGetDivine]["Left"]}")
    outputCall("-------------------------------------")
    symplex = rotate(symplex, min_indexGetMin, min_indexGetDivine)
    outputCall(returnEquation(symplex))
    while True:
        checkB = all(symplex["Equation"][i]["Right"][0] >= 0 for i in range(1, len(symplex["Equation"])))
        if  checkB and stopSymplex(symplex):
            outputCall("Pha 1 kết thúc ")
            break
        min_indexGetMin = findMinVariable(symplex)
        min_indexGetDivine = findMinDivine(symplex, min_indexGetMin)
        outputCall(f"Biến đầu vào: {symplex["Variable"][min_indexGetMin]}")
        outputCall(f"Biến đầu ra: {symplex["Equation"][min_indexGetDivine]["Left"]}")
        outputCall("-------------------------------------")
        symplex = rotate(symplex, min_indexGetMin, min_indexGetDivine)
        outputCall(returnEquation(symplex))
    #Chuyển pha 1 sang pha 2
    try:
        index_x0 = symplex["Variable"].index("x₀")  # tìm vị trí x₀
    except ValueError:
        outputCall("Không tìm thấy biến x₀")
        outputCall("Bài toán vô nghiệm")
        return 
    checkEquation = True
    for i, value in enumerate(symplex["Equation"][0]["Right"]):
        if i == index_x0:
            if value != 1:
                checkEquation = False
        else:
            if value != 0:
                checkEquation = False
    if checkEquation == True:
        index_x0 = symplex["Variable"].index("x₀")
        size_col = max(len(equation[i]) for i in range(len(equation)))
        size_row = len(equation)
        equa = []
        varList = []
        array = [0]*size_col
        for eq in symplex["Equation"]:
            leftVar = eq["Left"]
            if leftVar.startswith('x') and leftVar != f"x" + chr(0x2080 + 0):
                equa.append(eq["Right"])
                varList.append(leftVar)
        for var in symplex["Variable"]:
            if var.startswith('x')  and var != f"x" + chr(0x2080 + 0):
                varList.append(var)
                equa.append(array.copy())
        varEquaPairs = list(zip(varList, equa))
        varEquaPairsSorted = sorted(varEquaPairs, key=lambda pair: (
            get_subscript_index(pair[0]),
            0 if '⁺' in pair[0] else 1 if '⁻' in pair[0] else 2
        ))
        varSorted = [pair[0] for pair in varEquaPairsSorted]
        equaSorted = [pair[1] for pair in varEquaPairsSorted]
        for i, equa in enumerate(equaSorted):
            if all(abs(x) < 1e-8 for x in equa):  
                indexX = symplex["Variable"].index(varSorted[i])        
                equa[indexX] = 1
        z = [0] * size_col
        for right, equa in zip(copy_symplex["Equation"][0]["Right"][1:], equaSorted):
            z = [zj + right * ej for zj, ej in zip(z, equa)]
        indexX0 = -1
        for i, var in enumerate(symplex["Variable"]):
            if var == f"x" + chr(0x2080 + 0):
                indexX0 = i
                break
        symplex["Equation"][0]["Right"] = z
        for equa in symplex["Equation"]:
            equa["Right"][indexX0] = 0
        symplex["Variable"].pop(indexX0)
        for equa in symplex["Equation"]:
            equa["Right"].pop(indexX0)
        #Phase Two
        outputCall("-------------------------------------")
        outputCall("Pha hai")
        outputCall("Dùng đơn hình")
        outputCall(returnEquation(symplex))
        while True:
            if  infinitySolution(symplex, condition, outputCall):
                outputCall("Vô số nghiệm")
                break
            if stopSymplex(symplex):
                outputCall("Nghiệm duy nhất")
                result(symplex, condition, outputCall)
                break
            min_indexGetMin = findMinVariable(symplex)
            min_indexGetDivine = findMinDivine(symplex, min_indexGetMin)
            if unboundedSolution(symplex, min_indexGetMin):
                outputCall("Bài toán không giới nội")
                if symplex["Condition"] == "min":
                    outputCall(f"z = {float('-inf')}")
                else:
                    outputCall(f"z = {float('inf')}")
                break
            outputCall(f"Biến đầu vào: {symplex["Variable"][min_indexGetMin]}")
            outputCall(f"Biến đầu ra: {symplex["Equation"][min_indexGetDivine]["Left"]}")
            outputCall("-------------------------------------")
            symplex = rotate(symplex, min_indexGetMin, min_indexGetDivine)
            outputCall(returnEquation(symplex))
    else:
        outputCall("Bài toán vô nghiệm")
    return symplex

            

            
