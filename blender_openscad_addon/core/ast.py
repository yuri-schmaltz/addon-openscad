from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class Node:
  pass


@dataclass
class Program(Node):
  statements: List[Node] = field(default_factory=list)


@dataclass
class Primitive(Node):
  kind: str
  args: dict[str, Any]


@dataclass
class Transform(Node):
  kind: str
  values: list[float]
  body: list[Node] = field(default_factory=list)


@dataclass
class BooleanOp(Node):
  kind: str
  body: list[Node] = field(default_factory=list)


@dataclass
class ColorOp(Node):
  rgba: list[float]
  body: list[Node] = field(default_factory=list)


@dataclass
class RawCall(Node):
  name: str
  args: dict[str, Any]


@dataclass
class EvalItem:
  node_type: str
  primitive: Optional[Primitive] = None
  transform_chain: list[tuple[str, list[float]]] = field(default_factory=list)
  boolean_kind: Optional[str] = None
  children: list["EvalItem"] = field(default_factory=list)
  color: Optional[list[float]] = None
