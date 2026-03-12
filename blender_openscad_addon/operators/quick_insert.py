from __future__ import annotations

import bpy

class OPENSCAD_OT_quick_insert(bpy.types.Operator):
  bl_idname = "openscad_bridge.quick_insert"
  bl_label = "Quick Insert SCAD Script"
  bl_description = "Abre uma janela para digitar ou colar script OpenSCAD rapidamente"

  script_content: bpy.props.StringProperty(
    name="Script",
    description="Cole ou digite seu script OpenSCAD aqui",
    default="",
  )

  def execute(self, context):
    props = context.scene.openscad_bridge
    
    # Check if we have a valid text block, otherwise create one
    text_name = props.text_block_name
    text = bpy.data.texts.get(text_name) if text_name else None
    
    if not text:
      text = bpy.data.texts.new("OpenSCAD_Script.scad")
      props.text_block_name = text.name
      
    text.clear()
    text.write(self.script_content)
    
    # Try to preview immediately
    try:
      bpy.ops.openscad_bridge.preview('INVOKE_DEFAULT')
    except Exception:
      pass
      
    return {"FINISHED"}

  def invoke(self, context, event):
    props = context.scene.openscad_bridge
    text_name = props.text_block_name
    text = bpy.data.texts.get(text_name) if text_name else None
    
    if text:
      self.script_content = text.as_string()
    else:
      self.script_content = ""
      
    return context.window_manager.invoke_props_dialog(self, width=600)

  def draw(self, context):
    layout = self.layout
    layout.label(text="OpenSCAD Script:", icon='TEXT')
    
    # Create a column for the text box and expand its vertical scale
    # to behave like a textarea instead of a single-line string input.
    col = layout.column()
    col.scale_y = 15.0  # Make it 15 lines tall
    col.prop(self, "script_content", text="")


def register():
  bpy.utils.register_class(OPENSCAD_OT_quick_insert)


def unregister():
  bpy.utils.unregister_class(OPENSCAD_OT_quick_insert)
