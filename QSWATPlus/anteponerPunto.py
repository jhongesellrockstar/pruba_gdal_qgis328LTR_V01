import os
import re

# Ruta base al plugin QSWATPlus
carpeta_plugin = 'C:/Users/jhonv/AppData/Roaming/QGIS/QGIS3/profiles/default/python/plugins/QSWATPlus'

# Nombres de módulos internos que se deben cambiar a importación relativa
modulos = [
    'QSWATUtils', 'DBUtils', 'parameters', 'TauDEMUtils',
    'QSWATTopology', 'polygonizeInC2', 'polygonizeInC', 'globals',
    'convertFromArc', 'selectsubs', 'selectlu', 'visualise', 'visualisedialog',
    'about', 'landscape', 'ui_qswat', 'ui_parameters', 'ui_visualise', 'delineation',
    'split', 'floodplain', 'exempt', 'elevationbands', 'exporttable', 'outlets',
    'graphdialog', 'gwflow', 'hrus', 'runTauDEM'
]

regex = re.compile(r'^(from|import)\s+(' + '|'.join(modulos) + r')\b', re.MULTILINE)

def procesar_archivo(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    nuevo_contenido = regex.sub(lambda m: m.group(1) + ' .' + m.group(2), contenido)

    if contenido != nuevo_contenido:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print(f"Modificado: {os.path.basename(filepath)}")

# Recorre todos los archivos .py en la carpeta del plugin
for root, _, files in os.walk(carpeta_plugin):
    for file in files:
        if file.endswith('.py'):
            procesar_archivo(os.path.join(root, file))
