import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import re

# ======== Logic giải bài toán QHTT ========

def find_intersection(line1, line2):
    A = np.array([line1[:2], line2[:2]])
    b = np.array([line1[2], line2[2]])
    try:
        return np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return None

def is_point_feasible(point, constraints):
    if point is None:
        return False
    x1, x2 = point
    for a, b, c, op in constraints:
        val = a * x1 + b * x2
        if op == "<=" and val > c + 1e-6:
            return False
        elif op == ">=" and val < c - 1e-6:
            return False
        elif op == "=" and abs(val - c) > 1e-6:
            return False
    return True

def get_vertices(constraints):
    vertices = []
    lines = [c[:3] for c in constraints]
    for i, j in combinations(range(len(lines)), 2):
        point = find_intersection(lines[i], lines[j])
        if is_point_feasible(point, constraints):
            vertices.append(point)
    return np.array(vertices) if len(vertices) > 0 else np.array([])

def evaluate_objective(vertices, c):
    return [c[0] * x1 + c[1] * x2 for x1, x2 in vertices]

def is_infinite_solutions(vertices, values, c, constraints, objective):
    if len(vertices) < 2:
        return False, []
    optimal_value = max(values) if objective == "max" else min(values)
    optimal_points = [v for v, val in zip(vertices, values) if abs(val - optimal_value) < 1e-6]
    if len(optimal_points) >= 2:
        for constraint in constraints:
            a, b, c_val, op = constraint
            if op != "=" and all(abs(a * p[0] + b * p[1] - c_val) < 1e-6 for p in optimal_points):
                if abs(a * c[1] - b * c[0]) < 1e-6:
                    return True, optimal_points
    return False, optimal_points

def is_unbounded(constraints, c, objective):
    test_points = [
        (1000, 1000), (-1000, 1000), (1000, -1000), (-1000, -1000),
        (0, 1000), (0, -1000), (1000, 0), (-1000, 0)
    ]
    feasible_points = [p for p in test_points if is_point_feasible(p, constraints)]
    if not feasible_points:
        return False, None
    values = [c[0] * x1 + c[1] * x2 for x1, x2 in feasible_points]
    if objective == "max" and max(values) > 1e6:
        return True, np.array(feasible_points)
    elif objective == "min" and min(values) < -1e6:
        return True, np.array(feasible_points)
    grad = np.array(c)
    for a, b, _, op in constraints:
        normal = np.array([a, b])
        if op == "<=" and np.dot(grad, normal) > 1e-6:
            return True, None
        elif op == ">=" and np.dot(grad, -normal) > 1e-6:
            return True, None
    return False, None

def solve_linear_programming(constraints, c, objective):
    vertices = get_vertices(constraints)
    if len(vertices) == 0:
        # Vẫn gọi plot_feasible_region sau
        return "Miền nghiệm rỗng", None, np.array([]), None, False, [], False, None
    
    is_unb, unbounded_points = is_unbounded(constraints, c, objective)
    if is_unb:
        return "Vô nghiệm (Miền nghiệm không bị chặn)", None, vertices, None, False, [], True, unbounded_points

    values = evaluate_objective(vertices, c)
    is_inf, optimal_points = is_infinite_solutions(vertices, values, c, constraints, objective)
    optimal_value = max(values) if objective == "max" else min(values)
    if not is_inf:
        optimal_points = [v for v, val in zip(vertices, values) if abs(val - optimal_value) < 1e-6]

    return optimal_value, optimal_points, vertices, values, is_inf, optimal_points, False, None

# ======== Hàm vẽ miền nghiệm và in kết quả ========

def plot_feasible_region(constraints, vertices, optimal_points, is_infinite, is_unbounded, unbounded_points, c, objective):
    plt.figure(figsize=(8, 6))
    x1 = np.linspace(-15, 15, 400)

    # Luôn vẽ các đường ràng buộc
    for a, b, d, op in constraints:
        if b != 0:
            x2 = (d - a * x1) / b
            plt.plot(x1, x2, label=f"{a}x1 + {b}x2 {op} {d}")
        else:
            x = d / a
            plt.axvline(x, label=f"{a}x1 {op} {d}")

    # Nếu không có đỉnh hợp lệ => miền nghiệm rỗng
    if len(vertices) == 0:
        plt.title("Miền nghiệm rỗng")
    else:
        # Vẽ miền nghiệm
        hull = vertices[np.argsort(np.arctan2(vertices[:, 1] - vertices[:, 1].mean(),
                                              vertices[:, 0] - vertices[:, 0].mean()))]
        plt.fill(hull[:, 0], hull[:, 1], 'lightblue', alpha=0.5, label="Miền nghiệm khả thi")
        plt.plot(vertices[:, 0], vertices[:, 1], 'ro', label="Đỉnh")

        if is_unbounded:
            plt.title("Miền nghiệm không bị chặn")
            if unbounded_points is not None and len(unbounded_points) > 0:
                plt.plot(unbounded_points[:, 0], unbounded_points[:, 1], 'y.', alpha=0.5)
            grad = np.array(c) / np.linalg.norm(c) * 5
            if objective == "max":
                plt.arrow(0, 0, grad[0], grad[1], color='purple', width=0.1)
            else:
                plt.arrow(0, 0, -grad[0], -grad[1], color='purple', width=0.1)

        elif is_infinite and optimal_points:
            opt_array = np.array(optimal_points)
            if len(opt_array) >= 2:
                opt_array = opt_array[np.lexsort((opt_array[:, 1], opt_array[:, 0]))]
                plt.plot(opt_array[:, 0], opt_array[:, 1], 'k-', linewidth=3, label="Đoạn nghiệm tối ưu (vô số)", zorder=5)
                plt.plot(opt_array[:, 0], opt_array[:, 1])
            else:
                plt.plot(opt_array[:, 0], opt_array[:, 1], 'go', label="Điểm tối ưu (vô số)")
            plt.title("Vô số nghiệm")

        elif optimal_points:
            opt_array = np.array(optimal_points)
            plt.plot(opt_array[:, 0], opt_array[:, 1], 'g*', markersize=12, label="Điểm tối ưu")
            plt.title("Miền nghiệm và điểm tối ưu")

    # Trục, lưới, nhãn
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.grid(True)
    plt.legend()
    plt.show()

# ======== Hàm main chạy từ dòng lệnh ========

def solve(aimText, constraintText):
    objective_str = aimText.strip()
    constraintText = constraintText.split('\n')
    constraint_lines = []
    for line in constraintText:
        if not line.strip():
            break
        constraint_lines.append(line.strip())

    # Parse objective
    match = re.match(r"^(max|min)\s+([-+]?\s*\d*\.?\d*)?x1\s*([-+])\s*([-+]?\s*\d*\.?\d*)?x2$", objective_str, re.IGNORECASE)
    if not match:
        print("Hàm mục tiêu không hợp lệ.")
        return

    objective = match.group(1).lower()
    c1_str = match.group(2) or "1"  # Default to "1" if no coefficient
    sign = match.group(3)
    c2_str = match.group(4) or "1"  # Default to "1" if no coefficient

    # Handle coefficient for x1
    c1_str = c1_str.replace(" ", "")  # Remove any spaces
    if c1_str == "-":
        c1 = -1.0
    elif c1_str == "+" or c1_str == "":
        c1 = 1.0
    else:
        c1 = float(c1_str)

    # Handle coefficient for x2
    c2_str = c2_str.replace(" ", "")  # Remove any spaces
    if c2_str == "-":
        c2 = -1.0
    elif c2_str == "+" or c2_str == "":
        c2 = 1.0
    else:
        c2 = float(c2_str)
    if sign == "-":
        c2 = -c2
    c = [c1, c2]

    # Parse constraints
    constraints = []
    for line in constraint_lines:
        match_full = re.match(r"([-+]?\s*\d*\.?\d*)?x1\s*([-+])\s*([-+]?\s*\d*\.?\d*)?x2\s*(<=|>=|=)\s*([-\d.]+)", line)
        match_x1 = re.match(r"([-+]?\s*\d*\.?\d*)?x1\s*(<=|>=|=)\s*([-\d.]+)", line)
        match_x2 = re.match(r"([-+]?\s*\d*\.?\d*)?x2\s*(<=|>=|=)\s*([-\d.]+)", line)

        if match_full:
            a_str = match_full.group(1) or "1"
            a_str = a_str.replace(" ", "")
            if a_str == "-" or a_str == "-1":
                a = -1.0
            elif a_str == "+" or a_str == "" or a_str == "1":
                a = 1.0
            else:
                a = float(a_str)
            sign = match_full.group(2)
            b_str = match_full.group(3) or "1"
            b_str = b_str.replace(" ", "")
            if b_str == "-" or b_str == "-1":
                b = -1.0
            elif b_str == "+" or b_str == "" or b_str == "1":
                b = 1.0
            else:
                b = float(b_str)
            if sign == "-":
                b = -b
            op = match_full.group(4)
            d = float(match_full.group(5))
            constraints.append([a, b, d, op])
        elif match_x1:
            a_str = match_x1.group(1) or "1"
            a_str = a_str.replace(" ", "")
            if a_str == "-" or a_str == "-1":
                a = -1.0
            elif a_str == "+" or a_str == "" or a_str == "1":
                a = 1.0
            else:
                a = float(a_str)
            b = 0.0
            op = match_x1.group(2)
            d = float(match_x1.group(3))
            constraints.append([a, b, d, op])
        elif match_x2:
            a = 0.0
            b_str = match_x2.group(1) or "1"
            b_str = b_str.replace(" ", "")
            if b_str == "-" or b_str == "-1":
                b = -1.0
            elif b_str == "+" or b_str == "" or b_str == "1":
                b = 1.0
            else:
                b = float(b_str)
            op = match_x2.group(2)
            d = float(match_x2.group(3))
            constraints.append([a, b, d, op])
        else:
            print(f"Ràng buộc không hợp lệ: {line}")
            return

    result, optimal_points, vertices, values, is_infinite, _, is_unbounded, unbounded_points = solve_linear_programming(constraints, c, objective)

    if result == "Miền nghiệm rỗng":
        print(result)
        plot_feasible_region(constraints, vertices, [], False, False, None, c, objective)
        return


    if is_infinite:
        result_text = f"Giá trị tối {'đa' if objective == 'max' else 'thiểu'} Z = {result:.2f}\n"
        result_text += "Kết quả: Vô số nghiệm\n"
        result_text += "\nMột số điểm tối ưu mẫu:\n" + "\n".join(
            [f"({x1:.2f}, {x2:.2f})" for x1, x2 in optimal_points[:2]]
        )
    elif is_unbounded:
        result_text = "Miền nghiệm không bị chặn (vô nghiệm với mục tiêu ràng buộc)\n"
    else:
        result_text = f"Giá trị tối {'đa' if objective == 'max' else 'thiểu'} Z = {result:.2f}\n"
        result_text += "\nCác điểm tối ưu:\n" + "\n".join(
            [f"({x1:.2f}, {x2:.2f})" for x1, x2 in optimal_points]
        )

    result_text += "\n\nTất cả các đỉnh và Z tương ứng:\n" + "\n".join([
        f"({x1:.2f}, {x2:.2f}) -> Z = {val:.2f}" for (x1, x2), val in zip(vertices, values)
    ])
    print(result_text)
    result = solve_linear_programming(constraints, c, objective)
    optimal_value, optimal_points, vertices, values, is_infinite, optimal_points, is_unbounded, unbounded_points = result

    plot_feasible_region(constraints, vertices, optimal_points, is_infinite, is_unbounded, unbounded_points, c, objective)
if __name__ == "__main__":
    aimText = "min -x1 + x2"
    constraintText = """-x1 -2x2 <= 6
                x1 - 2x2 <= 4
                -x1 + x2 <= 1
                x1 <=0 
                x2 <= 0"""
    solve(aimText, constraintText)
