#!/usr/bin/python

import re, sys

trans = {
        'base03':   {'base16': ['38;5;0',  '48;5;0'],  'sol16':['90','100'], 'sol256':["38;5;234","48;5;234"], 'sol16M':["38;2;0;43;54","48;2;0;43;54"]},
        'base02':   {'base16': ['38;5;18', '48;5;18'], 'sol16':['30','40'],  'sol256':["38;5;235","48;5;235"], 'sol16M':["38;2;7;54;66","48;2;7;54;66"]},
        'base01':   {'base16': ['38;5;19', '48;5;19'], 'sol16':['92','102'], 'sol256':["38;5;240","48;5;240"], 'sol16M':["38;2;88;110;117","48;2;88;110;117"]},
        'base00':   {'base16': ['38;5;8',  '48;5;8'],  'sol16':['93','103'], 'sol256':["38;5;241","48;5;241"], 'sol16M':["38;2;101;123;131","48;2;101;123;131"]},
        'base0':    {'base16': ['38;5;20', '48;5;20'], 'sol16':['94','104'], 'sol256':["38;5;244","48;5;244"], 'sol16M':["38;2;131;148;150","48;2;131;148;150"]},
        'base1':    {'base16': ['38;5;7',  '48;5;7'],  'sol16':['96','106'], 'sol256':["38;5;245","48;5;245"], 'sol16M':["38;2;147;161;161","48;2;147;161;161"]},
        'base2':    {'base16': ['38;5;21', '48;5;21'], 'sol16':['37','47'],  'sol256':["38;5;254","48;5;254"], 'sol16M':["38;2;238;232;213","48;2;238;232;213"]},
        'base3':    {'base16': ['38;5;15', '48;5;15'], 'sol16':['97','107'], 'sol256':["38;5;230","48;5;230"], 'sol16M':["38;2;253;246;227","48;2;253;246;227"]},
        'yellow':   {'base16': ['38;5;3',  '48;5;3'],  'sol16':['33','43'],  'sol256':["38;5;136","48;5;136"], 'sol16M':["38;2;181;137;0","48;2;181;137;0"]},
        'orange':   {'base16': ['38;5;16', '48;5;16'], 'sol16':['91','101'], 'sol256':["38;5;166","48;5;166"], 'sol16M':["38;2;203;75;22","48;2;203;75;22"]},
        'red':      {'base16': ['38;5;1',  '48;5;1'],  'sol16':['31','41'],  'sol256':["38;5;160","48;5;160"], 'sol16M':["38;2;220;50;47","48;2;220;50;47"]},
        'magenta':  {'base16': ['38;5;17', '48;5;17'], 'sol16':['35','45'],  'sol256':["38;5;125","48;5;125"], 'sol16M':["38;2;211;54;130","48;2;211;54;130"]},
        'violet':   {'base16': ['38;5;5',  '48;5;5'],  'sol16':['95','105'], 'sol256':["38;5;61","48;5;61"],   'sol16M':["38;2;108;113;196","48;2;108;113;196"]},
        'blue':     {'base16': ['38;5;4',  '48;5;4'],  'sol16':['34','44'],  'sol256':["38;5;33","48;5;33"],   'sol16M':["38;2;38;139;210","48;2;38;139;210"]},
        'cyan':     {'base16': ['38;5;6',  '48;5;6'],  'sol16':['36','46'],  'sol256':["38;5;37","48;5;37"],   'sol16M':["38;2;42;161;152","48;2;42;161;152"]},
        'green':    {'base16': ['38;5;2',  '48;5;2'],  'sol16':['32','42'],  'sol256':["38;5;64","48;5;64"],   'sol16M':["38;2;133;153;0","48;2;133;153;0"]}
}

basechange = {
        'base03': 'base3',
        'base02': 'base2',
        'base01': 'base1',
        'base00': 'base0',
        'base0':  'base00',
        'base1':  'base01',
        'base2':  'base02',
        'base3':  'base03',
        'yellow': 'yellow',
        'orange': 'orange',
        'red':    'red',
        'magenta':'magenta',
        'violet': 'violet',
        'blue':   'blue',
        'cyan':   'cyan',
        'green':  'green'
}

def to_desc(depth):
    desc = {
            'base16': 'Base16, using modified xterm 256 color palette',
            'sol16':  'ANSI 16 color, solarized modified palette',
            'sol256': 'xterm 256 color, solarized degraded using standard ansi palette',
            'sol16M': 'Solarized using TrueColor (24 bit, 16.7 million color)'
    }
    return desc[depth]

pat = re.compile('#{(flavor|(fg|bg):(' + '|'.join(trans.keys()) + ')(:bold)?)}')

def repl_func(depth, changebase, match):
    value = match.group(0)
    if (value == '#{flavor}'):
        return to_desc(depth)
    fgbg = match.group(2)
    key = match.group(3)
    if changebase:
        key = basechange[key]
    bold = match.group(4)
    seq = trans[key][depth][0 if fgbg == "fg" else 1]
    if bold:
        seq = '01;' + seq
    return seq

def snr(infile, outfile, depth, changebase):
    out = open(outfile, 'w')
    for i, line in enumerate(open(infile)):
        out.write(pat.sub(lambda m: repl_func(depth, changebase, m), line))

if __name__ == '__main__':
    depth = 'sol' + sys.argv[1] if sys.argv[1] != 'base16' else sys.argv[1]
    change = (True if sys.argv[2] == 'light' else False)
    snr('dircolors.in', 'dircolors.' + sys.argv[1] + sys.argv[2], depth, change)

