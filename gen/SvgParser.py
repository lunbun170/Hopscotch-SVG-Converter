# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\6")
        buf.write("*\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\5\2\r\n\2\3")
        buf.write("\2\3\2\3\3\7\3\22\n\3\f\3\16\3\25\13\3\3\4\3\4\3\4\5\4")
        buf.write("\32\n\4\3\4\7\4\35\n\4\f\4\16\4 \13\4\5\4\"\n\4\3\5\7")
        buf.write("\5%\n\5\f\5\16\5(\13\5\3\5\2\2\6\2\4\6\b\2\2\2+\2\n\3")
        buf.write("\2\2\2\4\23\3\2\2\2\6\26\3\2\2\2\b&\3\2\2\2\n\f\7\4\2")
        buf.write("\2\13\r\7\3\2\2\f\13\3\2\2\2\f\r\3\2\2\2\r\16\3\2\2\2")
        buf.write("\16\17\7\4\2\2\17\3\3\2\2\2\20\22\5\2\2\2\21\20\3\2\2")
        buf.write("\2\22\25\3\2\2\2\23\21\3\2\2\2\23\24\3\2\2\2\24\5\3\2")
        buf.write("\2\2\25\23\3\2\2\2\26!\7\5\2\2\27\36\7\4\2\2\30\32\7\3")
        buf.write("\2\2\31\30\3\2\2\2\31\32\3\2\2\2\32\33\3\2\2\2\33\35\7")
        buf.write("\4\2\2\34\31\3\2\2\2\35 \3\2\2\2\36\34\3\2\2\2\36\37\3")
        buf.write("\2\2\2\37\"\3\2\2\2 \36\3\2\2\2!\27\3\2\2\2!\"\3\2\2\2")
        buf.write("\"\7\3\2\2\2#%\5\6\4\2$#\3\2\2\2%(\3\2\2\2&$\3\2\2\2&")
        buf.write("\'\3\2\2\2\'\t\3\2\2\2(&\3\2\2\2\b\f\23\31\36!&")
        return buf.getvalue()


class SvgParser ( Parser ):

    grammarFileName = "Svg.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "','" ]

    symbolicNames = [ "<INVALID>", "Comma", "Number", "Letter", "WS" ]

    RULE_point = 0
    RULE_poly_points = 1
    RULE_command = 2
    RULE_path = 3

    ruleNames =  [ "point", "poly_points", "command", "path" ]

    EOF = Token.EOF
    Comma=1
    Number=2
    Letter=3
    WS=4

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class PointContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Number(self, i:int=None):
            if i is None:
                return self.getTokens(SvgParser.Number)
            else:
                return self.getToken(SvgParser.Number, i)

        def Comma(self):
            return self.getToken(SvgParser.Comma, 0)

        def getRuleIndex(self):
            return SvgParser.RULE_point

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPoint" ):
                return visitor.visitPoint(self)
            else:
                return visitor.visitChildren(self)




    def point(self):

        localctx = SvgParser.PointContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_point)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.match(SvgParser.Number)
            self.state = 10
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SvgParser.Comma:
                self.state = 9
                self.match(SvgParser.Comma)


            self.state = 12
            self.match(SvgParser.Number)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Poly_pointsContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def point(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SvgParser.PointContext)
            else:
                return self.getTypedRuleContext(SvgParser.PointContext,i)


        def getRuleIndex(self):
            return SvgParser.RULE_poly_points

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPoly_points" ):
                return visitor.visitPoly_points(self)
            else:
                return visitor.visitChildren(self)




    def poly_points(self):

        localctx = SvgParser.Poly_pointsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_poly_points)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SvgParser.Number:
                self.state = 14
                self.point()
                self.state = 19
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommandContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Letter(self):
            return self.getToken(SvgParser.Letter, 0)

        def Number(self, i:int=None):
            if i is None:
                return self.getTokens(SvgParser.Number)
            else:
                return self.getToken(SvgParser.Number, i)

        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(SvgParser.Comma)
            else:
                return self.getToken(SvgParser.Comma, i)

        def getRuleIndex(self):
            return SvgParser.RULE_command

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCommand" ):
                return visitor.visitCommand(self)
            else:
                return visitor.visitChildren(self)




    def command(self):

        localctx = SvgParser.CommandContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_command)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 20
            self.match(SvgParser.Letter)
            self.state = 31
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==SvgParser.Number:
                self.state = 21
                self.match(SvgParser.Number)
                self.state = 28
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==SvgParser.Comma or _la==SvgParser.Number:
                    self.state = 23
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==SvgParser.Comma:
                        self.state = 22
                        self.match(SvgParser.Comma)


                    self.state = 25
                    self.match(SvgParser.Number)
                    self.state = 30
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PathContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def command(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(SvgParser.CommandContext)
            else:
                return self.getTypedRuleContext(SvgParser.CommandContext,i)


        def getRuleIndex(self):
            return SvgParser.RULE_path

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPath" ):
                return visitor.visitPath(self)
            else:
                return visitor.visitChildren(self)




    def path(self):

        localctx = SvgParser.PathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_path)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==SvgParser.Letter:
                self.state = 33
                self.command()
                self.state = 38
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





