# Linear Programming Program 📈
The project is a desktop application designed to solve problems relating to Linear Programming mathematical model. It provides an efficient and structured way to input complex mathematical constraints, run optimization algorithm, and output actionable, optimal solutions for decision-making scenarios.

## 📌 Table of Contents
* [Key Features](#-key-features)
* [Tech Stack](#%EF%B8%8F-tech-stack)
* [Technical Deep Dive](#-technical-deep-dive)
* [Getting Started](#-getting-started)
* [Collaborators](#-collaborators)

## 🚀 Key Features
* **Standard & Canonical Forms (`Chinh_Tac.py`, `Chuan_Tac.py`):** Automatically converts user-inputted linear programming problems into their Standard (Chính tắc) or Canonical (Chuẩn tắc) forms, which is a required prerequisite for algorithmic solving.
* **Simplex Algorithm Implementations (`DonHinh_Bland_2Pha.py`):** Features robust mathematical solvers, specifically implementing the Two-Phase Simplex method (Đơn hình 2 pha) and Bland's Rule to prevent cycling during optimization.
* **Graphical Method & Coordinate Geometry (`HinhHoc_ToaDo.py`):** Provides a visual/geometric approach to solving 2-variable linear programming problems by finding intersection points and evaluating the objective function at the vertices of the feasible region.
* **Input Processing (`Xu_Ly_Dau_Vao.py`):** Safely parses, validates, and structures raw mathematical strings or matrices provided by the user into usable data arrays.
* **User Interface (`GiaoDien.py`, `main.py`):** Includes a frontend interface that allows users to interact with the underlying mathematical models without needing to write code.

## 🛠️ Tech Stack
**Core Language:**
* Python3
**Libraries & Components:**
* **NumPy:** For high-performance matrix manipulation and linear algebra operations.
* **UI Framework:** PyQt for building the desktop graphical user interface.
* **Data Visualization:** Matplotlib for rendering the 2D coordinate geometry graphs.

## ✨Which problems does it handle?
This project is explicitly built to handle mathematical optimization scenarios, helping users make the best possible decisions given strict limitations. It handles:
1. **Resource Allocation:** Maximizing profit or total output when constrained by limited materials, budget, or time.
2. **Cost Minimization:** Finding the absolute cheapest combination of inputs (like ingredients or shipping routes) that still meets a required baseline.
3. **Logistics & Network Flow:** Determining the most efficient routing configurations to eliminate bottlenecks.

## ⚙️How to set up the program
### Prerequisites
* Python 3.4 or later
* If you don't install pip yet, let's install it by python get-pip.py. You can check python version by python --version and pip by pip --version before.
* After installing pip successfully:
   * Install numpy

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tin1508/projectQHTT.git](https://github.com/tin1508/projectQHTT.git)
   cd projectQHTT

