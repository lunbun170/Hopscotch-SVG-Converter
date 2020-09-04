import xml.etree.ElementTree as ET
import math
from gen.SvgLexer import *
from gen.SvgParser import *
from gen.SvgVisitor import *
from antlr4 import *

class Svg2Shp:
    def __init__(self, svg: ET.Element, quality: int):
        def getf(param):
            nonlocal svg
            if param not in svg.attrib.keys():
                return 0
            elif svg.attrib[param].endswith('px'):
                return float(svg.attrib[param][:-2])
            else:
                return float(svg.attrib[param])

        def gets(param):
            nonlocal svg
            return '' if param not in svg.attrib.keys() else svg.attrib[param]

        def get_iter(peri):
            nonlocal quality
            return math.ceil(quality * math.sqrt(peri) / 15)

        def lerp(a, b, c):
            return a + ((b - a) * c)

        tag = svg.tag.rpartition('}')[2]
        if tag == 'rect':
            x, y, w, h = getf('x'), getf('y'), getf('width'), getf('height')
            self.shape = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
            self.closed = True
        elif tag == 'circle':
            x, y, r = getf('cx'), getf('cy'), getf('r')
            self.shape = list()
            peri = math.tau * r
            it = get_iter(peri)
            for i in range(it):
                self.shape.append((x + math.sin(i * math.tau / it) * r, y + math.cos(i * math.tau / it) * r))
            self.closed = True
        elif tag == 'ellipse':
            x, y, rx, ry = getf('cx'), getf('cy'), getf('rx'), getf('ry')
            self.shape = list()
            peri = math.tau * math.sqrt((rx * rx + ry * ry) / 2)
            it = get_iter(peri)
            for i in range(it):
                self.shape.append((x + math.sin(i * math.tau / it) * rx, y + math.cos(i * math.tau / it) * ry))
            self.closed = True
        elif tag == 'line':
            x1, y1, x2, y2 = getf('x1'), getf('y1'), getf('x2'), getf('y2')
            self.shape = [(x1, y1), (x2, y2)]
            self.closed = False
        elif tag == 'polygon':
            points = gets('points')
            text = InputStream(points)
            lexer = SvgLexer(text)
            stream = CommonTokenStream(lexer)
            parser = SvgParser(stream)
            tree = parser.poly_points()
            self.shape = list()
            for point in tree.point():
                self.shape.append((float(point.Number(0).getText()), float(point.Number(1).getText())))
            self.closed = True
        elif tag == 'polyline':
            points = gets('points')
            text = InputStream(points)
            lexer = SvgLexer(text)
            stream = CommonTokenStream(lexer)
            parser = SvgParser(stream)
            tree = parser.poly_points()
            self.shape = list()
            for point in tree.point():
                self.shape.append((float(point.Number(0).getText()), float(point.Number(1).getText())))
            self.closed = False
        elif tag == 'path':
            def add(x, y):
                nonlocal self
                if (x, y) not in self.shape:
                    self.shape.append((x, y))

            self.shape = list()
            self.closed = False
            x, y = 0, 0
            text = InputStream(gets('d'))
            lexer = SvgLexer(text)
            stream = CommonTokenStream(lexer)
            parser = SvgParser(stream)
            tree = parser.path()
            for command in tree.command():
                args = list()
                cmd = command.Letter().getText()
                rel = cmd.islower()
                r = True
                for arg in command.Number():
                    a = float(arg.getText())
                    if rel:
                        if r:
                            a += x
                        else:
                            a += y
                        r = not r
                    args.append(a)

                cmd = cmd.lower()
                if cmd == 'm':  # TODO: holes
                    x, y = args[0], args[1]
                elif cmd == 'l':
                    add(x, y)
                    x, y = args[0], args[1]
                    add(x, y)
                elif cmd == 'h':
                    add(x, y)
                    x = args[0]
                    add(x, y)
                elif cmd == 'v':
                    add(x, y)
                    if rel:
                        y += args[0] - x
                    else:
                        y = args[0]
                    add(x, y)
                elif cmd in 'cs':  # cubic bezier
                    lena = dist((x, y), (args[0], args[1]))
                    lenb = dist((args[0], args[1]), (args[2], args[3]))
                    lenc = dist((args[2], args[3]), (args[4], args[5]))
                    lend = dist((x, y), (args[4], args[5]))
                    peri = (lena + lenb + lenc + lend) / 2
                    it = get_iter(peri)
                    for i in range(it + 1):
                        dx0 = lerp(x, args[0], i / it)
                        dy0 = lerp(y, args[1], i / it)
                        dx1 = lerp(args[0], args[2], i / it)
                        dy1 = lerp(args[1], args[3], i / it)
                        dx2 = lerp(args[2], args[4], i / it)
                        dy2 = lerp(args[3], args[5], i / it)
                        dx3 = lerp(dx0, dx1, i / it)
                        dy3 = lerp(dy0, dy1, i / it)
                        dx4 = lerp(dx1, dx2, i / it)
                        dy4 = lerp(dy1, dy2, i / it)
                        dx5 = lerp(dx3, dx4, i / it)
                        dy5 = lerp(dy3, dy4, i / it)
                        add(dx5, dy5)
                    x, y = args[4], args[5]
                elif cmd in 'qt':  # quadratic bezier
                    lena = dist((x, y), (args[0], args[1]))
                    lenb = dist((args[0], args[1]), (args[2], args[3]))
                    lenc = dist((x, y), (args[2], args[3]))
                    peri = (lena + lenb + lenc) / 2
                    it = get_iter(peri)
                    for i in range(it + 1):
                        dx0 = lerp(x, args[0], i / it)
                        dy0 = lerp(y, args[1], i / it)
                        dx1 = lerp(args[0], args[2], i / it)
                        dy1 = lerp(args[1], args[3], i / it)
                        dx2 = lerp(dx0, dx1, i / it)
                        dy2 = lerp(dy0, dy1, i / it)
                        add(dx2, dy2)
                    x, y = args[2], args[3]
                elif cmd == 'a':  # elliptical arc
                    pass
                elif cmd == 'z':
                    self.closed = True

def dist(a, b):
    return math.sqrt(((a[0] - b[0]) * (a[0] - b[0])) + ((a[1] - b[1]) * (a[1] - b[1])))

def polish_tris(tris, y, color, trans):
    if color[3] == 0:
        return list()
    tmp = list()
    x, z = trans
    for tri in tris:
        tmp.append(((tri[0][0] + x, y - tri[0][1] + z), (tri[1][0] + x, y - tri[1][1] + z),
                    (tri[2][0] + x, y - tri[2][1] + z), color))
    return tmp

