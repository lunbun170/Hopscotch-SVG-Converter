# Hopscotch-SVG-Converter
Converts SVGs to Hopscotch JSON

__NOTE: THIS DOES NOT WORK FOR HOPSCOTCH VERSION 32, ONLY VERSION 31__ (version 32 broke the triangle renderer because of the clone index update)

## Installing

Download the respository. You might also want to make sure the Python libraries `antlr4`, `xml`, `pyglet`, `tripy`, `tinycss`, `webcolors`, `colorsys`, `json`, `math`, and `random` work (probably download them from `pip`)

## How to Use

Unfortunately, if you want to actually use this, you have to change the code itself (because theres no UI). The input file defaults to `input.svg`, and the output file defaults to `output.json`. If you want to see what your SVG will look like without going onto Hopscotch, set the `hsify` variable to `False` (renders it on `pyglet` instead). Also, if you want to bundle a different triangle renderer, change the IDs of `ax`, `ay`, `bx`, `by`, `cx`, `cy`, `res`, `draw`, `r`, `g`, and `b` to the respective variable IDs (all of this is done in `main.py`).

I probably won't be updating this very often (although I might make a Javascript version of this sometime in the future).

## Compatibility

I don't know if this works on all operating systems. I think it works on all Macs (I don't know about Windows or Linux, I tested it on a Mac).

