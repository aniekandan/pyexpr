import re

keywords = {
        '+': 'PLUS', 
        '-': 'MINUS', 
        '*': 'TIMES', 
        '/': 'DIVIDE', 
        '=': 'ASSIGNMENT', 
        '(': 'LPAREN', 
        ')': 'RPAREN'
    }

float_regex = r'\d+(\.\d+)?'
identifier_regex = r'[a-zA-Z][a-zA-Z0-9]*'

regex = '|'.join([re.escape(k) for k in keywords.keys()] + [float_regex, identifier_regex])

def tokenize(input_string):
    tokens = []
    
    for match in re.finditer(regex, input_string):
        token_type = keywords.get(match.group(), None)

        if not token_type:
            if re.match(float_regex, match.group()):
                token_type = 'FLOAT_NUM'
            elif re.match(identifier_regex, match.group()):
                token_type = 'IDENTIFIER'
            else:
                raise ValueError(f"Unexpected character: {match.group()}")

        tokens.append((token_type, match.group()))

    tokens.append(("EOS", None))
    return tokens
