# GitHub Copilot Experience

## What worked well
1. **Boilerplate generation:** Once I wrote the `main()` function's `while True:` loop and the first print statement, Copilot correctly predicted the rest of the menu options and print statements almost perfectly.
2. **Try/Except blocks:** When writing `basic_calculate()`, I typed `try:` and Copilot immediately suggested the correct `eval(expression)` logic and the corresponding `except Exception as e:` block to handle invalid math inputs. 
3. **String formatting:** When I was writing the `visualize_search()` function, Copilot suggested great f-string formatting (`{x:5.1f}` and `{result:8.2f}`) to keep the console output aligned in neat columns, which I wouldn't have thought to do right away.

## Challenges
1. **Looping with floats:** Copilot originally suggested a standard `for` loop with `range(-100, 100)`, but Python's `range()` function does not support decimal steps like `0.1`. It took some back-and-forth to get it to build a `while` loop that manually iterated `x += 0.1`.
2. **Dangerous functions:** Copilot suggested using `eval()` to execute the math strings. While it works perfectly for this project, I know from class materials that passing raw user input directly into `eval()` is generally a security risk in production applications.

## My Judgement (Where I rejected or changed suggestions)
1. **Floating-point drift:** Copilot's suggested `while x <= 100.0:` loop had a math quirk where adding `0.1` repeatedly resulted in weird numbers like `2.000000000000001` instead of `2.1`. I had to manually intervene and add `x = round(x, 1)` at the end of the loop to force the numbers to stay clean.
2. **Variable replacement:** Copilot suggested using `expression.replace('x', str(x))`. I rejected this and changed it to `expression.replace('x', f"({x})")`. Without the parentheses, if a user typed `x**2` and `x` was negative, it evaluated `-5**2` (which is -25 in Python) instead of `(-5)**2` (which is 25). Wrapping the replacement in parentheses fixed the order of operations.