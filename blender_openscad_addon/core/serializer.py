from __future__ import annotations

import bpy


def _fmt_vec(values):
  return "[" + ", ".join(f"{v:.6f}" for v in values) + "]"


def serialize_object_to_scad(obj: bpy.types.Object) -> str:
  if obj.type != "MESH":
    return f"// Objeto {obj.name} nao e mesh\n"

  # Smart Primitive Interceptor
  has_destructive_modifiers = any(m.type not in ('MIRROR', 'SOLIDIFY') for m in obj.modifiers)
  
  lines = []
  lines.append(f"// Exportado de Blender: {obj.name}")
  
  if not has_destructive_modifiers:
    primitive_type = None
    # Crude primitive matching using names or vertex count/bounds
    # Cube: 8 verts, 6 polygons
    if len(obj.data.vertices) == 8 and len(obj.data.polygons) == 6:
       primitive_type = "cube"
    elif "Sphere" in obj.data.name or "Sphere" in obj.name:
       # Approximated
       primitive_type = "sphere"
       
    if primitive_type == "cube":
      sx = obj.scale.x * obj.dimensions.x / (obj.scale.x if obj.scale.x != 0 else 1)
      sy = obj.scale.y * obj.dimensions.y / (obj.scale.y if obj.scale.y != 0 else 1)
      sz = obj.scale.z * obj.dimensions.z / (obj.scale.z if obj.scale.z != 0 else 1)
      loc = obj.location
      return "".join(lines) + f"\ntranslate([{loc.x:.6f}, {loc.y:.6f}, {loc.z:.6f}])\n  cube([{sx:.6f}, {sy:.6f}, {sz:.6f}], center=true);\n"
    elif primitive_type == "sphere":
      r = max(obj.dimensions.x, obj.dimensions.y, obj.dimensions.z) / 2.0
      loc = obj.location
      return "".join(lines) + f"\ntranslate([{loc.x:.6f}, {loc.y:.6f}, {loc.z:.6f}])\n  sphere(r={r:.6f});\n"

  # Fallback to Polyhedron
  mesh = obj.data
  verts = [obj.matrix_world @ v.co for v in mesh.vertices]
  faces = [list(p.vertices) for p in mesh.polygons]

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
