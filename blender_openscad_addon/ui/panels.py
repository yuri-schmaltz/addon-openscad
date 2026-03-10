from __future__ import annotations

import bpy


class OPENSCAD_PT_bridge_panel(bpy.types.Panel):
  bl_label = "OpenSCAD Bridge"
  bl_idname = "OPENSCAD_PT_bridge_panel"
  bl_space_type = "VIEW_3D"
  bl_region_type = "UI"
  bl_category = "OpenSCAD"

  def draw(self, context):
    layout = self.layout
    props = context.scene.openscad_bridge

    col = layout.column(align=True)
    col.prop(props, "text_block_name")
    col.prop(props, "source_path")

    col = layout.column(align=True)
    col.prop(props, "live_preview")
    col.prop(props, "apply_boolean_modifiers")
    col.prop(props, "fallback_segments")

    row = layout.row(align=True)
    row.operator("openscad_bridge.import_file", text="Import SCAD")
    row.operator("openscad_bridge.export_selected", text="Export SCAD")

    row = layout.row(align=True)
    row.operator("openscad_bridge.preview", text="Preview")
    row.operator("openscad_bridge.render", text="Render")


class OPENSCAD_PT_bridge_text_editor_panel(bpy.types.Panel):
  bl_label = "OpenSCAD Bridge"
  bl_idname = "OPENSCAD_PT_bridge_text_editor_panel"
  bl_space_type = "TEXT_EDITOR"
  bl_region_type = "UI"
  bl_category = "OpenSCAD"

  def draw(self, context):
    layout = self.layout
    props = context.scene.openscad_bridge

    if context.space_data.text:
      props.text_block_name = context.space_data.text.name

    layout.label(text="Text block atual para preview:")
    layout.prop(props, "text_block_name", text="")
    layout.operator("openscad_bridge.preview", text="Preview From Text")


def register():
  bpy.utils.register_class(OPENSCAD_PT_bridge_panel)
  bpy.utils.register_class(OPENSCAD_PT_bridge_text_editor_panel)


def unregister():
  bpy.utils.unregister_class(OPENSCAD_PT_bridge_text_editor_panel)
  bpy.utils.unregister_class(OPENSCAD_PT_bridge_panel)
