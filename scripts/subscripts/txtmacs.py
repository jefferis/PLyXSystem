# Define and expand text macros in a LyX document.
# Part of the pLyX.py system; not an independent script
#
# txtmacs.py 
#
# Andrew Parsloe (aparsloe@clear.net.nz)
#
######################################################

import re, argparse

bs1 = '\n\\backslash\n1\n'
macdict = {'toggle': [[], ''], 'if0': [[''], bs1], 'if1': [[''], bs1],
           'peel': [[''], bs1]}

def main(infl, outfl, options, guff):
    '''Expand text macros.'''
      
    flex_arg = r'\begin_inset Flex .[argument]'
    begin_layout = r'\begin_layout'
    end_layout = r'\end_layout'
    begin_inset = r'\begin_inset'
    end_inset = r'\end_inset'
    begin_note = r'\begin_inset Note Note'
    bkslash = '\\'
    backslash = '\\backslash\n'
    status_open = 'status open\n'
    status_coll = 'status collapsed\n'

    re_macro = re.compile(r'(\w+)\n*(\w*)\s*(\d*)\s*$')
    re_lyxcmds = re.compile(r'(\\\w+) \w+')
    underscores = set([begin_layout, begin_inset, end_layout, end_inset])
    charstyles = ['\\family', '\\series', '\\shape', '\\size', '\\emph', \
                  '\\noun', '\\underbar', '\\strikeout', '\\uuline', \
                  '\\uwave', '\\no_emph', '\\no_noun', '\\no_strikeout', \
                  '\\no_bar', '\\no_uuline', '\\no_uwave']

    def output(depth, L):
        # write to file only at top level
        if depth == 0:
            outfl.write(L)
            return ''
        else:
            return L

    def defaults(s):
        '''Return used charstyles to default states.'''
        temp = r''
        for y in (set(re_lyxcmds.findall(s)) - underscores):
            if y == r'\color':
                temp += y + ' inherit\n'
            elif y == r'\lang':
                temp += y + ' english\n'
            elif y.lower() in charstyles:
                temp += y + ' default\n'
        return temp
    
    def expand(mname, sup_args, depth):
        '''Expand the macro (recursively if necessary).'''
        # substitute values for placeholders
        macexp = macdict.get(mname)[1]
        macprms = macdict.get(mname)[0]
        num_params = len(macprms)
        macprms = ['\n'] + macprms[:num_params - len(sup_args)] + sup_args
        for i in range(num_params, -1, -1):            
            macexp = macexp.replace('\n\\backslash\n' + str(i), macprms[i])
        # replace macro & inset with its expansion
        #  & expand included macros
        store = scan(iter(macexp.splitlines(True)), depth + 1)
        # return char styles to defaults
        store += output(depth + 1, defaults(macexp))
        return store

    def strip_outers(stuff):
        '''Strip enclosing layout statements.'''
        stuff = stuff.partition('\n')[2]
        stuff = stuff.rpartition(end_layout)[0]
        return stuff
    
    def inset_contents(iterable, keepouters):
        '''Get contents of inset +/- outer layout statements.'''
        contents = lines = ''
        insets = 1
        status = True
        bslash = False
        
        for line in iterable:
            lines += line
            # lose empties & status line
            if line == '\n':
                continue
            elif status:
                if status_open == line or status_coll == line:
                    status = False
                    continue
            elif begin_inset in line:
                insets += 1
                bslash = True
                contents += line
            elif end_inset in line:
                insets -= 1
                bslash = True
                if insets == 0:
                    if keepouters:
                        return contents, lines
                    else:
                        # strip outermost layout statements
                        temp = strip_outers(contents)
                        return temp, lines
                else:
                    contents += line
            elif backslash == line:
                if bslash:
                    contents += '\n'
                    bslash = False
                contents += line
            elif bkslash == line[0]:
                bslash = True
                contents += line
            else:
                contents += line
                bslash = False

    def indx(look_for, given):
        '''Return index of look_for in given.'''
        if look_for in given:
            return given.index(look_for)
        else:
            return len(given)

    def scan(iterable, depth):
        '''Parse the iterable line by line & resolve into output.'''
        
        # the 2nd is needed for the "toggle" macro
        flex_macro = r'\begin_inset Flex .expand macro'
        flex_macr0 = r'\begin_inset Flex .expand macro'
        
        lines = store = ''
        status = 0
        pending = starting = False
        params = supplied_args = []
        for line in iterable:
            if line in '\n':
                continue
            # scanning text, looking for macro & note insets
            elif status == 0:
                # a macro inset?
                if flex_macro in line:
                    status += 1
                    lines = line # store the line
                    defining = False
                # a note inset?
                elif begin_note in line and not starting:
                    store += output(depth, line)
                    if not scanotes:
                        # don't expand macros in notes
                        toss, temp = inset_contents(iterable, True)
                        store += output(depth, temp)
                # looking for toggle macro
                elif starting:
                    lines += line
                    if 'toggle\n' == line:
                        # found it!
                        flex_macro = flex_macr0
                        status += 1
                        defining = False
                        starting = False
                        if toggle_keep:
                            store += output(depth, lines)
                            lines = ''
                            store += output(depth, end_layout + '\n' \
                                        + end_inset + '\n')
                    # not the toggle macro
                    elif end_inset in line:
                        starting = False
                        store += output(depth, lines)
                        lines = ''
                # macro expansion off; is this the toggle macro?
                elif flex_macr0 in line:
                    lines = line
                    starting = True
                # otherwise write to file
                else:
                    store += output(depth, line)
                                   
            # in a macro inset
            elif status == 1:
                # get macro
                if re_macro.match(line):
                    m = re_macro.match(line)
                    macname = m.group(1) + m.group(2)
                    if macname not in macdict:
                        # a defining inset
                        if m.group(3) != '':
                            nparams = int(m.group(3))
                        else:
                            nparams = 0
                        lines += line
                        store += output(depth, lines)
                        lines = line = ''
                        defining = True
                        ndflts = 0
                        params = [globdef for x in range(nparams)]
                    elif macname == 'toggle':
                        # turn off macro expansion by misnaming (a hack)
                        flex_macro = r'\penguin_insect .expand macro'
                        if toggle_keep:
                            defining = True
                            lines += line
                            store += output(depth, lines)
                            lines = line = ''
                    elif m.group(3) == '0':
                        # delete macro from dictionary
                        macdict.pop(macname)
                        lines += line
                        store += output(depth, lines)
                        lines = line = ''
                        defining = True
                    else:
                        # a 'using' use; expansion looming
                        pending = True
                elif begin_note in line:
                    store += output(depth, line)
                    toss, temp = inset_contents(iterable, True)
                    store += output(depth, temp)
                elif end_inset in line:
                    if defining:
                        defining = False
                        store += output(depth, end_layout + '\n')
                        store += output(depth, line)
                        status -= 1
                    else:
                        # get arguments
                        supplied_args = []
                        status += 1
                # get default parameters
                elif flex_arg in line:
                    store += output(depth, line)
                    params[ndflts], temp = inset_contents(iterable, False)
                    ndflts += 1
                    store += output(depth, temp)
                # get macro expansion
                elif flex_macro in line:
                    store += output(depth, line)
                    expansion, temp = inset_contents(iterable, False)
                    macdict[macname] = [params, expansion]
                    params = []
                    store += output(depth, temp)
                else:
                    lines += line

            # get arguments (if any); expand macro
            elif status == 2:
                # get arguments (but not too many!)
                if flex_arg in line and \
                   len(supplied_args) < len(macdict.get(macname)[0]):
                    arg, toss = inset_contents(iterable, False)
                    # check if arg contains a top-level macro
                    if indx(flex_macro, arg) < indx(flex_arg, arg):
                        arg = scan(iter(arg.splitlines(True)), depth + 1)
                    # strip nested argument insets (if they exist)
                    if macname == 'peel':
                        if flex_arg in arg[:29]:
                            arg, toss = inset_contents(arg.splitlines(True)[1:], False)
                    arg = arg.rstrip()
                    # block (some) args of the conditionals
                    if (macname == 'if0' and arg != '')  or \
                       (macname == 'if1' and arg == ''):
                        continue
                    else:
                        supplied_args.append(arg)
                # macro following hard on another
                elif flex_macro in line:
                    # expand previous macro
                    store += output(depth, expand(macname, supplied_args, depth))
                    pending = False
                    # now parse this one
                    status = 1
                    defining = False
                    lines = line
                else:
                    # all args found; expand
                    store += output(depth, expand(macname, supplied_args, depth))
                    store += output(depth, line)
                    pending = False
                    status = 0
            
        if pending:
            store += output(depth, expand(macname, supplied_args, depth))
        return store
                            
    ######################################################                
    # write the prelims
    outfl.write(guff)

    # get the options
    parser = argparse.ArgumentParser(description='Expand text macros')

    parser.add_argument('-n', action ='store_true', default = False, \
                        help='Expand macros in notes')
    parser.add_argument('-t', action ='store_true', default = False, \
                        help='Retain toggle macros in document')
    parser.add_argument('-g', action ='store', default = '', \
                        help='Set global default value')

    scanotes = parser.parse_args(options).n
    toggle_keep = parser.parse_args(options).t
    globdef = parser.parse_args(options).g
    
    depth = 0
    scan(infl, depth)

    return 1
                
            
            
    

