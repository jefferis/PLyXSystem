# The 'master' script from which other scripts are called.
#
# pLyX.py
#
# Andrew Parsloe (aparsloe@clear.net.nz)
#
import argparse, re, sys, tempfile

parser = argparse.ArgumentParser(description='pLyX hub', \
                                     version='1.0')

##parser.add_argument('encdg', action ='store', \
##                    help='$$e Encoding')
##parser.add_argument('filep', action='store', \
##                    help='$$r Full pathname to the original LyX file \
##being processed ')
##parser.add_argument('filen', action ='store', \
##                    help='$$f Filename (with extension but without \
##directory path) of the LyX file')
##parser.add_argument('tempp', action='store', \
##                    help='$$p Full directory path of the LyX temporary \
##directory')
##parser.add_argument('basen', action='store', \
##                    help='$$b Base name (without extension) in the LyX \
##temp. directory')
##
parser.add_argument('infile', type=argparse.FileType('r'), \
                        help='Input file.')
parser.add_argument('outfile', type=argparse.FileType('w'), \
                        help='Output file.')

##encod = parser.parse_args().encdg # $$e
##fpath = parser.parse_args().filep # $$r
##fname = parser.parse_args().filen # $$f
##tpath = parser.parse_args().tempp # $$p
##bname = parser.parse_args().basen # $$b

fin = parser.parse_args().infile
fout = parser.parse_args().outfile

re_lyxcmds = re.compile(r'(\\\w+)|(status (open|collapsed))')
re_script = re.compile(r'Flex \..*\|(.*)$')
run_script = r'\begin_inset Flex .Run script'
end_inset = r'\end_inset'
flex = r'\begin_inset Flex'
begin_body = r'\begin_body'

begin_note = r'''\end_layout
\begin_layout Standard
\begin_inset Note Note
status open
'''
end_note = r'''\end_inset
\end_layout
\begin_layout Standard
'''

h_v = ['-h', '--help', '-v', '--version']

def helpmsg(msg):
    '''Send a help message to a yellow note in LyX.'''
    return begin_note + msg + end_note

def ishelpversn(optlist):
    '''Test if optlist contains -h, --help, -v, --version'''
    for s in [x.lower() for x in optlist]:
        if s in h_v:
            return h_v.index(s)
    return -1

def help_routine(this_help, infl, guff):
    fout.write(guff)
    fout.write(helpmsg(this_help))
    for line in infl:
        fout.write(line)
        
compressed = '''Compressed file? To sort, clear the Document > Compressed
setting and re-save your document.'''

def error(msg):
    sys.stderr.write(msg + '\n')
    sys.exit(1)

def get_pymods(infl):
    # store the prelims; get the modules and options
    scan = -1
    prelims = options = pymod = ''
    module_queue = []
    recorded = False
    for line in infl:
        # get contents of .Run script inset
        if scan > 0:
            prelims += line
            if end_inset in line:
                scan -= 1
                if scan > 0:
                    opts = options.split()
                    module_queue.append((pymod, opts))
                    pymod = options = ''
                    recorded = True
                else:
                    if not recorded:
                        opts = options.split()
                        module_queue.append((pymod, opts))
                        pymod = options = ''
                    return module_queue, prelims
            elif flex in line:
                scan += 1
                pymod = re_script.search(line).expand(r'\1')
            elif re_lyxcmds.match(line):
                continue
            else:
                options += line.strip('\n')

        # ".Run script" inset found
        elif run_script in line:
            scan += 1
            prelims += line

        # accumulate preliminary lines    
        elif scan == 0:
            prelims += line

        # doc. must not be in compressed format
        elif scan == -1:
            if re.search(r'LyX.*created', line):
                scan +=1
                prelims = line
            else:
                error(compressed)
    return [('',[])], ''

# Now run the scripts (if any)

scripts, prelims = get_pymods(fin)

if scripts[0][0] == '':
    # "Run script" help or version info.
    from pLyX_help import helpnote
    if scripts[0][1] != []:
        opt = scripts[0][1][0]
        hv = ishelpversn(scripts[0][1])
        if hv > -1:
            help_routine(helpnote(hv), fin, prelims)
        else:
            # unknown option
            from pLyX_help import whatopt
            help_routine(whatopt(), fin, prelims)            
    else:    
        # unknown or no custom inset inserted!
        from pLyX_help import unknown
        fin.seek(0)
        prelims = ''
        for line in fin:
            if begin_body in line:
                prelims += line
                help_routine(unknown(), fin, prelims)
            else:
                prelims += line
else:
    # run the script(s)
    ftemp = ['' for i in range(len(scripts) + 1)]
    ftemp[0] = fin
    ftemp[len(scripts)] = fout
    for i in range(len(scripts)):
        if i > 0:
            toss, prelims = get_pymods(ftemp[i])
        if i < (len(scripts) - 1):
            ftemp[i + 1] = tempfile.TemporaryFile(mode = 'w+t')
  
        scr = scripts[i][0]
        opts = scripts[i][1]
        
        runner = __import__('subscripts.' + scr, globals(), locals(), \
                            [scr], 0)
        helper = __import__('help.' + scr + '_help', globals(), locals(), \
                            [scr + '_help'], 0)
        hv = ishelpversn(opts)
        if hv > -1:
            help_routine(helper.helpnote(hv), ftemp[i], prelims)
            break
        else:
            if scr == 'break':
                ftemp[i + 1] = fout
            x = runner.main(ftemp[i], ftemp[i + 1], opts, prelims)
            ftemp[i].close()
            if x == 0:
                break
            else:               
                ftemp[i + 1].seek(0)
            
fout.close()

      






    

