def helpnote(hv):
    if hv > 1:
        return header + version
    else:
        return header + tail
    
header = r'''\begin_layout LyX-Code
\family roman
\series bold
.expand macros           
\end_layout
'''
version = r'''\begin_layout LyX-Code
\family roman
Version 1.0 (30 December 2012)
 'invisible punctuator'; reversal of substitution order; built-in 'peel' macro.  
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.6 (20 December 2012)
 expand arguments containing top-level macros before passing to the parent macro.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.5 (c.1 December 2012)
 built-in 'if0' and 'if1' macros.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.4 (10 November 2012)
 built-in 'toggle' macro.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.3 (21 October 2012)
 first version for the pLyX system.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.2 (18 October 2012)
 first functioning script using insets instead of markers.
\end_layout
\begin_layout LyX-Code
\family roman
Version 0.1 (13 October 2012)
 first script for expanding abbreviations.
\end_layout
'''
tail = r'''\begin_layout LyX-Code
\family roman
Define and expand text macros.
\end_layout
\begin_layout LyX-Code

\end_layout
\begin_layout LyX-Code
\family roman
\series bold
Global options
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
\family roman
\series bold
-g  
\series default
 set global default value for arguments; the default is the empty string.
 E.g. 
\series bold
-g *
\series default
 sets the global default to *.
\end_layout
\begin_layout LyX-Code
\family roman
\series bold
-n   
\series default
make macros within (yellow) notes expandable; default 
\series bold
False
\series default
.
\end_layout
\begin_layout LyX-Code

\end_layout
\begin_layout LyX-Code
\family roman
\series bold
Defining macros
\end_layout
\begin_layout LyX-Code
\family roman
\emph on
Example 1:
\end_layout
\begin_layout LyX-Code
\family roman
\begin_inset Flex .expand macro|txtmacs
status open
\begin_layout Plain Layout
\family roman
Lp
\begin_inset Flex .expand macro|txtmacs
status open

\begin_layout Plain Layout
\begin_inset Formula ${\displaystyle \left(\frac{\partial^{2}}{\partial x^{2}}+\frac{\partial^{2}}{\partial y^{2}}+\frac{\partial^{2}}{\partial z^{2}}\right)\phi=0}$
\end_inset
\end_layout
\end_inset
\end_layout
\end_inset
\end_layout
\begin_layout LyX-Code
\family roman
defines a 
\begin_inset Quotes els
\end_inset

pure abbreviation
\begin_inset Quotes ers
\end_inset

 macro 
\series bold
Lp
\series default
 (one with no parameters) which expands to Laplace's equation in mathematical
 display format: 
\family default

\begin_inset Flex .expand macro|txtmacs
status open

\begin_layout Plain Layout

\family roman
Lp
\end_layout

\end_inset


\end_layout

\begin_layout LyX-Code

\family roman
\emph on
Example 2: 
\end_layout

\begin_layout LyX-Code

\family roman
\begin_inset Flex .expand macro|txtmacs
status open

\begin_layout Plain Layout

\family roman
hg 1 
\begin_inset Flex .[argument]
status collapsed

\begin_layout Plain Layout

\family roman
h
\end_layout

\end_inset

 
\begin_inset Flex .expand macro|txtmacs
status open

\begin_layout Plain Layout

\family roman

\backslash
1yperbolic geometry
\end_layout

\end_inset


\end_layout

\end_inset


\end_layout

\begin_layout LyX-Code

\family roman
shows the definition of a macro 
\series bold
hg
\series default
 with one parameter.
 The default value of the parameter is 
\begin_inset Quotes els
\end_inset

h
\begin_inset Quotes ers
\end_inset

. Using 
\begin_inset Quotes els
\end_inset

=>
\begin_inset Quotes ers
\end_inset

 to mean 
\begin_inset Quotes els
\end_inset

expands to
\begin_inset Quotes ers
\end_inset

,
\end_layout

\begin_layout LyX-Code

\family roman
\begin_inset Flex .expand macro|txtmacs
status collapsed

\begin_layout Plain Layout

\family roman
hg
\end_layout

\end_inset

 => hyperbolic geometry
\end_layout

\begin_layout LyX-Code

\family roman
\begin_inset Flex .expand macro|txtmacs
status collapsed

\begin_layout Plain Layout

\family roman
hg
\end_layout

\end_inset


\begin_inset Flex .[argument]
status collapsed

\begin_layout Plain Layout

\family roman
H
\end_layout

\end_inset

 => Hyperbolic geometry
\end_layout

\begin_layout LyX-Code

\family roman
so that the latter is appropriate for use at the start of a sentence.
\end_layout

\begin_layout LyX-Code

\family roman
\emph on
Example 3:
\end_layout

\begin_layout LyX-Code

\family roman
\begin_inset Flex .expand macro|txtmacs
status open

\begin_layout Plain Layout

\family roman
tp 2 
\family default

\begin_inset Flex .[argument]
status collapsed

\begin_layout Plain Layout
File Handling
\end_layout

\end_inset


\family roman

\begin_inset Flex .[argument]
status collapsed

\begin_layout Plain Layout
File Formats
\end_layout

\end_inset


\family sans

\begin_inset Flex .expand macro|txtmacs
status open

\begin_layout Plain Layout

\family sans
Tools \SpecialChar \menuseparator
 Preferences \SpecialChar \menuseparator
 
\backslash
1 \SpecialChar \menuseparator
 
\backslash
2
\end_layout

\end_inset


\end_layout

\end_inset


\end_layout

\begin_layout LyX-Code

\family roman
defines the macro 
\series bold
tp
\series default
 with two parameters, for both of which default values are given (but specifying
 default values for some or all parameters is not essential).
 Thus 
\end_layout

\begin_layout LyX-Code

\family roman
\begin_inset Flex .expand macro|txtmacs
status collapsed

\begin_layout Plain Layout

\family roman
tp
\end_layout

\end_inset

 => 
\family sans
Tools \SpecialChar \menuseparator
 
Preferences \SpecialChar \menuseparator
 File Handling \SpecialChar \menuseparator
 File Formats
 
\end_layout

\begin_layout LyX-Code

\family roman
\begin_inset Flex .expand macro|txtmacs
status collapsed

\begin_layout Plain Layout

\family roman
tp
\end_layout

\end_inset


\family default

\begin_inset Flex .[argument]
status collapsed

\begin_layout Plain Layout

\family roman
Converters
\end_layout

\end_inset


\family roman
 =>  
\family sans
Tools \SpecialChar \menuseparator
 Preferences \SpecialChar \menuseparator
 File Handling \SpecialChar \menuseparator
 Converters
 
\end_layout

\begin_layout LyX-Code

\family roman
\begin_inset Flex .expand macro|txtmacs
status collapsed

\begin_layout Plain Layout

\family roman
tp
\end_layout

\end_inset


\begin_inset Flex .[argument]
status collapsed

\begin_layout Plain Layout
Editing
\end_layout

\end_inset


\family default

\begin_inset Flex .[argument]
status collapsed

\begin_layout Plain Layout
Shortcuts
\end_layout

\end_inset


\family roman
 => 
\family sans
Tools \SpecialChar \menuseparator
 Preferences \SpecialChar \menuseparator
 Editing \SpecialChar \menuseparator
 Shortcuts
\end_layout

\begin_layout LyX-Code

\end_layout

\begin_layout LyX-Code

\family roman
\emph on
Parameters
\end_layout

\begin_layout LyX-Code

\family roman
Parameters are entered in  an 
\family sans
.[argument]
\family roman
 inset: the contents of an 
\family sans
.[argument]
\family roman
 inset are invisible to LaTeX and have no effect on the pdf.
 Parameters are numbered from 
\backslash
1,
\backslash
2, ...
\end_layout

\begin_layout Itemize
The contents of both macro and argument insets are invisible to LaTeX.
\end_layout

\begin_layout Itemize

\family roman
More than one macro may be defined in a macro inset, but each must start
 on a new line in native LyX format (check
\family sans
View Source
\family roman.
\end_layout

\begin_layout Itemize

\family roman
An expansion may include other macros.
\end_layout

\begin_layout Itemize

\family roman
An expansion may be a word or phrase, or a multi-paragraph passage, containing
 text and character formatting, an equation, a graphic, indeed anything
 that can be displayed in LyX. It may contain parameters and other macros.
\end_layout

\begin_layout Itemize
A macro must be defined 
\emph on
before
\emph default
 its first use in the text (but the order of definition within an inset
 is immaterial).
\end_layout

\begin_layout Itemize
Use the built-in macro
\series bold
 toggle
\series default
 to stop macro expansion thereafter or, used again, to start it again.
\end_layout

\begin_layout LyX-Code

\family roman
\series bold
Shortcuts
\end_layout

\begin_layout LyX-Code

\family roman
Convenient keyboard shortcuts are needed for the 
\family sans
Macro
\family roman
 and 
\family sans
.[argument]
\family roman
 insets, and also for 
\begin_inset Quotes els
\end_inset

jumping
\begin_inset Quotes ers
\end_inset

 out of an inset (to the right), so that the cursor is correctly placed
 for further input.
 Perhaps (after removing the current assignment of 
\family sans
 Ctrl+K
\family roman
):
\end_layout

\begin_layout Itemize

\series bold
flex-insert 
\begin_inset Quotes eld
\end_inset

.expand macro|txtmacs
\begin_inset Quotes erd
\end_inset


\series default
 <=> 
\family sans
Ctrl+K
\family roman
 (or 
\family sans
 Ctrl+H
\family roman
)
\end_layout

\begin_layout Itemize

\series bold
flex-insert .[argument]
\series default
 <=> 
\family sans
Ctrl+;
\end_layout

\begin_layout Itemize

\series bold
command-sequence line-end; char-right; toggle-inset;
\series default
 <=> 
\family sans
Ctrl+J 
\family default
(J as in Jump)
\end_layout
'''

