from __future__ import annotations

import bpy

from ..core.parser import parse_scad
from ..core.evaluator import evaluate_program
from ..core.csg_builder import build_scene


class OPENSCAD_OT_import_file(bpy.types.Operator):
  bl_idname = "openscad_bridge.import_file"
  bl_label = "Import .scad"
  bl_description = "Carrega arquivo .scad para um Text datablock"

  filepath = bpy.props.StringProperty(subtype="FILE_PATH")

  def execute(self, context):
    scene_props = context.scene.openscad_bridge
    if not self.filepath:
      self.report({"ERROR"}, "Selecione um arquivo .scad")
      return {"CANCELLED"}

    try:
      with open(self.filepath, "r", encoding="utf-8") as f:
        source = f.read()
    except Exception as ex:
      self.report({"ERROR"}, f"Falha ao ler arquivo: {ex}")
      return {"CANCELLED"}

    name = bpy.path.display_name_from_filepath(self.filepath)
    text = bpy.data.texts.get(name)
    if text is None:
      text = bpy.data.texts.new(name)
    text.clear()
    text.write(source)

    scene_props.text_block_name = name
    scene_props.source_path = self.filepath

    if scene_props.live_preview:
      try:
        program = parse_scad(source)
        eval_items = evaluate_program(program)
        build_scene(context.scene, eval_items)
      except Exception as ex:
        self.report({"ERROR"}, f"Importado, mas preview falhou: {ex}")
        return {"CANCELLED"}

    self.report({"INFO"}, f"Arquivo importado: {self.filepath}")
    return {"FINISHED"}

  def invoke(self, context, event):
    context.window_manager.fileselect_add(self)
    return {"RUNNING_MODAL"}


def register():
  bpy.utils.register_class(OPENSCAD_OT_import_file)


def unregister():
  bpy.utils.unregister_class(OPENSCAD_OT_import_file)
