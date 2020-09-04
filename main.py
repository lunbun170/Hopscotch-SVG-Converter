import xml.etree.ElementTree as ET
from svg2shp import Svg2Shp, polish_tris
import pyglet
import tripy
import tinycss
import webcolors
import colorsys
import json
import math
from pyglet.gl import *
from random import *

tree = ET.parse('input.svg')
root = tree.getroot()

def getf(svg, param):
    if param not in svg.attrib.keys():
        return 0
    elif svg.attrib[param].endswith('px'):
        return float(svg.attrib[param][:-2])
    else:
        return float(svg.attrib[param])

width = getf(root, 'width')
height = getf(root, 'height')

translations = list()
triangles = list()

def translate():
    x, y = 0, 0
    for trans in translations:
        if trans is None:
            continue
        x += trans[0]
        y -= trans[1]
    return x, y

def tiny_func(attr):
    pars = list()
    for c in attr.content:
        if c.type in ['NUMBER', 'INTEGER']:
            pars.append(c.value)
    return pars

def color(attr):
    if attr.type == 'IDENT':
        clr = webcolors.name_to_rgb(attr.value)
        return clr[0] / 255, clr[1] / 255, clr[2] / 255
    elif attr.type == 'HASH':
        if len(attr.value) == 4:
            r = int(attr.value[1], 16)
            g = int(attr.value[2], 16)
            b = int(attr.value[3], 16)
            return r * 17, g * 17, b * 17
        else:
            r = int(attr.value[1:3], 16)
            g = int(attr.value[3:5], 16)
            b = int(attr.value[5:], 16)
            return r / 255, g / 255, b / 255
    elif type(attr) is tinycss.token_data.FunctionToken:
        pars = tiny_func(attr)
        if attr.function_name == 'rgb':
            return pars[0] / 255, pars[1] / 255, pars[2] / 255
        elif attr.function_name == 'hsl':
            return colorsys.hls_to_rgb(pars[0] / 360, pars[2] / 100, pars[1] / 100)

def lstroke(x1, y1, x2, y2, s):
    s /= 2
    ang = math.atan2(y2 - y1, x2 - x1)
    return [((x1 + math.sin(ang) * s, y1 - math.cos(ang) * s), (x1 - math.sin(ang) * s, y1 + math.cos(ang) * s),
            (x2 - math.sin(ang) * s, y2 + math.cos(ang) * s)), ((x1 + math.sin(ang) * s, y1 - math.cos(ang) * s),
            (x2 + math.sin(ang) * s, y2 - math.cos(ang) * s), (x2 - math.sin(ang) * s, y2 + math.cos(ang) * s))]

def tri_elem(elem, quality):
    global triangles, translations
    tag = elem.tag.rpartition('}')[2]
    added_trans = False
    fill = (0, 0, 0, 1)
    stroke = (0, 0, 0, 0)
    stroke_w = 0
    if 'transform' in elem.attrib:
        attr = tinycss.make_parser().parse_style_attr('test:' + elem.attrib['transform'] + ';')[0][0].value[0]
        if type(attr) is tinycss.token_data.FunctionToken:
            pars = tiny_func(attr)
            if attr.function_name == 'translate':
                translations.append((pars[0], pars[1]))
        added_trans = True
    if 'style' in elem.attrib:
        attrs = tinycss.make_parser().parse_style_attr(elem.attrib['style'])
        for attr in attrs[0]:
            if attr.name == 'fill':
                fill = (*color(attr.value[0]), 1)
            elif attr.name == 'stroke':
                stroke = (*color(attr.value[0]), 1)
            elif attr.name == 'stroke-width':
                stroke_w = attr.value[0].value
            elif attr.name == 'opacity':
                fill = (*fill[:3], attr.value[0].value)
    if 'fill' in elem.attrib:
        attr = tinycss.make_parser().parse_style_attr('test:' + elem.attrib['fill'] + ';')[0][0].value[0]
        fill = (*color(attr), 1)  # TODO: group fill stuff
    if 'stroke' in elem.attrib:
        attr = tinycss.make_parser().parse_style_attr('test:' + elem.attrib['stroke'] + ';')[0][0].value[0]
        stroke = (*color(attr), 1)  # TODO: group stroke stuff
    if 'stroke-width' in elem.attrib:
        stroke_w = tinycss.make_parser().parse_style_attr('test:' + elem.attrib['stroke-width'] + ';')[0][0].value[0]
        # TODO: group stroke-width stuff
    if not added_trans:
        translations.append(None)
    if stroke_w == 0:
        stroke = (0, 0, 0, 0)

    if tag == 'g':
        for e in elem:
            tri_elem(e, quality)
    else:
        svg = Svg2Shp(elem, quality)
        if hasattr(svg, 'closed'):
            if svg.closed:
                triangles += polish_tris(tripy.earclip(svg.shape), height, fill, translate())
        last = svg.shape[-1]
        for a in svg.shape:
            triangles += polish_tris(lstroke(*last, *a, stroke_w), height, stroke, translate())
            last = a

    translations.pop()

for elem in root:
    tri_elem(elem, 26)

def to_hs(ax, ay, bx, by, cx, cy, res, draw, r, g, b):
    def sv(i, v):
        blocks.append({'block_class': 'method', 'type': 45, 'description': 'Set', 'parameters': [{'defaultValue': '', 'value': '', 'key': '', 'datum': {'type': 8004, 'variable': i, 'description': 'Variable'}}, {'defaultValue': '', 'value': str(v), 'key': 'to', 'type': 42}]})

    def wait(v):
        blocks.append({'block_class': 'method', 'description': 'Wait', 'type': 61, 'parameters': [{'defaultValue': '', 'value': '0', 'key': 'seconds', 'type': 57}]})

    blocks = list()
    sv(res, 0.25)
    ar = 10000000
    ag = 10000000
    ab = 10000000
    for tri in triangles:
        sv(ax, tri[0][0])
        sv(ay, tri[0][1])
        sv(bx, tri[1][0])
        sv(by, tri[1][1])
        sv(cx, tri[2][0])
        sv(cy, tri[2][1])
        br = tri[3][0] * 255
        bg = tri[3][1] * 255
        bb = tri[3][2] * 255
        if ar != br:
            sv(r, br)
            ar = br
        if ag != bg:
            sv(g, bg)
            ag = bg
        if ab != bb:
            sv(b, bb)
            ab = bb
        sv(draw, 1)
        wait(0)
    return blocks

hsify = True

if hsify:
    ax = 'BAD4F2A7-9B78-4AFC-AC76-95F6DE6DAF24-9510-00000B36F15A0FC4'
    ay = '14FFCA4E-38D0-47D4-83F2-9F333A870E95-9510-00000B36F92413A1'
    bx = '472080C8-8D46-4706-9A0C-8B841743BD3C-9510-00000B36FDAAC964'
    by = 'E27E2292-8D9C-43CA-9AB8-C9E11A64B8C1-9510-00000B37040A5F24'
    cx = 'A015871B-BB46-41FD-B327-776C58FAD5E9-9510-00000B370815E85E'
    cy = '3329A117-5D01-4035-A9E6-D245C024B603-9510-00000B370C8B86ED'
    res = '10268A84-0C8B-4714-B793-A6F8EC0AD3F3-9510-00000B60DDB30762'
    draw = '30F8C0CB-A820-461B-B11D-214C03B67244-9510-00000B60E6C04A50'
    r = '5CA691D7-A2F8-4564-9F52-34BB36451351-9510-00000B614873EF95'
    g = '6FC0A93F-1DC9-464F-9436-5B69C80567AB-9510-00000B6152638989'
    b = 'E5DC8902-9EB2-4EC3-B7CF-72E4A1FBAB0F-9510-00000B615C323A97'
    output_file = 'output.json'
    blocks = to_hs(ax, ay, bx, by, cx, cy, res, draw, r, g, b)
    bj = json.dumps(blocks, separators=(',', ':'))
    with open('template.txt', 'r') as f:
        cont = f.read()
    d = cont.replace('"<Template Template>"', bj)
    with open(output_file, 'w+') as fp:
        fp.write(json.dumps(json.loads(d), separators=(',', ':')))  # to compress the project
else:
    window = pyglet.window.Window(width=width, height=height, caption='Svg Triangulation')

    glClearColor(1, 1, 1, 1)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    def rand():
        glColor3f(random(), random(), random(), 1)

    @window.event
    def on_draw():
        window.clear()
        glClear(GL_COLOR_BUFFER_BIT)
        for tri in triangles:
            glColor4f(*tri[3])
            vlist = pyglet.graphics.vertex_list(3, ('v2f', [*tri[0], *tri[1], *tri[2]]))
            vlist.draw(GL_TRIANGLES)

    pyglet.app.run()

