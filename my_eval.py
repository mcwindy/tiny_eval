base = 10  # 2到36
operators = {'+': '__add__', '-': '__sub__', '*': '__mul__',
             '%': '__mod__', '/': '__floordiv__', '**': lambda a, b: int(pow(a, b))}
trace = True


def handle_lexical(formula: str):
    digits = list(map(chr, [*range(ord('0'), ord('9') + 1), *range(ord('a'), ord('z') + 1)]))[:base]

    while '  ' in formula:
        formula.replace('  ', ' ')
    formula = formula.replace('  ', ' ')
    for i in range(len(formula) - 1):
        if formula[i] == ' ' and formula[i - 1] in operators and formula[i + 1] in operators:
            raise SyntaxError('Space between operators error')
    formula = '(' + formula.replace(' ', '') + ')'

    l, cur, empty, i, le = [], '', True, 0, len(formula)

    while i < le:
        if formula[i] in digits:
            empty, cur = False, cur + formula[i]
        elif formula[i] in list(operators) + ['(', ')']:
            if not empty:
                l.append(int(cur, base))
                cur = ''
                empty = True
            if formula[i:i + 2] in operators:
                l.append(formula[i:i + 2])
                i += 1
            elif formula[i] in operators and formula[i + 1] in operators:
                raise SyntaxError('Invalid operator: ' + formula[i:i + 2])
            else:
                l.append(formula[i])
        else:
            raise SyntaxError('Invalid operator: ' + formula[i])
        i += 1
    return l


def handle_syntax(l: list):
    def parser(text):
        if text == None:
            return []
        elif text == '(':
            subs = []
            while True:
                try:
                    text = next(l)
                except StopIteration:
                    raise SyntaxError('Unexcepted EOL found')
                if text == ')':
                    break
                subs.append(parser(text))
            if text != ')':
                raise SyntaxError(f'Unexcepted EOL found')
            if not subs:
                raise SyntaxError('Empty () found')
            return subs
        elif text == ')':
            raise SyntaxError('Unexcepted ")" token')
        else:
            return text
    l = iter(l)
    res = parser(next(l))
    return res


def handle_semantic(t, eval_level=1):
    global trace
    if trace and list_checker(t) > 1:
        print('\t' * (eval_level - 1) + "eval " + repr_list(t))
        trace = True

    a = term(t, eval_level)
    while list_checker(t) and t[0] in '+-':
        func = operators[t.pop(0)]
        c = term(t, eval_level)
        if not isinstance(c, int):
            raise SyntaxError("Invalid operand")
        a = update(func, a, c)
    if trace:
        print('\t' * (eval_level - 1) + "eval result:[" + str(a) + ']')
    return a


list_checker = lambda x: len(x) if isinstance(x, list) else 0
update = lambda f, x, y: getattr(x, f)(y) if isinstance(f, str) else f(x, y)
repr_list = lambda l, sep=' ', s='': '[' + [s := s + sep +
                                            (repr_list(x, sep) if isinstance(x, list) else str(x)) for x in l][0][len(sep):] + ']'


def factor(tree, eval_level):  # 求解子表达式
    r = tree.pop(0)
    if isinstance(r, list):
        r = handle_semantic(r, eval_level + 1)
    else:
        assert isinstance(r, int), f'[{r}] should be a number'
    return r


def term(tree, eval_level):  # 计算高优先级运算
    a = factor(tree, eval_level)
    while isinstance(a, int) and list_checker(tree) and tree[0] in list(operators)[2:]:
        func = operators[tree.pop(0)]
        c = factor(tree, eval_level)
        if not isinstance(c, int):
            raise SyntaxError("Invalid operand")
        a = update(func, a, c)
    return a


def execute(formula):
    funcs = ['handle_lexical', 'handle_syntax', 'handle_semantic']
    [formula := eval(func)(formula) for func in funcs]
    return formula


def test():
    formulas = [
        '1+ 2*3',
        '(1 + 2) * 3',
        '106 + 7 * (5 - 2)',
        '(((3+2)*3)*5-7) - (6 *(3+8)/2)',
        '(3*6)**4-114',

        # '(1+2',
        # '517  **  90+4--2'
        # '(((3+2)*3)*5-7) - (6 *(3+8)2)',  # innvalid
        # '() + 66',  # innvalid
    ]
    for f in formulas:
        print(execute(f))


if __name__ == '__main__':
    # test()
    while True:
        s = input('>')
        if s == 'exit()':
            print('Exiting.')
            exit(0)
        execute(s)
