# MDMA — Formal Grammar (EBNF)

This document defines the `.mdma` file format using Extended Backus-Naur Form (EBNF).

```ebnf
(* Top-level file structure *)
file              = inputs-section , { block } ;

(* Inputs section *)
inputs-section    = "@inputs" , NEWLINE , { input-decl } ;
input-decl        = IDENTIFIER , ":" , type , [ "=" , default-value ] , NEWLINE ;

(* Types *)
type              = scalar-type | array-type ;
scalar-type       = "string" | "boolean" | "number" | "object" ;
array-type        = scalar-type , "[]" ;

(* Default values *)
default-value     = empty-array
                  | empty-string
                  | quoted-string
                  | boolean-literal
                  | number-literal
                  ;
empty-array       = "[" , "]" ;
empty-string      = '"' , '"' ;
quoted-string     = '"' , { any-char-except-quote } , '"' ;
boolean-literal   = "true" | "false" ;
number-literal    = [ "-" ] , digit , { digit } , [ "." , digit , { digit } ] ;

(* Named blocks *)
block             = block-header , block-body ;
block-header      = simple-header | open-header ;
simple-header     = "<" , block-name , ">" , NEWLINE ;
open-header       = "<" , [ block-name ] , NEWLINE ,
                     [ block-name , NEWLINE ] ,
                     { modifier-line } ,
                     ">" , NEWLINE ;
block-name        = ( letter | digit ) , { letter | digit | "-" } ;
modifier-line     = multiple-modifier | name-modifier ;
multiple-modifier = "multiple" , ":" , IDENTIFIER , "in" , IDENTIFIER , NEWLINE ;
name-modifier     = "name" , ":" , expression , NEWLINE ;
block-body        = { template-line | content-line | NEWLINE } ;

(* Template lines (may be mixed with content on the same line) *)
template-line     = { content-char | interpolation | control-tag } , NEWLINE ;
interpolation     = ( "{{" | "{{-" ) , expression , ( "}}" | "-}}" ) ;
control-tag       = ( "{%" | "{%-" ) , statement , ( "%}" | "-%}" ) ;

(* Statements inside {% %} *)
statement         = if-stmt | elif-stmt | else-stmt | endif-stmt
                  | for-stmt | endfor-stmt
                  ;
if-stmt           = "if" , expression ;
elif-stmt         = "elif" , expression ;
else-stmt         = "else" ;
endif-stmt        = "endif" ;
for-stmt          = "for" , IDENTIFIER , "in" , expression ;
endfor-stmt       = "endfor" ;

(* Expressions *)
expression        = primary , { pipe-filter } ;
primary           = variable | string-literal | number-literal | boolean-literal
                  | comparison | logical-expr
                  ;
variable          = IDENTIFIER , { "." , IDENTIFIER } ;
pipe-filter       = "|" , IDENTIFIER , [ "(" , filter-args , ")" ] ;
filter-args       = expression , { "," , expression } ;
comparison        = expression , comparator , expression ;
comparator        = "==" | "!=" | ">" | ">=" | "<" | "<=" ;
logical-expr      = expression , logical-op , expression
                  | "not" , expression
                  ;
logical-op        = "and" | "or" ;

(* Terminals *)
IDENTIFIER        = letter , { letter | digit | "_" } ;
NEWLINE           = "\n" | "\r\n" ;
letter            = "a" | ... | "z" | "A" | ... | "Z" | "_" ;
digit             = "0" | ... | "9" ;
```

## Notes

- Whitespace between tokens within a line is flexible (extra spaces are ignored in the inputs section and block headers).
- The `-` whitespace-control modifier on `{{-`, `-}}`, `{%-`, `-%}` is lexically part of the delimiter and affects the surrounding rendered whitespace, not the expression itself.
- Block names are case-sensitive. `<Title>` and `<title>` are distinct blocks.
- `multiple` is a reserved word and may not be used as a block name or input identifier. `name` is *not* reserved (e.g. `name: string` is a valid input) -- it's only recognized as a modifier keyword inside a block's own multi-line header, never as a standalone tag, so it never collides with an input declaration or a block literally named `name`.
- There is exactly one delimiter for "this is a block declaration": angle brackets. A block with no modifiers is the single-line `simple-header` (`<blockname>`). A block with `multiple` and/or `name` uses `open-header`, which spans multiple lines like an HTML tag with attributes: `<` opens, each modifier is a bare `key: value` line, and a lone `>` closes it.
- In `open-header`, the block name appears in exactly one of two positions: inline right after `<` (`<blockname`, continuing on the next line), or alone on the line immediately following a bare `<`. No blank lines are permitted between the opening `<` and the closing `>`.
- `multiple` and `name` modifier lines may appear in either order within `open-header`. `name` is only valid when `multiple` is also present in the same header.
- A block with `multiple` and no `name` renders to an array of strings; adding `name` renders it to an object keyed by each item's computed name instead.
