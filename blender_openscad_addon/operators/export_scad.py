from __future__ import annotations

import bpy

from ..core.serializer import serialize_object_to_scad


class OPENSCAD_OT_export_selected(bpy.types.Operator):
  bl_idname = "openscad_bridge.export_selected"
  bl_label = "Export Selected to .scad"
  bl_description = "Exporta o objeto selecionado para script OpenSCAD"

  filepath = bpy.props.StringProperty(subtype="FILE_PATH")

  def execute(self, context):
    obj = context.active_object
    if obj is None:
      self.report({"ERROR"}, "Nenhum objeto ativo")
      return {"CANCELLED"}

    scad = serialize_object_to_scad(obj)

    if not self.filepath:
      self.report({"ERROR"}, "Selecione um caminho de saida")
      return {"CANCELLED"}

    if not self.filepath.lower().endswith(".scad"):
      self.filepath += ".scad"

    try:
      with open(self.filepath, "w", encoding="utf-8") as f:
        f.write(scad)
    except Exception as ex:
      self.report({"ERROR"}, f"Falha ao salvar: {ex}")
      return {"CANCELLED"}

    self.report({"INFO"}, f"Exportado: {self.filepath}")
    return {"FINISHED"}

  def invoke(self, context, event):
    self.filepath = bpy.path.ensure_ext(context.active_object.name, ".scad")
    context.window_manager.fileselect_add(self)
    return {"RUNNING_MODAL"}


def register():
  bpy.utils.register_class(OPENSCAD_OT_export_selected)


def unregister():
  bpy.utils.unregister_class(OPENSCAD_OT_export_selected)
