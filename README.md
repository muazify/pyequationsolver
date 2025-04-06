# Hybrid Equation Solver for 'x'

A Python script that solves mathematical equations for the variable 'x' using a hybrid approach, combining symbolic solving (for exact solutions) with numerical methods (for approximations when symbolic solving is insufficient).

## Overview

This script prompts the user to enter a single-variable equation involving 'x'. It first attempts to find exact, real solutions using the powerful symbolic mathematics library `SymPy`. If exact finite solutions cannot be found symbolically, the script falls back to a numerical root-finding algorithm (`fsolve`) from the `SciPy` library to find an approximate solution based on an initial guess.

## Benefits & Features

* **Hybrid Solving Strategy:** Leverages the strengths of both symbolic (exact) and numerical (approximate) methods. It prioritizes precise answers but provides a fallback for more complex equations.
* **Symbolic Power:** Uses `SymPy` to find exact analytical solutions where possible, handling a wide range of algebraic manipulations.
* **Numerical Robustness:** Employs `SciPy.optimize.fsolve` to find numerical approximations for equations that are difficult or impossible to solve symbolically.
* **User-Friendly Input:** Accepts equations in a natural Python/SymPy syntax (e.g., `x**2 - 4 = 0`, `sympy.sin(x) - 0.5 = 0`).
* **Clear Output:** Distinguishes between symbolically found exact solutions and numerically found approximate solutions.
* **Handles Different Formats:** Understands equations written as `expression = 0` or `lhs = rhs`.
* **Educational:** Provides a practical example of integrating symbolic and numerical computation techniques in Python.
* **Error Handling:** Includes basic error handling for parsing invalid equation inputs.

## Requirements

* Python 3.x
* NumPy
* SciPy
* SymPy

## Installation

1.  **Clone the repository (or download the script):**
    ```bash
    git clone https://github.com/muazify/pyequationsolver.git
    cd pyequationsolver
    ```
2.  **Install the required libraries using pip:**
    ```bash
    pip install numpy scipy sympy
    ```

## Usage

1.  **Run the script from your terminal:**
    ```bash
    python3 eqation.py
    ```
    
2.  **Enter the equation when prompted.** Follow the syntax guidelines:
    * Use `x` as the variable.
    * Use `**` for exponentiation (e.g., `x**2` for x squared).
    * Use `*` for multiplication (e.g., `5*x`).
    * Use `sympy.` prefix for mathematical functions like `sympy.sqrt()`, `sympy.sin()`, `sympy.exp()`, `sympy.log()`, `sympy.factorial()`.
        * Alternatively, pre-calculate simple constants (e.g., use `6` instead of `sympy.factorial(3)` if you know the value).
    * You can enter the equation as `expression` (implicitly assuming `expression = 0`) or as `lhs = rhs`.

**Examples:**

* `1 + x = 4`
* `x**2 - 5*x + 6 = 0`
* `sympy.exp(x) - 10 = 0`
* `sympy.sqrt(x) = 5`
* `sympy.sin(x) - x/2 = 0` (This will likely require numerical solving)

The script will first attempt symbolic solving. If it finds exact real solutions, it will print them. If not, or if the symbolic solution is complex (like a conditional set), it will proceed to numerical solving using `fsolve` with an initial guess (currently hardcoded as `1.0`).

## How it Works

1.  **Input & Parsing:** The script takes the equation as a string input. `SymPy`'s `sympify` function parses this string into a symbolic mathematical expression. It handles both `expression = 0` and `lhs = rhs` formats by converting them into a single expression assumed to be equal to zero (`expression = lhs - rhs`).
2.  **Symbolic Solving:** `SymPy`'s `solveset` function is used to find the set of values for `x` that make the expression equal to zero, specifically searching within the domain of real numbers (`sympy.S.Reals`).
3.  **Numerical Solving (Fallback):**
    * If `solveset` does not return a finite set of solutions (e.g., it finds no solutions, returns an interval, or a conditional set), the script prepares for numerical solving.
    * `SymPy`'s `lambdify` function converts the symbolic expression into a Python function suitable for fast numerical evaluation using `NumPy`.
    * `SciPy`'s `fsolve` function is called. This is an iterative root-finding algorithm that starts from an `initial_guess` and tries to find a value of `x` where the numerical function is close to zero.
4.  **Output:** The script reports any solutions found, clearly indicating whether they are symbolic (exact) or numerical (approximate).

## Limitations

* **Numerical Guess:** The `fsolve` function requires an initial guess. The quality of this guess can significantly impact whether a solution is found and *which* solution is found if multiple exist. The current script uses a fixed guess (`1.0`). For difficult equations, you might need to modify the script to change this guess.
* **Real Solutions Only:** The symbolic solver (`solveset`) is currently configured to search only for real solutions (`domain=sympy.S.Reals`).
* **Solver Capabilities:** Neither `solveset` nor `fsolve` can solve *all* possible equations. Very complex or pathological equations might fail in both symbolic and numerical stages.
* **Parsing Complexity:** While `sympify` is powerful, extremely complex or ambiguously written input strings might cause parsing errors.
