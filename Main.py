import string
from treelib import Tree

# Please first install TreeLib. its the one help generate the parse tree.
# pip install treelib

parse_tree = Tree()
parse_tree.create_node('Program', 'program')

Keywords = ['Num']
Operators = ['+', '-', '*', '/', '=']
Numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
Identifiers = ['a', 'b', 'c', 'x', 'y', 'z']

validity = True


def get_token_type(lx):
    if lx in Keywords:
        print('Type : Keyword ⟶ {TK}'.format(TK=lx))
        return 'Keyword'
    elif lx in Operators:
        print('Type : Operator ⟶ {TK}'.format(TK=lx))
        return 'Operator'
    elif lx in Numbers:
        print('Type : Number ⟶ {TK}'.format(TK=lx))
        return 'Number'
    elif lx in Identifiers:
        print('Type : Identifier ⟶ {TK}'.format(TK=lx))
        return 'Identifier'
    else:
        return 'Not_A_Token'


symbol_table = []


def get_token(sub_code):
    index = 1
    token_position = 0
    print('Symbols Table :')
    while index <= len(sub_code):
        lx = sub_code[:index]
        lx_type = get_token_type(lx)
        if lx_type != 'Not_A_Token':
            sub_code = sub_code[index:]
            index = 0
            symbol_table.append({
                'Token': lx,
                'Type': lx_type,
                'Position': token_position
            })
            token_position += 1
        index += 1
    parse_tree_maker()


def parse_tree_right_maker(index_token, token_tree):
    global validity
    must_num = token_tree[0::2]
    must_op = token_tree[1::2]
    is_right_valid = True
    for tks in must_num:
        if tks['Type'] != 'Number':
            is_right_valid = False
            break
    for tks in must_op:
        if tks['Type'] != 'Operator':
            is_right_valid = False
            break
    if not is_right_valid:
        validity = False
        print('====> Invalid Input. Expecting a Number below 10 or a Operator <====')
    parse_tree.create_node('Expression', 'expression-r-{i}'.format(i=index_token), parent='program')
    parse_tree.create_node('Term', 'term-r-{i}{i}'.format(i=index_token),
                           parent='expression-r-{i}'.format(i=index_token))
    index_r = 99
    for tks in token_tree:
        parse_tree.create_node('{Type} - {ID}'.format(Type=tks['Type'], ID=tks['Token']),
                               '{Type}-r-{i}{i}{i}'.format(Type=tks['Type'], i=index_r),
                               parent='term-r-{i}{i}'.format(i=index_token))
        index_r += 1


def parse_tree_maker():
    global validity
    token = symbol_table[0]
    index_token = symbol_table.index(token)
    next_token = symbol_table[symbol_table.index(token) + 1]
    next_next_token = symbol_table[symbol_table.index(token) + 2]
    if token['Token'] == 'Num':
        if next_token['Type'] == 'Identifier' and next_next_token['Token'] == '=':
            parse_tree.create_node('Expression', 'expression-{i}'.format(i=index_token), parent='program')
            parse_tree.create_node('Term', 'term-{i}{i}'.format(i=index_token),
                                   parent='expression-{i}'.format(i=index_token))
            parse_tree.create_node('Keyword - {ID}'.format(ID=token['Token']),
                                   'ident-{i}{i}{i}'.format(i=index_token + 1),
                                   parent='term-{i}{i}'.format(i=index_token))
            parse_tree.create_node('Identifier - {ID}'.format(ID=next_token['Token']),
                                   'ident-{i}{i}{i}'.format(i=index_token + 2),
                                   parent='term-{i}{i}'.format(i=index_token))

            parse_tree.create_node('=', '=', parent='program')

            right_tree = symbol_table[3:]
            parse_tree_right_maker(index_token, right_tree)

        else:
            validity = False
            print('====> Invalid Input. Expecting an Identifier followed by "=" <====')
    elif token['Type'] == 'Number':
        parse_tree_right_maker(index_token, symbol_table)

    if validity:
        print('\nParse Tree :')
        parse_tree.show()  # shows the parse tree.
        execute()  # Code is only executed if and only if the the code is Valid


def execute():
    global validity
    token = symbol_table[0]
    if token['Token'] == 'Num':
        executable = symbol_table[3:]
        exe_formula = ''
        for tks in executable:
            exe_formula = exe_formula + tks['Token']
        output = eval(exe_formula)
        print('Output of the Code : {out}'.format(out=output))

    elif token['Type'] == 'Number':
        executable = symbol_table
        exe_formula = ''
        for tks in executable:
            exe_formula = exe_formula + tks['Token']
        output = eval(exe_formula)
        print('Output of the Code : {out}'.format(out=output))

    else:
        validity = False
        print('====> Compile Error. Invalid Token at index 0 <====')


def lexicalAnalyzer(code):
    print('Source Code Length: {ln} (Whitespaces Removed)'.format(ln=len(code)))
    code = code.translate(str.maketrans('', '', string.whitespace))
    get_token(code)


# Entry Point

lexicalAnalyzer('Num x = 2 * 5')
# Below is the support for running the code from a file.
# SCL Stands for Simple Calculator Language. its essentially a text file
# Please comment the above line and uncomment the below 2 lines.

#source_file = open("sample-code.scl", "r")
#lexicalAnalyzer(source_file.readline())
