import re

# Token types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
TIMES = 'TIMES'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'     #end of file - end of the input string

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def get_next_token(self):
        if self.pos >= len(self.text):
            return Token(EOF, None)

        current_char = self.text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        elif current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        elif current_char == '*':
            token = Token(TIMES, current_char)
            self.pos += 1
            return token
        elif current_char == '(':
            token = Token(LPAREN, current_char)
            self.pos += 1
            return token
        elif current_char == ')':
            token = Token(RPAREN, current_char)
            self.pos += 1
            return token

        self.error()

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        result = self.factor()

        while self.current_token.type in (TIMES,):
            token = self.current_token
            if token.type == TIMES:
                self.eat(TIMES)
                result *= self.factor()

        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS,):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()

        return result

def evaluate(expression):
    lexer = Lexer(expression)
    parser = Parser(lexer)
    result = parser.expr()
    return result

def main():
    while True:
        try:
            expression = input("Enter your expression input: ")
            result = evaluate(expression)
            print("Result:", result)
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    main()

class Parser:
    # Existing code...

    def prefix_expr(self):
        result = ''

        while self.current_token.type != EOF:
            token = self.current_token

            if token.type == INTEGER:
                result += str(token.value)
                self.eat(INTEGER)
            elif token.type in (PLUS, TIMES):
                result += token.value
                self.eat(token.type)
            elif token.type == LPAREN:
                result += '('
                self.eat(LPAREN)
            elif token.type == RPAREN:
                result += ')'
                self.eat(RPAREN)

        return result

    def postfix_expr(self):
        output = []
        stack = []

        precedence = {
            PLUS: 1,
            TIMES: 2,
        }

        while self.current_token.type != EOF:
            token = self.current_token

            if token.type == INTEGER:
                output.append(str(token.value))
                self.eat(INTEGER)
            elif token.type in (PLUS, TIMES):
                while stack and precedence.get(stack[-1]) >= precedence.get(token.type):
                    output.append(stack.pop())
                stack.append(token.value)
                self.eat(token.type)
            elif token.type == LPAREN:
                stack.append(token.value)
                self.eat(LPAREN)
            elif token.type == RPAREN:
                while stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Discard the '('
                self.eat(RPAREN)

        while stack:
            output.append(stack.pop())

        return ' '.join(output)

def evaluate(expression):
    lexer = Lexer(expression)
    parser = Parser(lexer)
    result = parser.expr()
    prefix_result = parser.prefix_expr()
    postfix_result = parser.postfix_expr()
    return result, prefix_result, postfix_result

# Main function remains the same...

