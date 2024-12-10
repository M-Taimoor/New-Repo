import ast

class LambdaSyntaxChecker(ast.NodeVisitor):
    """
    Custom visitor class to check for common syntax errors in lambda functions.
    """
    
    def visit_Lambda(self, node):
        """
        Visit Lambda nodes and check for syntax errors.
        """
        # Check for missing parentheses around arguments
        if not isinstance(node.args, ast.Lambda):
            raise SyntaxError("Lambda function arguments must be enclosed in parentheses")
        
        # Check for incorrect argument syntax
        if not isinstance(node.args.args, (ast.Name, ast.Tuple)):
            raise SyntaxError("Lambda function arguments must be simple names or tuples")
        
        # Check for missing return statement (implicit return)
        if not isinstance(node.body, ast.Expr):
            raise SyntaxError("Lambda function body must be a single expression")
        
        # Visit the body of the lambda function
        self.visit(node.body)

def check_lambda_syntax(lambda_str):
    """
    Check the syntax of a lambda function string and raise a SyntaxError if any errors are found.
    """
    try:
        # Parse the lambda function string into an AST
        lambda_ast = ast.parse(lambda_str)
        
        # Create an instance of the LambdaSyntaxChecker class and visit the AST
        checker = LambdaSyntaxChecker()
        checker.visit(lambda_ast)
        
        # If no syntax errors were found, return True
        return True
    except SyntaxError as e:
        # If a syntax error was found, print the error message and return False
        print(f"Syntax error: {e}")
        return False

# Example usage
lambda_str1 = "lambda x, y: x + y"
lambda_str2 = "lambda x, y: x + y *"
lambda_str3 = "lambda x, y: if x > y: x else: y"

if check_lambda_syntax(lambda_str1):
    print("Lambda function syntax is correct!")
else:
    print("Lambda function syntax is incorrect.")

if check_lambda_syntax(lambda_str2):
    print("Lambda function syntax is correct!")
else:
    print("Lambda function syntax is incorrect.")

if check_lambda_syntax(lambda_str3):
    print("Lambda function syntax is correct!")
else:
    print("Lambda function syntax is incorrect.")