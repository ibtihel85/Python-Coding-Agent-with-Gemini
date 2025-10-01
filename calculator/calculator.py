def calculate(expression):
    # WARNING: Using eval() can be dangerous if the input expression is not sanitized.
    # It can execute arbitrary code.
    result = eval(expression)
    return result

# expression = "3 + 7 * 2"
# print(calculate(expression))