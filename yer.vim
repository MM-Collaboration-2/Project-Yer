" Vim syntax file for the language

" Define the language name and file extensions
if exists("b:current_syntax")
  finish
endif

" Integer with - + or nothing in front
syn match yerNumber '\d\+'
syn match yerNumber '[-+]\d\+'

" Floating point number with decimal no E or e 
syn match yerNumber '[-+]\d\+\.\d*'

syn keyword yerBlockCmd Expr While If For Func
syn match yerComment '\'.*\''
syn match yerString '".*"'
syn match yerVariable '[a-zA-Z_][a-zA-Z0-9_]*'
syn match yerFunction '[a-zA-Z_][a-zA-Z0-9_]*\ze('

let b:current_syntax = "yer"
" hi Type guifg=#008787
hi def link yerNumber      Constant
hi def link yerBlockCmd    Conditional
hi def link yerComment     Comment
hi def link yerString      String
hi def link yerFunction    Function
hi def link yerVariable    Type " for some reason Variable here is just plain color


