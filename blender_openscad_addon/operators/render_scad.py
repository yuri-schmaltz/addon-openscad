from __future__ import annotations

import bpy


class OPENSCAD_OT_render(bpy.types.Operator):
  bl_idname = "openscad_bridge.render"
  bl_label = "Render (Apply Booleans)"
  bl_description = "Executa preview e aplica modificadores booleanos"

  def execute(self, context):
    preview_result = bpy.ops.openscad_bridge.preview()
    if "FINISHED" not in preview_result:
      return {"CANCELLED"}

    if not context.scene.openscad_bridge.apply_boolean_modifiers:
      self.report({"INFO"}, "Render concluido sem aplicar booleanos")
      return {"FINISHED"}

    coll = bpy.data.collections.get("OpenSCAD Preview")
    if not coll:
      self.report({"WARNING"}, "Colecao de preview nao encontrada")
      return {"CANCELLED"}

    active_view_layer = context.view_layer
    for obj in list(coll.objects):
      if obj.type != "MESH":
        continue

      for mod in list(obj.modifiers):
        if mod.type != "BOOLEAN":
          continue
        active_view_layer.objects.active = obj
        obj.select_set(True)
        try:
          bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception:
          pass
        obj.select_set(False)

    self.report({"INFO"}, "Render concluido com aplicacao de booleanos")
    return {"FINISHED"}


def register():
  bpy.utils.register_class(OPENSCAD_OT_render)


def unregister():
  bpy.utils.unregister_class(OPENSCAD_OT_render)
