from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SvgParser import SvgParser
else:
    from SvgParser import SvgParser

# This class defines a complete generic visitor for a parse tree produced by SvgParser.

class SvgVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SvgParser#point.
    def visitPoint(self, ctx:SvgParser.PointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SvgParser#poly_points.
    def visitPoly_points(self, ctx:SvgParser.Poly_pointsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SvgParser#command.
    def visitCommand(self, ctx:SvgParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SvgParser#path.
    def visitPath(self, ctx:SvgParser.PathContext):
        return self.visitChildren(ctx)



del SvgParser