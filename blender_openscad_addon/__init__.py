bl_info = {
  "name": "OpenSCAD Bridge for Blender",
  "author": "Copilot",
  "version": (0, 1, 1),
  "blender": (5, 0, 0),
  "location": "View3D > Sidebar > OpenSCAD",
  "description": "Bridge OpenSCAD-like workflow inside Blender",
  "category": "Import-Export",
}

from . import preferences
from . import properties
from .operators import import_scad, preview_scad, render_scad, export_scad
from .ui import panels


def register():
  preferences.register()
  properties.register()
  import_scad.register()
  preview_scad.register()
  render_scad.register()
  export_scad.register()
  panels.register()


def unregister():
  panels.unregister()
  export_scad.unregister()
  render_scad.unregister()
  preview_scad.unregister()
  import_scad.unregister()
  properties.unregister()
  preferences.unregister()
