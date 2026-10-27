def basic_calculate():
    """Evaluates a basic mathematical expression entered by the user."""
    print("\n--- Basic Calculator ---")
    expression = input("Enter a basic math expression (e.g., 5 + 5 or 10 * 2.5): ")
    try:
        # eval() processes the string as a Python math expression
        result = eval(expression)
        print(f"Result: {result}")
    except Exception as e:
        print("Error: Invalid mathematical expression.")


def solve_for_x(expression, target):
    """
    Brute-force search: tries every value of x from -100 to 100 
    in steps of 0.1 to find the result closest to the target.
    """
    best_x = 0
    smallest_error = float('inf')
    
    x = -100.0
    while x <= 100.0:
        try:
            # Safely replace 'x' with the current loop value in parentheses
            test_expr = expression.replace('x', f"({x})")
            result = eval(test_expr)
            
            # Calculate how far off this result is from our target
            error = abs(result - target)
            
            # If this is the closest we've gotten, save it
            if error < smallest_error:
                smallest_error = error
                best_x = x
        except Exception:
            pass # Ignore syntax errors for invalid replacements
        
        # Step by 0.1 and round to avoid floating-point drift (e.g., 0.1000000001)
        x += 0.1
        x = round(x, 1)
        
    return best_x


def visualize_search():
    """Runs a smaller brute-force search and prints every step to the console."""
    print("\n--- Search Visualisation ---")
    print("Note: Using valid Python syntax. Example: '2*x + 5'")
    expression = input("Enter the expression containing 'x': ")
    
    try:
        target = float(input("What should this expression equal?: "))
    except ValueError:
        print("Invalid target number.")
        return

    best_x = 0
    smallest_error = float('inf')
    
    # We use a smaller range (-10 to 10) here so the terminal doesn't flood with 2000 lines
    x = -10.0
    print("\nStarting visual search from x = -10.0 to 10.0...")
    while x <= 10.0:
        try:
            test_expr = expression.replace('x', f"({x})")
            result = eval(test_expr)
            error = abs(result - target)
            
            # Print exactly what the algorithm is 'thinking'
            print(f"Trying x = {x:5.1f} | Result = {result:8.2f} | Distance from target = {error:8.2f}")
            
            if error < smallest_error:
                smallest_error = error
                best_x = x
        except Exception:
            pass
        
        x += 0.1
        x = round(x, 1)
        
    print(f"\nSearch complete. Closest match found: x = {best_x}")


def equation_solver_menu():
    """Prompts the user for equation details and calls the solver."""
    print("\n--- Equation Solver ---")
    print("Note: Use valid Python syntax. Example: '2*x + 5'")
    expression = input("Enter the expression containing 'x': ")
    
    try:
        target = float(input("What should this expression equal? (target value): "))
        print("Searching for the answer...")
        answer = solve_for_x(expression, target)
        print(f"The closest value for x is: {answer}")
    except ValueError:
        print("Error: Please enter a valid number for the target.")


def main():
    while True:
        print("\n=== Smart Calculator Menu ===")
        print("1. Basic calculation")
        print("2. Equation solver")
        print("3. Search visualisation")
        print("4. What is a search algorithm?")
        print("5. Exit")
        
        choice = input("Select an option (1-5): ")
        
        if choice == '1':
            basic_calculate()
        elif choice == '2':
            equation_solver_menu()
        elif choice == '3':
            visualize_search()
        elif choice == '4':
            print("\n--- What is a search algorithm? ---")
            print("A search algorithm looks for a solution by methodically exploring possibilities.")
            print("Our equation solver uses a 'brute-force' search: it blindly tries every single")
            print("decimal from -100 to 100 without any cleverness. While it eventually finds the")
            print("answer, checking 2,000 possibilities is inefficient. Modern search algorithms,")
            print("like binary search, are smarter—they look at the error distance and adjust their")
            print("next guess accordingly to find the exact answer almost instantly.")
        elif choice == '5':
            print("Exiting calculator. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()