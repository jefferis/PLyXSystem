def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail

header = r'''\begin_layout LyX-Code
\family roman
\series bold
.Run script(s)           
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 1.0 (3 December 2012)
\family default
.stop
\family roman
 script introduced.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.2 (1 November 2012) First version to allow multiple scripts to be run.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.1 (6 October 2012)
\end_layout
'''
tail = r'''\begin_layout LyX-Code
\family roman
Run a script a script or scripts manipulating the current document.           
\end_layout
\begin_layout LyX-Code
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
Global options
\series default
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-h --help  
\series default
show this help note.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-v --version  
\series default
show version information.
\end_layout
\begin_layout LyX-Code
\end_layout
\begin_layout LyX-Code
\family roman
To run a script (or scripts), insert a 
\begin_inset Quotes els
\end_inset

dotted
\begin_inset Quotes ers
\end_inset
 inset (or insets) from those listed under 
\family sans
Insert \SpecialChar \menuseparator
 Custom Insets
\family roman
. Into the inset (or insets) insert any desired 
\emph on
global
\emph default
 options, e.g.,
 
\begin_inset Flex .Run script(s)
status open
\begin_layout Plain Layout
\family roman
\begin_inset Flex .calculate formula|calcul8
status open
\begin_layout Plain Layout
\family roman
-h
\end_layout
\end_inset
\end_inset
 to see the help note for the
 
\family sans
.calculate formula
\family roman
 inset.
\end_layout
'''

def unknown():
    return r'''\begin_layout LyX-Code
\family roman
Unknown script (or no script) specified! Ensure the 
\family typewriter
pLyX
\family roman
 module has been added
 to your document and insert the 
\family sans
.Run script(s)
\family roman
 custom inset in place of this note (perhaps with the  
\series bold
-h
\series default
 or
 \series bold
--help
\series default
 option entered in it).
\end_layout
'''

def whatopt():
    return r'''\begin_layout LyX-Code
\family roman
Unknown option specified!
\end_layout
\begin_layout LyX-Code
\family roman
 Enter 
\series bold
-h
\series default
 for help.
\end_layout
'''

