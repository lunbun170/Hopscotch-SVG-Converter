from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\6")
        buf.write("&\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\3\5\3")
        buf.write("\17\n\3\3\3\6\3\22\n\3\r\3\16\3\23\3\3\3\3\6\3\30\n\3")
        buf.write("\r\3\16\3\31\5\3\34\n\3\3\4\3\4\3\5\6\5!\n\5\r\5\16\5")
        buf.write("\"\3\5\3\5\2\2\6\3\3\5\4\7\5\t\6\3\2\5\3\2\62;\4\2C\\")
        buf.write("c|\5\2\13\f\17\17\"\"\2*\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3")
        buf.write("\2\2\2\2\t\3\2\2\2\3\13\3\2\2\2\5\16\3\2\2\2\7\35\3\2")
        buf.write("\2\2\t \3\2\2\2\13\f\7.\2\2\f\4\3\2\2\2\r\17\7/\2\2\16")
        buf.write("\r\3\2\2\2\16\17\3\2\2\2\17\21\3\2\2\2\20\22\t\2\2\2\21")
        buf.write("\20\3\2\2\2\22\23\3\2\2\2\23\21\3\2\2\2\23\24\3\2\2\2")
        buf.write("\24\33\3\2\2\2\25\27\7\60\2\2\26\30\t\2\2\2\27\26\3\2")
        buf.write("\2\2\30\31\3\2\2\2\31\27\3\2\2\2\31\32\3\2\2\2\32\34\3")
        buf.write("\2\2\2\33\25\3\2\2\2\33\34\3\2\2\2\34\6\3\2\2\2\35\36")
        buf.write("\t\3\2\2\36\b\3\2\2\2\37!\t\4\2\2 \37\3\2\2\2!\"\3\2\2")
        buf.write("\2\" \3\2\2\2\"#\3\2\2\2#$\3\2\2\2$%\b\5\2\2%\n\3\2\2")
        buf.write("\2\b\2\16\23\31\33\"\3\b\2\2")
        return buf.getvalue()


class SvgLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    Comma = 1
    Number = 2
    Letter = 3
    WS = 4

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "','" ]

    symbolicNames = [ "<INVALID>",
            "Comma", "Number", "Letter", "WS" ]

    ruleNames = [ "Comma", "Number", "Letter", "WS" ]

    grammarFileName = "Svg.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


