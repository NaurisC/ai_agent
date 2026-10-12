from pkg.calculator import Calculator

calc = Calculator()
result = calc.evaluate("3 + 7 * 2")
print(f"3 + 7 * 2 = {result}")

result2 = calc.evaluate("3 * 4 + 5")
print(f"3 * 4 + 5 = {result2}")

result3 = calc.evaluate("2 * 3 - 8 / 2 + 5")
print(f"2 * 3 - 8 / 2 + 5 = {result3}")