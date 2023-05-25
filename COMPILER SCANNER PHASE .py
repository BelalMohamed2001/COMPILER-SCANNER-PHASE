import tkinter as tk
from enum import Enum
import re
import pandas
from tkinter import *


class Token_type(Enum):
    Program = 1
    Var = 2
    Const = 3
    Type = 4
    Function = 5
    Procedure = 6
    Begin = 7
    End = 8
    If = 9
    Then = 10
    Else = 11
    Case = 12
    Of = 13
    While = 14
    Do = 15
    Repeat = 16
    Until = 17
    For = 18
    To = 19
    Downto = 20
    Break = 21
    Continue = 22
    Exit = 23
    Array = 24
    Record = 25
    String = 26
    Integer = 27
    Real = 28
    Boolean = 29
    Char = 30
    Not = 31
    And = 32
    Or = 33
    Div = 34
    Mod = 35
    AssignOp = 36
    EqualOp = 37
    NotEqualOp = 38
    LessThanOp = 39
    GreaterThanOp = 40
    LessThanOrEqualOp = 41
    GreaterThanOrEqualOp = 42
    PlusOp = 43
    MinusOp = 44
    MultiplyOp = 45
    DivideOp = 46
    OpenParenthesis = 47
    CloseParenthesis = 48
    Semicolon = 49
    Colon = 50
    Comma = 51
    Dot = 52
    DoubleDot = 53
    SingleLineComment = 54
    MultiLineComment = 55
    Identifier = 56
    Number = 57
    LocalVariables = 58
    GlobalVariables = 59
    Read = 60
    ReadLn = 61
    Write = 62
    WriteLn = 63


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type

        }


ReservedWords = {
    Token_type.Program: "program",
    Token_type.Var: "var",
    Token_type.Const: "const",
    Token_type.Type: "type",
    Token_type.Function: "function",
    Token_type.Procedure: "procedure",
    Token_type.Begin: "begin",
    Token_type.End: "end",
    Token_type.If: "if",
    Token_type.Then: "then",
    Token_type.Else: "else",
    Token_type.Case: "case",
    Token_type.Of: "of",
    Token_type.While: "while",
    Token_type.Do: "do",
    Token_type.Repeat: "repeat",
    Token_type.Until: "until",
    Token_type.For: "for",
    Token_type.To: "to",
    Token_type.Downto: "downto",
    Token_type.Break: "break",
    Token_type.Continue: "continue",
    Token_type.Exit: "exit",
    Token_type.Array: "array",
    Token_type.Record: "record",
    Token_type.String: "string",
    Token_type.Integer: "integer",
    Token_type.Real: "real",
    Token_type.Boolean: "boolean",
    Token_type.Char: "char",
    Token_type.Not: "not",
    Token_type.And: "and",
    Token_type.Or: "or",
    Token_type.Div: "div",
    Token_type.Mod: "mod",
    Token_type.Identifier: "<identifier>",
    Token_type.Number: "<number>",
    Token_type.LocalVariables: "local variables",
    Token_type.GlobalVariables: "global variables",
    Token_type.Read: "read",
    Token_type.ReadLn: "readln",
    Token_type.Write: "write",
    Token_type.WriteLn: "writeln"
}

Operators = {
    ":=": Token_type.AssignOp,
    "=": Token_type.EqualOp,
    "<>": Token_type.NotEqualOp,
    "<": Token_type.LessThanOp,
    ">": Token_type.GreaterThanOp,
    "<=": Token_type.LessThanOrEqualOp,
    ">=": Token_type.GreaterThanOrEqualOp,
    "+": Token_type.PlusOp,
    "-": Token_type.MinusOp,
    "*": Token_type.MultiplyOp,
    "/": Token_type.DivideOp,
    "(": Token_type.OpenParenthesis,
    ")": Token_type.CloseParenthesis,
    ";": Token_type.Semicolon,
    ":": Token_type.Colon,
    ",": Token_type.Comma,
    ".": Token_type.Dot,
    "..": Token_type.DoubleDot,
    "{": Token_type.SingleLineComment,
    "}": Token_type.SingleLineComment,
    "{*": Token_type.MultiLineComment,
    "*}": Token_type.MultiLineComment,
    "'" : Token_type.String,
   

}

Tokens = []
errors = []


def find_token(text):
    current_state = None
    current_lex = ""
    text = text.lower()
    i = 0
    while i < len(text):
        char = text[i]

        if current_state is None:
            if char.isalpha():
                current_state = Token_type.Identifier
                current_lex += char
            elif char.isdigit():
                current_state = Token_type.Number
                current_lex += char
            elif char.isspace():
                i += 1
                continue
            elif char == "{":
                if text[i:i + 2] == "{*":
                    current_state = Token_type.MultiLineComment
                    current_lex = "{*"
                    i += 1
                else:
                    current_state = Token_type.SingleLineComment
                    current_lex = "{"
            elif char == "'":
                current_state = Token_type.String
                current_lex += char

            else:
                operators = [op for op in Operators.keys() if text[i:i + len(op)] == op]
                if operators:
                    operator = max(operators, key=len)
                    Tokens.append(token(operator, Operators[operator]))
                    i += len(operator)
                    continue
                else:
                    errors.append("Lexical error: Invalid character '" + char + "'")
        elif current_state == Token_type.Identifier:
            if char.isalnum() or char == '_':
                current_lex += char
            else:
                current_lex = current_lex.lower()
                if current_lex in ReservedWords.values():
                    for token_type, reserved_word in ReservedWords.items():
                        if reserved_word == current_lex:
                            Tokens.append(token(current_lex, token_type))
                            break
                else:
                    Tokens.append(token(current_lex, Token_type.Identifier))
                current_lex = ""
                current_state = None
                continue
        elif current_state == Token_type.Number:
            if char.isdigit() or char == '.':
                current_lex += char
            else:
                Tokens.append(token(current_lex, Token_type.Number))
                current_lex = ""
                current_state = None
                continue
        elif current_state == Token_type.SingleLineComment:
            if char == "}":
                Tokens.append(token(current_lex + char, Token_type.SingleLineComment))
                current_lex = ""
                current_state = None
            else:
                current_lex += char
        elif current_state == Token_type.MultiLineComment:
            if char == "*" and text[i:i + 2] == "*}":
                Tokens.append(token(current_lex + "*}", Token_type.MultiLineComment))
                current_lex = ""
                current_state = None
                i += 1
            else:
               current_lex += char

        elif current_state == Token_type.String:
            current_lex += char
            if char == "'":
                Tokens.append(token(current_lex, Token_type.String))
                current_lex = ""
                current_state = None

             

        i += 1

    if current_state == Token_type.Identifier and current_lex:
        current_lex = current_lex.lower()
        if current_lex in ReservedWords.values():
            for token_type, reserved_word in ReservedWords.items():
                if reserved_word == current_lex:
                    Tokens.append(token(current_lex, token_type))
                    break
        else:
            Tokens.append(token(current_lex, Token_type.Identifier))
    elif current_state == Token_type.Number and current_lex:
        Tokens.append(token(current_lex, Token_type.Number))
    elif current_state == Token_type.SingleLineComment and current_lex:
        Tokens.append(token(current_lex, Token_type.SingleLineComment))
    elif current_state == Token_type.MultiLineComment and current_lex:
        Tokens.append(token(current_lex, Token_type.MultiLineComment))
    elif current_state == Token_type.String and current_lex:
        errors.append("Lexical error: Unclosed string literal '" + current_lex + "'")

# GUI
class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pascal Lexical Analyzer")
        self.text_input = None
        self.output_frame = None
        self.output_text = None

        self.create_widgets()

    def create_widgets(self):
        # Text input
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        input_label = tk.Label(input_frame, text="Input:", background="black", font='bold', fg='white')
        input_label.pack(side=tk.LEFT)

        self.text_input = tk.Text(input_frame, height=15, width=60)
        self.text_input.pack()

        analyze_button = tk.Button(self.root, text="Analyze", command=self.analyze_text, background="black",
                                   font='bold', fg='white')
        analyze_button.pack(pady=10)

        # Output
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack()

    def analyze_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        Tokens.clear()
        errors.clear()
        find_token(text)

        self.display_output()

    def display_output(self):
        if self.output_text:
            self.output_text.destroy()

        self.output_text = tk.Text(self.output_frame, height=15, width=60)
        self.output_text.pack()

        # Display tokens
        self.output_text.insert(tk.END, "Tokens:\n")
        for token in Tokens:
            self.output_text.insert(tk.END, f"Lex: {token.lex}, Token Type: {token.token_type}\n")

        # Display errors
        self.output_text.insert(tk.END, "\nErrors:\n")
        for error in errors:
            self.output_text.insert(tk.END, f"{error}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()
