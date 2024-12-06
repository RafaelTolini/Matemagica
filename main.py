from sly import Lexer, Parser

class MatemagicaLexer(Lexer):
    reserved = ('SOME', 'COM', 'MULTIPLIQUE', 'POR', 'FACA', 'SER', 'REPITA', 'VEZES', 'FIM', 'SE', 'ENTAO', 'SENAO', 'MOSTRE', 'MAIOR', 'MENOR', 'QUE')
    tokens = reserved + ('NUM', 'VAR', 'PONTO', 'DOIS_PONTOS')
    ignore = ' \t'

    NUM = r'[0-9]+'
    PONTO = r'\.'
    DOIS_PONTOS = r'\:'
    
    @_(r'[a-zA-Z][a-zA-Z]*')
    def VAR(self, t):
        if t.value in self.reserved:
            t.type = t.value
        return t

    ignore_newline = r'\n+'
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class MatemagicaParser(Parser):
    tokens = MatemagicaLexer.tokens

    @_('impressao', 'operacao', 'atribuicao', 'repeticao', 'condicional', 'fim')
    def start(self, p):
        return p[0]

    @_('MOSTRE VAR PONTO', 'MOSTRE operacao', 'MOSTRE NUM PONTO')
    def impressao(self, p):
        return f'print({p[1][p[1].find("=")+1:]})'
    
    @_('SOME VAR COM VAR PONTO', 'SOME NUM COM NUM PONTO', 'SOME NUM COM VAR PONTO', 'SOME VAR COM NUM PONTO')
    def operacao(self, p):
        return self.operacao_aux(p, '+')
    
    @_('MULTIPLIQUE VAR POR VAR PONTO', 'MULTIPLIQUE NUM POR NUM PONTO', 'MULTIPLIQUE NUM POR VAR PONTO', 'MULTIPLIQUE VAR POR NUM PONTO')
    def operacao(self, p):
        return self.operacao_aux(p, '*')
    
    @_('FACA VAR SER NUM PONTO', 'FACA VAR SER VAR PONTO')
    def atribuicao(self, p):
        return f'{p[1]} = {p[3]}'
    
    @_('REPITA NUM VEZES DOIS_PONTOS', 'REPITA VAR VEZES DOIS_PONTOS')
    def repeticao(self, p):
        return f'for TEMP2 = 1, {p[1]} do'
    
    @_('SE VAR ENTAO', 'SE NUM ENTAO')
    def condicional(self, p):
        return f'if not (({p[1]}) == 0) then'
    
    @_('SE VAR MAIOR QUE NUM ENTAO', 'SE VAR MAIOR QUE VAR ENTAO', 'SE NUM MAIOR QUE VAR ENTAO', 'SE NUM MAIOR QUE NUM ENTAO')
    def condicional(self, p):
        return f'if ({p[1]} > {p[4]}) then'
    
    @_('SE VAR MENOR QUE NUM ENTAO', 'SE VAR MENOR QUE VAR ENTAO', 'SE NUM MENOR QUE VAR ENTAO', 'SE NUM MENOR QUE NUM ENTAO')
    def condicional(self, p):
        return f'if ({p[1]} < {p[4]}) then'
        
    @_('SENAO')
    def condicional(self, p):
        return f'else'
    
    @_('FIM')
    def fim(self, p):
        return f'end'
    
    def operacao_aux(self, p, op):
        return f'TEMP1 = {p[1]} {op} {p[3]}' if (p[1].isnumeric() and p[3].isnumeric()) else (f'{p[3]} = {p[1]} {op} {p[3]}' if p[1].isnumeric() else f'{p[1]} = {p[1]} {op} {p[3]}')


if __name__ == '__main__':
    lexer = MatemagicaLexer()
    parser = MatemagicaParser()
    
    erro = False
    with open('codigo.mag') as f:
        with open('programa.lua', 'w') as fw:
            for idx, linha in enumerate(f):
                if linha == "\n" or linha == "":
                    continue
                try:
                    linha_convertida = parser.parse(lexer.tokenize(linha))
                    fw.write(linha_convertida + '\n')
                except:
                    print(f'\nErro de código na linha {idx+1} ::: {linha!r}')
                    erro = True
                    break

    if not erro:
        print("\n==============================================================================")
        print("O programa em Matemagica foi compilado com sucesso para Lua em programa.lua!")
        print("==============================================================================\n")