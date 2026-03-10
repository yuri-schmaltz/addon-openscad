from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

import bpy


def _write_ascii_stl(path: Path) -> None:
  stl = """solid tri
facet normal 0 0 1
 outer loop
  vertex 0 0 0
  vertex 1 0 0
  vertex 0 1 0
 endloop
endfacet
endsolid tri
"""
  path.write_text(stl, encoding="utf-8")


def _collect_objects(coll_name: str):
  coll = bpy.data.collections.get(coll_name)
  if coll is None:
    return []
  return list(coll.objects)


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--repo-root", required=True)
  parser.add_argument("--report-path", required=True)
  args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else [])

  repo_root = Path(args.repo_root).resolve()
  report_path = Path(args.report_path).resolve()

  if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

  import blender_openscad_addon as addon
  from blender_openscad_addon.core.parser import parse_scad
  from blender_openscad_addon.core.evaluator import evaluate_program
  from blender_openscad_addon.core.csg_builder import build_scene

  addon.register()

  with tempfile.TemporaryDirectory() as td:
    td_path = Path(td)
    stl_path = td_path / "tiny.stl"
    _write_ascii_stl(stl_path)
    stl_escaped = str(stl_path).replace("\\", "\\\\")

    source = "\n".join(
      [
        "$fn=24;",
        "module w(){ children(); }",
        "w(){",
        "  color([1,0,0,1]) cube([2,2,2]);",
        "  #sphere(1);",
        "  linear_extrude(height=2) polygon(points=[[0,0],[2,0],[1,1]]);",
        "  rotate_extrude(angle=180) polygon(points=[[2,0],[3,0],[2.5,1]]);",
        "  mirror([1,0,0]) square([2,2], center=true);",
        "  resize([2,3,4], auto=[true,true,true]) multmatrix([[1,0,0,1],[0,1,0,2],[0,0,1,3]]) cylinder(h=2,r=0.3);",
        "  text(\"OK\", size=1.2);",
        f'  import("{stl_escaped}");',
        "}",
      ]
    )

    program = parse_scad(source)
    eval_items = evaluate_program(program, source_path=str(td_path / "scene.scad"))
    created = build_scene(bpy.context.scene, eval_items)

    text_name = "headless_test"
    txt = bpy.data.texts.new(text_name)
    txt.write(source)
    props = bpy.context.scene.openscad_bridge
    props.text_block_name = text_name
    props.source_path = str(td_path / "scene.scad")
    preview_result = bpy.ops.openscad_bridge.preview()
    render_result = bpy.ops.openscad_bridge.render()

    objs = _collect_objects("OpenSCAD Preview")
    types = [o.type for o in objs]
    names = [o.name for o in objs]

    report = {
      "created_count_direct": len(created),
      "preview_collection_count": len(objs),
      "mesh_count": sum(1 for t in types if t == "MESH"),
      "curve_count": sum(1 for t in types if t == "CURVE"),
      "object_names": names,
      "preview_result": list(preview_result),
      "render_result": list(render_result),
      "success": len(objs) > 0 and ("FINISHED" in preview_result),
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

  addon.unregister()
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
