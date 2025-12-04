"""
Script para cambiar todas las importaciones de 'db' a 'database'
"""
import os
import re


def fix_imports(directory="."):
    """Cambia 'from database import' por 'from database import' en todos los archivos .py"""

    archivos_modificados = []

    for root, dirs, files in os.walk(directory):
        # Ignorar carpetas
        dirs[:] = [d for d in dirs if d not in ['.venv', '__pycache__', '.git', 'node_modules']]

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Buscar y reemplazar
                    new_content = content.replace('from database import', 'from database import')

                    if new_content != content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        archivos_modificados.append(filepath)
                        print(f"✅ Modificado: {filepath}")

                except Exception as e:
                    print(f"❌ Error en {filepath}: {e}")

    print(f"\n{'=' * 60}")
    print(f"✅ Importaciones actualizadas en {len(archivos_modificados)} archivos")
    print(f"{'=' * 60}")

    if archivos_modificados:
        print("\nArchivos modificados:")
        for arch in archivos_modificados:
            print(f"  - {arch}")


if __name__ == "__main__":
    print("🔧 Actualizando importaciones de 'db' a 'database'...\n")
    fix_imports()