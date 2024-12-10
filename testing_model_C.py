import ast


def verify_lambda_syntax(lambda_str):
    """
    Verifies the syntax of a lambda function string.

    Args:
        lambda_str (str): The lambda function string to verify.

    Returns:
        bool: True if the lambda function has valid syntax, False otherwise.
    """
    try:
        # Parse the lambda function string into an AST
        lambda_ast = ast.parse(lambda_str)

        # Check if the AST represents a lambda function
        if not isinstance(lambda_ast, ast.Lambda):
            raise SyntaxError("Not a lambda function")

        # Check if the lambda function has a single expression
        if len(lambda_ast.body) != 1:
            raise SyntaxError("Lambda function must have a single expression")

        # Check if the lambda function has any arguments
        if not lambda_ast.args.args:
            raise SyntaxError("Lambda function must have at least one argument")

        # Check if the lambda function has a valid expression
        ast.dump(lambda_ast.body[0])

        return True
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        return False


# Example usage
lambda_str = "lambda x: x + 1"
if verify_lambda_syntax(lambda_str):
    print("Lambda function has valid syntax")
else:
    print("Lambda function has invalid syntax")