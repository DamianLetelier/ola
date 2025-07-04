#!/usr/bin/env python3
"""
Script para instalar dependencias ML dinámicamente en runtime.
Se ejecuta solo cuando se necesitan funcionalidades de ML.
"""

import subprocess
import sys
import os

def install_ml_dependencies():
    """Instala las dependencias ML desde requirements-ml.txt"""
    try:
        print("🔧 Instalando dependencias ML...")
        
        # Verificar si requirements-ml.txt existe
        if not os.path.exists('requirements-ml.txt'):
            print("❌ requirements-ml.txt no encontrado")
            return False
            
        # Instalar dependencias
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements-ml.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencias ML instaladas correctamente")
            return True
        else:
            print(f"❌ Error instalando dependencias ML: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_ml_dependencies():
    """Verifica si las dependencias ML están instaladas"""
    try:
        import torch
        import stanza
        import yara
        print("✅ Todas las dependencias ML están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencias ML faltantes: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_ml_dependencies()
    else:
        install_ml_dependencies() 