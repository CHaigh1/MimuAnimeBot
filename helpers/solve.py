def solveInput(num1, sign, num2):
    if sign == '+':
        return num1 + num2
    elif sign == '-':
        return num1 - num2
    elif sign == '*':
        return num1 * num2
    elif sign == 'x':
        return num1 * num2
    elif sign == '/':
        return num1 / num2
    else:
        return 'not a valid sign'