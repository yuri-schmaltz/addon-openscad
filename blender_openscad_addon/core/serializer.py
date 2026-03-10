from __future__ import annotations

import bpy


def _fmt_vec(values):
  return "[" + ", ".join(f"{v:.6f}" for v in values) + "]"


def serialize_object_to_scad(obj: bpy.types.Object) -> str:
  if obj.type != "MESH":
    return f"// Objeto {obj.name} nao e mesh\n"

  mesh = obj.data
  verts = [obj.matrix_world @ v.co for v in mesh.vertices]
  faces = [list(p.vertices) for p in mesh.polygons]

  lines = []
  lines.append(f"// Exportado de Blender: {obj.name}")
  lines.append("polyhedron(")
  lines.append("  points=[")
  for v in verts:
    lines.append(f"    {_fmt_vec((v.x, v.y, v.z))},")
  lines.append("  ],")
  lines.append("  faces=[")
  for f in faces:
    lines.append("    [" + ", ".join(str(i) for i in f) + "],")
  lines.append("  ]")
  lines.append(");")
  return "\n".join(lines) + "\n"
