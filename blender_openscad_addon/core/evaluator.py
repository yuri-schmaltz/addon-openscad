from __future__ import annotations

from .ast import BooleanOp, ColorOp, EvalItem, Primitive, Program, RawCall, Transform


def _eval_node(node, transform_chain=None, color=None):
  transform_chain = list(transform_chain or [])

  if isinstance(node, Primitive):
    return EvalItem(
      node_type="primitive",
      primitive=node,
      transform_chain=transform_chain,
      color=color,
    )

  if isinstance(node, Transform):
    chain = transform_chain + [(node.kind, node.values)]
    return EvalItem(
      node_type="group",
      transform_chain=transform_chain,
      children=[_eval_node(ch, chain, color) for ch in node.body],
      color=color,
    )

  if isinstance(node, BooleanOp):
    return EvalItem(
      node_type="boolean",
      boolean_kind=node.kind,
      transform_chain=transform_chain,
      children=[_eval_node(ch, transform_chain, color) for ch in node.body],
      color=color,
    )

  if isinstance(node, ColorOp):
    rgba = list(node.rgba)
    if len(rgba) == 3:
      rgba.append(1.0)
    return EvalItem(
      node_type="group",
      transform_chain=transform_chain,
      children=[_eval_node(ch, transform_chain, rgba) for ch in node.body],
      color=rgba,
    )

  if isinstance(node, RawCall):
    return EvalItem(node_type="noop", transform_chain=transform_chain)

  return EvalItem(node_type="noop", transform_chain=transform_chain)


def evaluate_program(program: Program) -> list[EvalItem]:
  return [_eval_node(stmt) for stmt in program.statements]
