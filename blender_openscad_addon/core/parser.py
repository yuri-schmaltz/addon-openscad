from __future__ import annotations

from .ast import BooleanOp, ColorOp, Primitive, Program, RawCall, Transform
from .tokenizer import Token, tokenize


class ParseError(ValueError):
  pass


class Parser:
  def __init__(self, source: str):
    self.tokens = tokenize(source)
    self.idx = 0

  def peek(self) -> Token:
    return self.tokens[self.idx]

  def advance(self) -> Token:
    t = self.tokens[self.idx]
    self.idx += 1
    return t

  def expect_symbol(self, sym: str) -> None:
    t = self.advance()
    if t.kind != "symbol" or t.value != sym:
      raise ParseError(f"Esperado '{sym}' na posicao {t.index}")

  def expect_ident(self) -> str:
    t = self.advance()
    if t.kind != "ident":
      raise ParseError(f"Identificador esperado na posicao {t.index}")
    return t.value

  def parse_number(self) -> float:
    t = self.advance()
    if t.kind != "number":
      raise ParseError(f"Numero esperado na posicao {t.index}")
    return float(t.value)

  def parse_array(self) -> list[float]:
    self.expect_symbol("[")
    values: list[float] = []
    while True:
      if self.peek().kind == "symbol" and self.peek().value == "]":
        self.advance()
        break
      values.append(self.parse_number())
      if self.peek().kind == "symbol" and self.peek().value == ",":
        self.advance()
        continue
      self.expect_symbol("]")
      break
    return values

  def parse_args(self) -> dict[str, object]:
    args: dict[str, object] = {}
    self.expect_symbol("(")
    auto = 0
    while True:
      t = self.peek()
      if t.kind == "symbol" and t.value == ")":
        self.advance()
        break

      if t.kind == "ident":
        t2 = self.tokens[self.idx + 1]
        if t2.kind == "symbol" and t2.value == "=":
          name = self.advance().value
          self.advance()
          args[name] = self.parse_value()
        else:
          args[f"arg{auto}"] = self.parse_value()
          auto += 1
      else:
        args[f"arg{auto}"] = self.parse_value()
        auto += 1

      if self.peek().kind == "symbol" and self.peek().value == ",":
        self.advance()
        continue
    return args

  def parse_value(self):
    t = self.peek()
    if t.kind == "number":
      return self.parse_number()
    if t.kind == "symbol" and t.value == "[":
      return self.parse_array()
    raise ParseError(f"Valor invalido na posicao {t.index}")

  def parse_block(self) -> list:
    self.expect_symbol("{")
    items = []
    while not (self.peek().kind == "symbol" and self.peek().value == "}"):
      items.append(self.parse_statement())
    self.expect_symbol("}")
    return items

  def parse_statement(self):
    name = self.expect_ident()
    args = self.parse_args()

    if name in {"translate", "rotate", "scale"}:
      vals = args.get("arg0")
      if not isinstance(vals, list):
        raise ParseError(f"{name} espera vetor")
      body = self.parse_block()
      return Transform(kind=name, values=[float(v) for v in vals], body=body)

    if name in {"union", "difference", "intersection"}:
      body = self.parse_block()
      return BooleanOp(kind=name, body=body)

    if name == "color":
      vals = args.get("arg0")
      if not isinstance(vals, list):
        raise ParseError("color() espera vetor [r,g,b] ou [r,g,b,a]")
      body = self.parse_block()
      return ColorOp(rgba=[float(v) for v in vals], body=body)

    if name in {"cube", "sphere", "cylinder"}:
      self.expect_symbol(";")
      return Primitive(kind=name, args=args)

    self.expect_symbol(";")
    return RawCall(name=name, args=args)

  def parse_program(self) -> Program:
    out = []
    while self.peek().kind != "eof":
      out.append(self.parse_statement())
    return Program(statements=out)


def parse_scad(source: str) -> Program:
  return Parser(source).parse_program()
