class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def consume(self, name, value=None):
        if self.tokens[self.index].name == name:
            if value:
                if self.tokens[self.index].value == value:
                    self.index += 1
                    return True
                else:
                    return False
            else:
                self.index += 1
                return True
        return False

    def is_const_declaration(self):
        if not self.consume('IDENTIFIER'):
            raise SyntaxError
        else:
            if not self.consume('EQUAL'):
                raise SyntaxError
            else:
                self.is_static_expression()
                if not self.consume('SEMICOLON'):
                    raise SyntaxError

    def is_constant(self):
        if not (self.consume('INTEGER') or
                self.consume('BASE10_NUM') or
                self.consume('CHAR') or
                self.consume('REAL')):
            raise SyntaxError

    def is_static_factor(self):
        if self.consume('IDENTIFIER'):
            return
        try:
            is_constant()
            return
        except SyntaxError:
            if self.consume('LP'):
                is_static_expression()
                if self.consume('RP'):
                    return
        raise SyntaxError

    def is_op_mul(self):
        if not (self.consume('OP_MUL') or
                self.consume('KEYWORD', 'div') or
                self.consume('KEYWORD', 'mod')):
            raise SyntaxError

    def is_static_term_alt(self):
        try:
            is_op_mul()
            is_static_factor()
            is_static_term_alt()
        except SyntaxError:
            return

    def is_static_term(self):
        is_static_factor()
        is_static_term_alt()

    def is_op_add(self):
        if not self.consume('OP_AD'):
            raise SyntaxError

    def is_static_expression_alt(self):
        try:
            is_op_add()
        except SyntaxError:
            return
        is_static_term()
        is_static_expression_alt()

    def is_static_expression(self):
        is_static_term()
        is_static_expression_alt()


    def is_id_list_alt(self):
        if not self.consume('COMMA'):
            return
        if self.consume('IDENTIFIER'):
            is_id_list_alt()

    def is_id_list(self):
        if self.consume('IDENTIFIER'):
            is_id_list_alt()
        return

    def is_simple_type(self):
        if not (self.consume('KEYWORD', 'integer') or
                self.consume('KEYWORD', 'real') or
                self.consume('KEYWORD', 'char')):
            raise SyntaxError

    def is_array(self):
        if self.consume('KEYWORD', 'array'):
            if self.consume('LSB'):
                is_static_expression()
                if self.consume('RANGE'):
                    is_static_expression()
                    if self.consume('RSB'):
                        if self.consume('KEYWORD', 'of'):
                            is_simple_type()
                            return
        raise SyntaxError

    def is_simple_declaration(self):
        is_id_list()
        if not self.consume('COLON'):
            raise SyntaxError
        is_simple_type()

    def is_field_list_alt(self):
        if self.consume('SEMICOLON'):
            is_simple_declaration()
            is_field_list_alt()
        else:
            return

    def is_field_list(self):
        is_simple_declaration()
        is_field_list_alt()

    def is_struct(self):
        if self.consume('KEYWORD', 'record'):
            is_field_list()
            if self.consume('KEYWORD', 'end'):
                return
        raise SyntaxError

    def is_type(self):
        try:
            is_simple_type()
        except SyntaxError:
            try:
                is_array()
            except SyntaxError:
                is_struct()

    def is_var_declaration(self):
        is_id_list()
        if self.consume('COLON'):
            is_type()
            if not self.consume('SEMICOLON'):
                raise SyntaxError
        else:
            raise SyntaxError

    def is_const_declaration_list_alt(self):
        try:
            is_const_declaration()
            is_const_declaration_list_alt()
        except SyntaxError:
            return

    def is_const_declaration_list(self):
        is_const_declaration()
        is_const_declaration_list_alt()

    def is_const_section(self):
        if self.consume('KEYWORD', 'const'):
            is_const_declaration_list()

    def is_instr_list_alt(self):
        if not self.consume('SEMICOLON'):
            return
        is_instr()
        is_instr_list_alt()

    def is_instr_list(self):
        is_instr()
        is_instr_list_alt()

    def is_var_declaration_list_alt(self):
        try:
            is_var_declaration()
            is_var_declaration_list_alt()
        except SyntaxError:
            return

    def is_var_declaration_list(self):
        is_var_declaration()
        is_var_declaration_list_alt()

    def is_function_header(self):
        if self.consume('IDENTIFIER'):
            is_formal_param()
        else:
            raise SyntaxError

    def is_param_declaration(self):
        if not self.consume('KEYWORD', 'var'):
            pass
        is_simple_declaration()

    def is_formal_param_list_alt(self):
        if self.consume('SEMICOLON'):
            is_param_declaration()
            is_formal_param_list_alt()

    def is_formal_param_list(self):
        is_param_declaration()
        is_formal_param_list_alt()

    def is_formal_param(self):
        if self.consume('LP'):
            is_formal_param_list()
            if self.consume('RP'):
                return
            else:
                raise SyntaxError

    def is_composed_instruction(self):
        if self.consume('KEYWORD', 'begin'):
            is_instr_list()
            if self.consume('SEMICOLON'):
                pass
            if self.consume('KEYWORD', 'end'):
                return
        raise SyntaxError

    def is_block(self):
        is_const_section()
        is_var_section()
        is_subprogr_declaration_section()
        is_composed_instruction()

    def is_procedure_declaration(self):
        if self.consume('KEYWORD', 'procedure'):
            is_function_header()
            if self.consume('SEMICOLON'):
                is_block()
                if self.consume('SEMICOLON'):
                    return
        raise SyntaxError

    def is_var_section(self):
        if self.consume('KEYWORD', 'var'):
            is_var_declaration_list()

    def is_function_declaration(self):
        if self.consume('KEYWORD', 'function'):
            is_function_header()
            if self.consume('COLON'):
                is_simple_type()
                if self.consume('SEMICOLON'):
                    is_block()
                    if self.consume('SEMICOLON'):
                        return
        raise SyntaxError

    def is_subprog_declaration(self):
        try:
            is_function_declaration()
        except SyntaxError:
            is_procedure_declaration()

    def is_subprogr_declaration_list_alt(self):
        try:
            is_subprog_declaration()
            is_subprogr_declaration_list_alt()
        except SyntaxError:
            pass

    def is_subprogr_declaration_list(self):
        is_subprog_declaration()
        is_subprogr_declaration_list_alt()

    def is_subprogr_declaration_section(self):
        try:
            is_subprogr_declaration_list()
        except SyntaxError:
            pass

    def is_op_log(self):
        if not (self.consume('KEYWORD', 'and') or
                self.consume('KEYWORD', 'or')):
            raise SyntaxError

    def is_rel_expr(self):
        if self.consume('LP'):
            is_condition()
            if not self.consume('RP'):
                raise SyntaxError
            else:
                return
        else:
            is_expr()
            is_op_rel()
            is_expr()

    def is_op_rel(self):
        if not (self.consume('LT') or
                self.consume('GT') or
                self.consume('GE') or
                self.consume('LE') or
                self.consume('EQUAL') or
                self.consume('NOT_EQUAL')):
            raise SyntaxError

    def is_log_expr_alt(self):
        try:
            is_op_rel()
            is_rel_expr()
            is_log_expr_alt()
        except SyntaxError:
            return

    def is_log_expr(self):
        # if DEBUG:
        #     is_rel_expr()
        is_log_expr_alt()

    def is_condition(self):
        self.consume('KEYWORD', 'not')
        is_log_expr()

    def is_else(self):
        if self.consume('KEYWORD', 'else'):
            is_instr()
        else:
            return

    def is_if(self):
        if not self.consume('KEYWORD', 'if'):
            raise SyntaxError
        is_condition()
        if not self.consume('KEYWORD', 'then'):
            raise SyntaxError
        is_instr()
        is_else()

    def is_while(self):
        if not self.consume('KEYWORD', 'while'):
            raise SyntaxError
        is_condition()
        if not self.consume('KEYWORD', 'do'):
            raise SyntaxError
        is_instr()

    def is_repeat(self):
        if not self.consume('KEYWORD', 'repeat'):
            raise SyntaxError
        is_instr()
        if not self.consume('KEYWORD', 'until'):
            raise SyntaxError
        is_condition()

    def is_var(self):
        if self.consume('IDENTIFIER'):
            if self.consume('LSB'):
                is_expr()
                if not self.consume('RSB'):
                    raise SyntaxError
            elif self.consume('DOT'):
                if not self.consume('IDENTIFIER'):
                    raise SyntaxError
            else:
                raise SyntaxError
        else:
            raise SyntaxError

    def is_factor(self):
        try:
            is_constant()
        except SyntaxError:
            if self.consume('LP'):
                is_expr()
                if not self.consume('RP'):
                    raise SyntaxError
            elif self.consume('IDENTIFIER'):
                if self.consume('LP'):
                    is_expr_list()
                    if not self.consume('RP'):
                        raise SyntaxError
                elif self.consume('LSB'):
                    is_expr()
                    if not self.consume('RSB'):
                        raise SyntaxError
                elif self.consume('DOT'):
                    if not self.consume('IDENTIFIER'):
                        raise SyntaxError
                else:
                    raise SyntaxError
            else:
                raise SyntaxError

    def is_term_alt(self):
        try:
            is_op_mul()
            is_factor()
            is_term_alt()
        except SyntaxError:
            return

    def is_term(self):
        is_factor()
        is_term_alt()

    def is_expr_alt(self):
        try:
            is_op_add()
        except SyntaxError:
            return
        is_term()
        is_expr_alt()

    def is_expr(self):
        is_term()
        is_expr_alt()

    def is_direction(self):
        if not (self.consume('KEYWORD', 'to') or
                self.consume('KEYWORD', 'downto')):
            raise SyntaxError

    def is_step(self):
        if self.consume('KEYWORD', 'step'):
            is_expr()

    def is_for(self):
        if not self.consume('KEYWORD', 'for'):
            raise SyntaxError
        is_var()
        if not self.consume('ATTRIB'):
            raise SyntaxError
        is_expr()
        is_direction()
        is_expr()
        is_step()
        if not self.consume('KEYWORD', 'do'):
            raise SyntaxError
        is_instr()

    def is_val_list_alt(self):
        if self.consume('COMMA'):
            is_constant()
            is_val_list_alt()

    def is_val_list(self):
        is_constant()
        is_val_list_alt()

    def is_branch(self):
        is_val_list()
        if not self.consume('COLON'):
            raise SyntaxError
        is_instr()
        if not self.consume('SEMICOLON'):
            raise SyntaxError

    def is_branch_list_alt(self):
        try:
            is_branch()
            is_branch_list_alt()
        except SyntaxError:
            return

    def is_branch_list(self):
        is_branch()
        is_branch_list_alt()

    def is_alt_list(self):
        is_branch_list()
        if self.consume('KEYWORD', 'otherwise'):
            if not self.consume('COLON'):
                raise SyntaxError
            is_instr()

    def is_case(self):
        if not self.consume('KEYWORD', 'case'):
            raise SyntaxError
        is_expr()
        if not self.consume('KEYWORD', 'of'):
            raise SyntaxError
        is_alt_list()
        if not self.consume('KEYWORD', 'end'):
            raise SyntaxError

    def is_atrib(self):
        try:
            is_var()
        except SyntaxError:
            raise SyntaxError
        if not self.consume('ATTRIB'):
            self.index -= 1
        is_expr()

    def is_expr_list_alt(self):
        if self.consume('COMMA'):
            is_expr()
            is_expr_list_alt()

    def is_expr_list(self):
        is_expr()
        is_expr_list_alt()

    def is_proc_call(self):
        if self.consume('IDENTIFIER'):
            raise SyntaxError
        if not self.consume('LP'):
            return
        is_expr_list()
        if not self.consume('RP'):
            raise SyntaxError

    def is_var_list_alt(self):
        if self.consume('COMMA'):
            is_var()
            is_var_list_alt()

    def is_var_list(self):
        is_var()
        is_var_list_alt()

    def is_read(self):
        if not self.consume('KEYWORD', 'read'):
            raise SyntaxError
        if not self.consume('LP'):
            raise SyntaxError
        is_var_list()
        if not self.consume('RP'):
            raise SyntaxError

    def is_element(self):
        if self.consume('CHAR') or self.consume('STRING'):
            return
        else:
            is_expr()

    def is_elem_list_alt(self):
        if self.consume('COMMA'):
            is_element()
            is_elem_list_alt()

    def is_elem_list(self):
        is_element()
        is_elem_list_alt()

    def is_print(self):
        if not self.consume('KEYWORD', 'print'):
            raise SyntaxError
        if not self.consume('LP'):
            raise SyntaxError
        is_elem_list()
        if not self.consume('RP'):
            raise SyntaxError

    def is_instr(self):
        try:
            is_if()
        except SyntaxError:
            try:
                is_while()
            except SyntaxError:
                try:
                    is_repeat()
                except SyntaxError:
                    try:
                        is_for()
                    except SyntaxError:
                        try:
                            is_case()
                        except SyntaxError:
                            try:
                                is_atrib()
                            except SyntaxError:
                                try:
                                    is_proc_call()
                                except SyntaxError:
                                    try:
                                        is_read()
                                    except SyntaxError:
                                        try:
                                            is_print()
                                        except SyntaxError:
                                            try:
                                                is_composed_instruction()
                                            except SyntaxError as e:
                                                return

    def is_source(self):
        if self.consume('KEYWORD', 'program'):
            if self.consume('IDENTIFIER'):
                if not self.consume('SEMICOLON'):
                    raise SyntaxError
                is_block()
            else:
                raise SyntaxError
        else:
            raise SyntaxError

    def parse(self):
        self.is_source()
