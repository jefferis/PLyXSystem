# Undo for pLyX system. Writes the backup 
# file over the current buffer. Called thus:
#
# python <path to>/qLyX.py [-b <path to backup directory>] $$r $$f $$o
#
# Andrew Parsloe (aparsloe@clear.net.nz) 13 October 2012
#

import argparse, re

parser = argparse.ArgumentParser(description='pLyX undo-er', version='1.0')

parser.add_argument('-b', '--backup', action = 'store', dest = 'b', default = '', \
                    help="Backup directory with path e.g. E:/Lymbo")
parser.add_argument('filepath', action='store', \
                    help='$$r Full pathname to the LyX file being processed e.g. D:/Documents/')
parser.add_argument('filename', action ='store', \
                    help='$$f Filename (with extension) of the LyX file e.g. myfile.lyx')

parser.add_argument('outfile', type=argparse.FileType('w'), \
                        help='Output file.')

bpath = parser.parse_args().b # backup path name
fname = parser.parse_args().filename # $$f filename
fpath = parser.parse_args().filepath # $$r path to file
fout = parser.parse_args().outfile

#backup filename
if bpath != '':
    bfname = re.sub(r':|/', r'!', fpath) + fname + '~'
else:
    bfname = fname + '~'
    bpath = fpath

fin = open(bpath + '/' + bfname, 'r')
for line in fin:
    fout.write(line)
    
fin.close()
fout.close()

   







