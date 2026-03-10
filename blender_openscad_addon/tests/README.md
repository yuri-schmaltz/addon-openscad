# Tests

Este addon possui uma suite de testes unitarios e de integracao.

## 1. Smoke legado

- Arquivo: test_parser_eval.py
- Objetivo: validacao rapida do parser/evaluator em exemplos SCAD

Execucao:

python blender_openscad_addon/tests/test_parser_eval.py

## 2. Suite extensa de parser/evaluator

- Arquivo: test_extensive_parser_evaluator.py
- Cobre: tokenizer, operadores, funcoes builtin, include/use, children(), assert(), transform chain, text(), import(), extrude

Execucao:

python blender_openscad_addon/tests/test_extensive_parser_evaluator.py

## 3. Integracao end-to-end com Blender headless

- Arquivo: test_blender_headless_integration.py
- Cobre: register/unregister do addon, parse/evaluate/build_scene, operadores preview/render, colecao OpenSCAD Preview
- Executa Blender em background com --factory-startup

Caminho padrao do Blender:

C:\Blender\blender.exe

Opcionalmente configure variavel de ambiente BLENDER_EXE para outro caminho.

Execucao:

python blender_openscad_addon/tests/test_blender_headless_integration.py

## 4. Rodar tudo

python blender_openscad_addon/tests/test_parser_eval.py
python blender_openscad_addon/tests/test_extensive_parser_evaluator.py
python blender_openscad_addon/tests/test_blender_headless_integration.py
