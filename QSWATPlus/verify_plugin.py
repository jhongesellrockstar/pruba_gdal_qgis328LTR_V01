
import os
import importlib.util

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
ESSENTIAL_FILES = [
    '__init__.py',
    'QSWATPlusMain.py',
    'qswatdialog.py',
    'ui_qswat.py',
    'resources_rc.py',
    'resources.qrc'
]

def check_file_exists(filename):
    path = os.path.join(PLUGIN_DIR, filename)
    return os.path.isfile(path)

def check_importable(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        return False, f"Spec not found for {module_name}"
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, "OK"
    except Exception as e:
        return False, str(e)

print("🔍 Verificando archivos esenciales en:", PLUGIN_DIR)
for file in ESSENTIAL_FILES:
    exists = check_file_exists(file)
    status = "✅ Existe" if exists else "❌ NO existe"
    print(f"{file:20s} ... {status}")

print("🧪 Probando imports:")
for file in ['ui_qswat.py', 'resources_rc.py']:
    full_path = os.path.join(PLUGIN_DIR, file)
    if not os.path.isfile(full_path):
        print(f"{file:20s} ... ⛔ Archivo no encontrado")
        continue
    module_name = os.path.splitext(file)[0]
    ok, msg = check_importable(module_name, full_path)
    status = "✅ OK" if ok else f"❌ Error: {msg}"
    print(f"{module_name:20s} ... {status}")
