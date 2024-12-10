import ast

def validate_lambda_syntax(lambda_expr):
    """
    Validates the syntax of a lambda function expression.

    Parameters:
    lambda_expr (str): The lambda function expression to validate.

    Returns:
    bool: True if the lambda function syntax is valid, False otherwise.
    """
    try:
        # Attempt to parse the lambda function expression into an AST
        lambda_ast = ast.parse(lambda_expr, mode='eval')

        # Check if the AST body is a Lambda function
        if not isinstance(lambda_ast.body, ast.Lambda):
            raise SyntaxError(f"Invalid syntax: '{lambda_expr}' is not a lambda function.")

        # Check if the lambda function has at least one argument
        if len(lambda_ast.body.args.args) < 1:
            raise SyntaxError("Lambda function must have at least one argument.")

        # If the lambda expression is valid, return True
        return True

    except SyntaxError as e:
        print(f"Syntax error: {e}")
        return False
    except ValueError as e:
        print(f"Value error: {e}. This might indicate a malformed expression.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


# Example usage
lambda_exprs = [
    "lambda x: x + 1",  # Valid
    "lambda x, y: x + y",  # Valid
    "lambda: 42",  # Invalid: Missing argument
    "lambda x: x +",  # Invalid: Incomplete expression
    "lambda x: if x > 0: x else: -x"  # Invalid: Syntax error with if-else
]

for lambda_expr in lambda_exprs:
    if validate_lambda_syntax(lambda_expr):
        print(f"'{lambda_expr}' is valid.")
    else:
        print(f"'{lambda_expr}' is invalid.")
