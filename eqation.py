import sympy
from scipy.optimize import fsolve
import numpy as np
import math # For functions like factorial if needed BEFORE passing to sympy

def solve_for_x():
    """
    Attempts to solve an equation for the variable 'x' using symbolic
    and potentially numerical methods.
    """
    print("------------------------------------")
    print("Equation Solver for 'x'")
    print("------------------------------------")
    print("Enter the equation. Use Python/SymPy syntax:")
    print("  - Use 'x' as the variable.")
    print("  - Use '**' for exponentiation (e.g., x**2 for x squared).")
    print("  - Use functions like sympy.sqrt(), sympy.sin(), sympy.exp(), sympy.log(), sympy.factorial()")
    print("    (or pre-calculate numbers like 3! = 6 before entering).")
    print("  - Examples: ")
    print("    1 + x = 4")
    print("    x**2 - 5*x + 6 = 0")
    print("    sympy.sqrt(x) - 5 = 0")
    print("    sympy.Eq(sympy.sqrt((x+4)**5 - x + sympy.factorial(3)), 50)") # Explicit Eq object
    print("    sqrt((x+4)**5 - x + 6) - 50 = 0") # Assuming expression = 0
    print("------------------------------------")

    equation_str = input("Enter equation: ").strip()

    if not equation_str:
        print("No equation entered.")
        return

    # Define the symbol 'x'
    x = sympy.symbols('x')
    symbolic_solutions = None
    numerical_solution_val = None
    equation_expr = None # To store the expression f(x) for f(x)=0

    # --- Symbolic Solving Attempt ---
    print("\n--- Attempting Symbolic Solution (Exact) ---")
    try:
        # Try parsing the input string into a SymPy object
        # Using sympify is generally robust but can be tricky with complex inputs
        # We can handle two forms: 'lhs = rhs' or just 'expression' (assumed == 0)

        if '=' in equation_str and '==' not in equation_str: # Avoid confusion with logical equals
             # Handle 'lhs = rhs' format by creating an Eq object
             lhs_str, rhs_str = equation_str.split('=', 1)
             lhs = sympy.sympify(lhs_str, locals={'x': x, 'sympy': sympy, 'math': math})
             rhs = sympy.sympify(rhs_str, locals={'x': x, 'sympy': sympy, 'math': math})
             # Use solveset with Eq object or create expression = 0
             # equation_obj = sympy.Eq(lhs, rhs) # Can use this with solveset too
             equation_expr = lhs - rhs # For solveset and numerical solver: expr = 0
        else:
             # Assume 'expression = 0' format
             # Replace logical == with 0 if user typed it
             equation_str_expr = equation_str.replace('==', '-')
             equation_expr = sympy.sympify(equation_str_expr, locals={'x': x, 'sympy': sympy, 'math': math})

        # Use solveset for potentially more robust solving over solve
        # Domain S.Reals looks for real solutions. Use S.Complex for complex solutions.
        symbolic_solutions = sympy.solveset(equation_expr, x, domain=sympy.S.Reals)

        if symbolic_solutions.is_FiniteSet and symbolic_solutions:
            print("Symbolic Solution(s) found:")
            # Convert SymPy Floats/Integers to standard Python types for cleaner printing
            solutions_list = [float(s) if s.is_Float else int(s) if s.is_Integer else s for s in symbolic_solutions]
            print(solutions_list)
            # If we found exact solutions, we might not need numerical ones.
            # For demonstration, we'll proceed to numerical anyway, but you could exit here.

        elif isinstance(symbolic_solutions, sympy.sets.conditionset.ConditionSet):
             print("Symbolic solver returned a conditional solution set:")
             print(symbolic_solutions)
             print("This often means numerical methods are needed for specific values.")

        elif symbolic_solutions.is_EmptySet:
            print("Symbolic solver found no real solutions.")

        else: # Could be Interval, ImageSet etc.
            print("Symbolic solver returned a non-finite set (e.g., an interval):")
            print(symbolic_solutions)


    except (sympy.SympifyError, TypeError, SyntaxError) as e:
        print(f"Error parsing equation: {e}")
        print("Please check syntax (use '**' for powers, ensure balanced parentheses).")
        equation_expr = None # Ensure numerical part doesn't run
    except Exception as e:
        print(f"An unexpected error occurred during symbolic solving: {e}")
        # Proceed to numerical attempt if equation_expr was parsed

    # --- Numerical Solving Attempt (Fallback) ---
    # Only attempt if symbolic solving didn't find a finite set or failed,
    # and if the expression was parsed successfully.
    if equation_expr is not None and (not symbolic_solutions or not symbolic_solutions.is_FiniteSet):
        print("\n--- Attempting Numerical Solution (Approximate) ---")
        try:
            # Convert the SymPy expression into a Python function for numerical evaluation
            # We need the expression that equals zero (equation_expr)
            numeric_func = sympy.lambdify(x, equation_expr, 'numpy')

            # Numerical solvers need an initial guess. This is CRITICAL.
            # A bad guess might lead to no solution or a different solution.
            initial_guess = 1.0 # Default guess, might need changing!
            print(f"Using initial guess for x = {initial_guess}")
            print("(If solver fails or finds an unexpected root, try changing this guess)")

            # Use fsolve from SciPy. It finds roots of func(x) = 0.
            numerical_solution, info_dict, ier, msg = fsolve(numeric_func, initial_guess, full_output=True)

            if ier == 1: # ier=1 means solution found
                 solution_val = numerical_solution[0]
                 # Verify the solution (check if f(solution) is close to zero)
                 if np.isclose(numeric_func(solution_val), 0):
                      print(f"Numerical Solution found: x ≈ {solution_val:.8f}")
                      numerical_solution_val = solution_val
                 else:
                      print(f"Numerical solver converged, but result {solution_val:.8f} doesn't precisely satisfy the equation (f(x)={numeric_func(solution_val):.2e}). May be due to limitations.")
            else:
                print(f"Numerical solver did not converge or failed.")
                print(f"Solver message: {msg}")

        except NameError:
            print("Error: SciPy library not found. Please install it (`pip install scipy`).")
        except TypeError as e:
             print(f"Error during numerical evaluation: {e}")
             print("This can happen if the expression still contains symbolic parts or uses unsupported functions.")
        except Exception as e:
            print(f"An unexpected error occurred during numerical solving: {e}")

    print("\n------------------------------------")
    print("Solver finished.")
    print("------------------------------------")


# Run the solver
if __name__ == "__main__":
    solve_for_x()
