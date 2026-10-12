
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Cannot pop from an empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0


def precedence(operator):
    if operator in ("+", "-"):
        return 1
    elif operator in ("*", "/"):
        return 2
    return 0


def apply_operator(values, operators):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()

    if operator == "+":
        values.push(left + right)
    elif operator == "-":
        values.push(left - right)
    elif operator == "*":
        values.push(left * right)
    elif operator == "/":
        if right == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        values.push(left / right)


def evaluate_expression(expression):
    values = Stack()
    operators = Stack()

    tokens = expression.replace("(", " ( ").replace(")", " ) ").split()

    for token in tokens:
        if token.isdigit():
            values.push(int(token))

        elif token == "(":
            operators.push(token)

        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(values, operators)

            if operators.is_empty():
                raise ValueError("Mismatched parentheses")

            operators.pop()

        elif token in ("+", "-", "*", "/"):
            while (
                not operators.is_empty()
                and operators.peek() != "("
                and precedence(operators.peek()) >= precedence(token)
            ):
                apply_operator(values, operators)

            operators.push(token)

        else:
            raise ValueError(f"Invalid token: {token}")

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("Mismatched parentheses")

        apply_operator(values, operators)

    if len(values.items) != 1:
        raise ValueError("Invalid mathematical expression")

    return values.pop()


def process_files():
    input_file = "input.txt"
    output_file = "output.txt"

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        results = []

        for line in lines:
            expression = line.strip()

            if not expression:
                results.append("")
            elif all(character == "-" for character in expression):
                results.append(expression)
            else:
                try:
                    answer = evaluate_expression(expression)

                    if isinstance(answer, float) and answer.is_integer():
                        answer = int(answer)

                    results.append(str(answer))

                except (ValueError, ZeroDivisionError, IndexError) as error:
                    results.append(f"Error: {error}")

        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(results))

        print("Expressions evaluated successfully!")
        print("Results saved to output.txt")

    except FileNotFoundError:
        print("Error: input.txt was not found.")
        print("Make sure input.txt is in the same folder as main.py.")


if __name__ == "__main__":
    process_files()