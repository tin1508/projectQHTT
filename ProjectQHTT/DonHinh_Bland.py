#Giải bài toán theo phương pháp đơn hình và bland
import copy

def getSymplex(equation, condition):
    size_col = len(equation[0])
    size_row = len(equation)
    variables = [
        "b"  if i == 0 else f"x" + chr(0x2080 + i) 
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
                continue
            sign = "+" if coef > 0 else "-"
            coef_abs = abs(coef)
            if coef_abs == 1:
                terms.append(f"{sign} {var}")
            else:
                terms.append(f"{sign} {coef_abs:.2f}{var}")

        rhs = " ".join(terms)
        result.append(f"{left} = {b:.2f} {' ' + rhs if rhs else ''}")
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
def ifinitySolution(symplex, outputCall):
    Right = symplex["Equation"][0]["Right"]
    for i in range(1, len(Right)):
        if Right[i] == 0 :
            outputCall(f"Boi vi {symplex["Variable"][i]}","=", f"{Right[i]:.0f}")
            variables = symplex["Variable"]
            for eq in symplex["Equation"]:
                left = eq["Left"]
                right = eq["Right"]
                b = right[0]
                terms = []
                for coef, var in zip(right[1:], variables[1:]):
                    if coef == 0 or var == variables[i - 1]:
                        continue
                    sign = "+" if coef > 0 else "-"
                    coef_abs = abs(coef)
                    if coef_abs == 1:
                        terms.append(f"{sign} {var}")
                    else:
                        terms.append(f"{sign} {coef_abs:.2f}{var}")
                rhs = " ".join(terms)
                outputCall(f"{left} = {b:.2f} {' ' + rhs if rhs else ''}")
            #Xu ly dau
            size_col = len(symplex["Equation"][0]["Right"])
            if size_col == 3:
                variables = symplex["Variable"]
                bounds = []
                for eq in symplex["Equation"][1:]: 
                    left = eq["Left"]
                    right = eq["Right"]
                    b = right[0]
                    for coef, var in zip(right[1:], variables[1:]):
                        if coef != 0 and var != variables[i - 1]:
                            if coef < 0:
                                bound = b / abs(coef)
                                bounds.append((f"{variables[i]} < {bound:.2f}"))
                            else:
                                bound = -b / coef
                                bounds.append((f"{variables[i]} > {bound:.2f}"))  
                for b in bounds:
                    outputCall(b) 
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
    new_pivot = [x/(-pivot_element) for x in pivot_row]
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
    result = []
    for i in range(size_row):
        if symplex["Equation"][i]["Left"] == "z" and condition == "max":
            outputCall(f"{symplex['Equation'][i]['Left']} : {-symplex['Equation'][i]['Right'][0]:.2f}")
        else:
            outputCall(f"{symplex['Equation'][i]['Left']} : {symplex['Equation'][i]['Right'][0]:.2f}")
    for i in range(1, size_col):
        outputCall(f"{symplex['Variable'][i]} :  {0}")
def solveSymplex(equation, condition, outputCall):
    outputCall("Symplex")
    symplex = getSymplex(equation, condition)
    outputCall(returnEquation(symplex))
    while True:
        if ifinitySolution(symplex, outputCall):
            outputCall("Infinity Solution")
            break
        if stopSymplex(symplex):
            outputCall("Unique solution")
            outputCall(result(symplex, condition, outputCall))
            break
        min_indexGetMin = findMinVariable(symplex)
        min_indexGetDivine = findMinDivine(symplex, min_indexGetMin)
        if unboundedSolution(symplex, min_indexGetMin):
            outputCall("Unbounded Solution")
            if symplex["Condition"] == "min":
                outputCall(f"z = {float('-inf')}")
            else:
                outputCall(f"z = {float('inf')}")
            break
        outputCall(f"Bien dau vao: {symplex["Variable"][min_indexGetMin]}")
        outputCall(f"Bien dau ra: {symplex["Equation"][min_indexGetDivine]["Left"]}")
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
def solveBland(equation, condition, outputCall):
    outputCall("Bland")
    symplex = getSymplex(equation, condition)
    outputCall(returnEquation(symplex))
    while True:
        if ifinitySolution(symplex, outputCall):
            outputCall("Infinity Solution")
            break
        if stopSymplex(symplex):
            outputCall("Unique solution")
            result(symplex, condition, outputCall)
            break
        min_indexGetMin = findMinVariableBland(symplex)
        min_indexGetDivine = findMinDivine(symplex, min_indexGetMin)
        if unboundedSolution(symplex, min_indexGetMin):
            outputCall("Unbounded Solution")
            if symplex["Condition"] == "min":
                outputCall(f"z = {float('-inf')}")
            else:
                outputCall(f"z = {float('inf')}")
            break
        outputCall(f"Bien dau vao: {symplex["Variable"][min_indexGetMin]}")
        outputCall(f"Bien dau ra: {symplex["Equation"][min_indexGetDivine]["Left"]}")
        outputCall("-------------------------------------")
        symplex = rotate(symplex, min_indexGetMin, min_indexGetDivine)
        outputCall(returnEquation(symplex))
            

            
