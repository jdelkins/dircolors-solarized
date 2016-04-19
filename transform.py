#!/usr/bin/python

import re, sys

trans = {
        'base03':   {'d16':['90','100'], 'd256':["38;5;234","48;5;234"], 'd16M':["38;2;0;43;54","48;2;0;43;54"]},
        'base02':   {'d16':['30','40'],  'd256':["38;5;235","48;5;235"], 'd16M':["38;2;7;54;66","48;2;7;54;66"]},
        'base01':   {'d16':['92','102'], 'd256':["38;5;240","48;5;240"], 'd16M':["38;2;88;110;117","48;2;88;110;117"]},
        'base00':   {'d16':['93','103'], 'd256':["38;5;241","48;5;241"], 'd16M':["38;2;101;123;131","48;2;101;123;131"]},
        'base0':    {'d16':['94','104'], 'd256':["38;5;244","48;5;244"], 'd16M':["38;2;131;148;150","48;2;131;148;150"]},
        'base1':    {'d16':['96','106'], 'd256':["38;5;245","48;5;245"], 'd16M':["38;2;147;161;161","48;2;147;161;161"]},
        'base2':    {'d16':['37','47'],  'd256':["38;5;254","48;5;254"], 'd16M':["38;2;238;232;213","48;2;238;232;213"]},
        'base3':    {'d16':['97','107'], 'd256':["38;5;230","48;5;230"], 'd16M':["38;2;253;246;227","48;2;253;246;227"]},
        'yellow':   {'d16':['33','43'],  'd256':["38;5;136","48;5;136"], 'd16M':["38;2;181;137;0","48;2;181;137;0"]},
        'orange':   {'d16':['91','101'], 'd256':["38;5;166","48;5;166"], 'd16M':["38;2;203;75;22","48;2;203;75;22"]},
        'red':      {'d16':['31','41'],  'd256':["38;5;160","48;5;160"], 'd16M':["38;2;220;50;47","48;2;220;50;47"]},
        'magenta':  {'d16':['35','45'],  'd256':["38;5;125","48;5;125"], 'd16M':["38;2;211;54;130","48;2;211;54;130"]},
        'violet':   {'d16':['95','105'], 'd256':["38;5;61","48;5;61"],   'd16M':["38;2;108;113;196","48;2;108;113;196"]},
        'blue':     {'d16':['34','44'],  'd256':["38;5;33","48;5;33"],   'd16M':["38;2;38;139;210","48;2;38;139;210"]},
        'cyan':     {'d16':['36','46'],  'd256':["38;5;37","48;5;37"],   'd16M':["38;2;42;161;152","48;2;42;161;152"]},
        'green':    {'d16':['32','42'],  'd256':["38;5;64","48;5;64"],   'd16M':["38;2;133;153;0","48;2;133;153;0"]}
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
            'd16': 'ANSI 16 color',
            'd256': 'xterm 256 color',
            'd16M': 'TrueColor (24 bit, 16.7 million color)'
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
    depth = 'd' + sys.argv[1]
    change = (True if sys.argv[2] == 'light' else False)
    snr('dircolors.in', 'dircolors.' + sys.argv[1] + sys.argv[2], depth, change)

