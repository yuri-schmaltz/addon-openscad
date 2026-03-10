from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestBlenderHeadlessIntegration(unittest.TestCase):
  def test_blender_background_end_to_end(self):
    blender_exe = Path(os.environ.get("BLENDER_EXE", r"C:\Blender\blender.exe"))
    if not blender_exe.exists():
      self.skipTest(f"Blender nao encontrado em: {blender_exe}")

    tests_dir = Path(__file__).resolve().parent
    repo_root = tests_dir.parents[1]
    runner = tests_dir / "blender_headless_runner.py"

    with tempfile.TemporaryDirectory() as td:
      report_path = Path(td) / "report.json"
      cmd = [
        str(blender_exe),
        "-b",
        "--factory-startup",
        "--python",
        str(runner),
        "--",
        "--repo-root",
        str(repo_root),
        "--report-path",
        str(report_path),
      ]
      proc = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
      if proc.returncode != 0:
        self.fail(
          "Blender runner falhou\n"
          f"returncode={proc.returncode}\n"
          f"stdout:\n{proc.stdout}\n"
          f"stderr:\n{proc.stderr}\n"
        )

      self.assertTrue(
        report_path.exists(),
        "Runner nao gerou report.json\n"
        f"stdout:\n{proc.stdout}\n"
        f"stderr:\n{proc.stderr}\n",
      )
      report = json.loads(report_path.read_text(encoding="utf-8"))

      self.assertTrue(report.get("success"), f"Report sinalizou falha: {report}")
      self.assertGreater(report.get("created_count_direct", 0), 0)
      self.assertGreater(report.get("preview_collection_count", 0), 0)
      self.assertIn("FINISHED", report.get("preview_result", []))


if __name__ == "__main__":
  unittest.main()
