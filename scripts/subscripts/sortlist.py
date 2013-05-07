# Sort a list & sub-lists according to a sort specifation. 
# Part of of the pLyX system; not an independent script. 
#
# Andrew Parsloe (aparsloe@clear.net.nz)
#
import re, argparse, tempfile
from operator import itemgetter

re_lyxcmds = re.compile(r'(\\\w+)|(status (open|collapsed))')
re_itemkind = re.compile(r'\\begin_layout (Labeling|Enumerate|Description|Itemize)')

begin_inset = r'\begin_inset'
end_inset = r'\end_inset'
begin_layout = r'\begin_layout'
end_layout = r'\end_layout'
flex_list = r'\begin_inset Flex .sort list'
item_desc = r'\begin_layout Description'
item_enum = r'\begin_layout Enumerate'
item_label = r'\begin_layout Labeling'
item_ize = r'\begin_layout Itemize'
begin_deeper = r'\begin_deeper'
end_deeper = r'\end_deeper'
end_body = r'\end_body'

def main(infl, outfl, opts, guff):
    '''Sort (nested) lists.'''

    parser = argparse.ArgumentParser(description = 'Sort notes?')

    parser.add_argument('-n', '--notes', dest='n', action ='store_true', \
                    default = False, help="Makes LyX's (e.g. yellow) notes sortable")
    parser.add_argument('-a', action ='store_true', \
                    default = False, help="Sort across list-type boundaries")
    parser.add_argument('-c', action ='store', type = int, default = 20, \
                    help="No. of chars in the sort key")

    sort_notes = parser.parse_args(opts).n
    sort_all = parser.parse_args(opts).a
    nchars = parser.parse_args(opts).c
    
    def get_list_kind(infile, outfile):
        '''Itemize? Labeling? Enumerate? Description?'''
        for line in infile:
            # find item kind
            if re_itemkind.match(line):
                temp = r'\begin_layout ' + \
                            re_itemkind.match(line).expand(r'\1')
                return temp
            else:
                outfile.write(line)

    def sort_list(infile, outfile, dpth, sorter, updn, list_kind):
        '''Do the sort.'''
        
        def include_inset(notes):
            '''Include insets without sorting unless notes is True.'''
            count = 1
            temp = nqey = ''
            for line in infile:
                temp += line
                if begin_inset in line:
                    count += 1
                elif end_inset in line:
                    count -= 1
                    if count == 0:
                        return temp, nqey
                elif notes:
                    if re_lyxcmds.match(line):
                        continue
                    else:
                        nqey += line.strip()
                        
        #######################################
        list_type_change = False
        layouts = 1
        items = []
        qey = ''
        if list_kind == None:
            list_kind = ''
        current_item = list_kind + '\n'
        for line in infile:
            # get item & sort key
            if begin_deeper in line:
                current_item += line
                lkind = get_list_kind(infile, outfile)
                current_item += sort_list(infile, outfile, dpth + 1, sorter, updn, lkind)
                items[-1] = (qey, current_item)
            elif end_deeper in line:
                items.sort(key=itemgetter(0), reverse=updn[dpth])
                cur_items = ''
                for i in range(len(items)):
                    cur_items += items[i][1]
                cur_items += line
                return cur_items
            elif begin_inset in line:
                current_item += line
                if sort_notes and 'Note Note' in line:
                    tmp1, tmp2 = include_inset(sort_notes)
                else:
                    tmp1, tmp2 = include_inset(False)
                current_item += tmp1
                qey += tmp2
            elif begin_layout in line:
                # list-type change; continue sorting?
                if list_kind  in line or \
                   (re_itemkind.match(line) and (dpth > 0 or sort_all)):
                    current_item = line
                    layouts = 1
                    qey = ''
                else:
                    items.sort(key=itemgetter(0), reverse=updn[dpth])
                    cur_items = ''
                    for i in range(len(items)):
                        cur_items += items[i][1]
                    cur_items += line
                    return cur_items
            elif end_body in line:
                items.sort(key=itemgetter(0), reverse=updn[0])
                cur_items = ''
                for i in range(len(items)):
                    cur_items += items[i][1]
                cur_items += line
                return cur_items
            elif end_layout in line:
                current_item += line
                layouts -= 1
                if layouts == 0:
                    if sorter[dpth] in 'az':
                        qey = qey.lower()[:nchars]
                    elif sorter[dpth] in 'AZ':
                        qey = qey[:nchars]
                    elif sorter[dpth] in 'nN':
                        qey = '0'
                    elif sorter[dpth] in 'PM':
                        qey = float(qey)
                    items.append((qey, current_item))
            elif re_lyxcmds.search(line):
                current_item += line
            else:
                current_item += line
                qey += line.strip()

    

    ###############################################
    # write the prelims to file
    outfl.write(guff)
        
    list_status = 0
    for line in infl:
        # find sort spec. inset
        if list_status == 0:   
            outfl.write(line)
            if flex_list in line:
                list_status += 1
                sort_spec = ''
                insets = 1
        
        #get sort spec.
        elif list_status == 1:
            outfl.write(line)
            if begin_inset in line:
                insets += 1
            elif end_inset in line:
                insets -= 1
                if insets == 0:
                    # groom sort_spec to std form
                    sp = sort_spec.replace('+', 'P')
                    sp = sp.replace('-', 'M')
                    specs = sp.split('/')
                    repeats = len(specs)
                    for s in range(repeats):
                        specs[s] = re.sub(r'\W', '', specs[s])
                    levels = [[] for i in range(repeats)]
                    sort_type = [[] for i in range(repeats)]
                    for i in range(repeats):
                        levels[i] = [int(n) for n in re.findall(r'(\d)', specs[i])]
                        sort_type[i] = re.findall(r'\d(\w)', specs[i])
                    sorting = ['N' for j in range(6)]
                    
                    ftemp = ['' for i in range(repeats+1)]
                    ftemp[0] = infl
                    ftemp[repeats] = outfl
                    
                    for i in range(repeats):
                        # do lesser sorts before primary
                        for j in levels[repeats - i - 1]:
                            k = levels[repeats - i - 1].index(j)
                            sorting[j - 1] = sort_type[repeats - i - 1][k]
                        if i < repeats - 1:
                                ftemp[i+1] = tempfile.TemporaryFile(mode = 'w+t')
                        updn = [s in '-Zz' for s in sorting] 
                        depth = 0
                        list_kind = get_list_kind(ftemp[i], ftemp[i+1])
                        ftemp[i+1].write(sort_list(ftemp[i], ftemp[i+1], depth, sorting, updn, list_kind))
                        if i > 0:
                            ftemp[i].close()
                        if i < repeats - 1:
                            ftemp[i+1].seek(0)
                        list_status = 0
            elif re_lyxcmds.search(line):
                continue
            else:
                sort_spec += line.strip()
        else:
            outfl.write(line)
            
    return 1 




