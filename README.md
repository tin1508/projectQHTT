# projectQHTT

## Overview
The project is a desktop application designed to solve problems relating to Linear Programming mathematical model. It provides an efficient and structured way to input complex mathematical constraints, run optimization algorithm, and output actionable, optimal solutions for decision-making scenarios.

## Features
* **Model Parsing & Processing:** Efficiently reads and structures standard linear programming equations and constraints.
* **Optimization Engine:** Implements core mathematical solvers (e.g., the Simplex algorithm) to find maximum or minimum objective values.
* **Data Persistence:** Safely logs historical run data, problem sets, and solver results for future review.
* **Clean Architecture:** Separates business logic from the user interface, ensuring scalable and maintainable code.

## Tech Stacks
* **Core Framework & Querying:** C# / .NET utilizing LINQ for robust data manipulation.
* **Architecture Pattern:** MVVM (Model-View-ViewModel) for a clean separation of concerns.
* **Database:** MySQL for relational data storage.
* **Environment & Tools:** Docker for containerization and Postman for environment testing and API validation.

## Which problems does it handle?
This project is explicitly built to handle mathematical optimization scenarios, helping users make the best possible decisions given strict limitations. It handles:
1. **Resource Allocation:** Maximizing profit or total output when constrained by limited materials, budget, or time.
2. **Cost Minimization:** Finding the absolute cheapest combination of inputs (like ingredients or shipping routes) that still meets a required baseline.
3. **Logistics & Network Flow:** Determining the most efficient routing configurations to eliminate bottlenecks.

## How to set up the program

### Prerequisites
* Ensure you have [Docker](https://www.docker.com/) installed and running on your machine.
* A local or containerized instance of MySQL.

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/tin1508/projectQHTT.git](https://github.com/tin1508/projectQHTT.git)
   cd projectQHTT

