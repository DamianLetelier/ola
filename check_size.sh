#!/bin/bash
# Script para analizar el tamaño de archivos y carpetas

echo "=== ANÁLISIS DE TAMAÑO DEL PROYECTO ==="
echo ""

echo "Tamaño total del proyecto:"
du -sh . --exclude=.git 2>/dev/null || echo "No se pudo calcular"

echo ""
echo "Tamaño de carpetas principales:"
du -sh */ 2>/dev/null | sort -hr | head -10

echo ""
echo "Archivos más grandes:"
find . -type f -size +1M -exec ls -lh {} \; 2>/dev/null | sort -k5 -hr | head -10

echo ""
echo "Archivos por tipo (top 10):"
echo "Archivos .py:"
find . -name "*.py" | wc -l
echo "Archivos .html:"
find . -name "*.html" | wc -l
echo "Archivos .css:"
find . -name "*.css" | wc -l
echo "Archivos .js:"
find . -name "*.js" | wc -l
echo "Archivos .png:"
find . -name "*.png" | wc -l
echo "Archivos .jpg:"
find . -name "*.jpg" | wc -l
echo "Archivos .gif:"
find . -name "*.gif" | wc -l
echo "Archivos .mp4:"
find . -name "*.mp4" | wc -l
echo "Archivos .pptx:"
find . -name "*.pptx" | wc -l
echo "Archivos .docx:"
find . -name "*.docx" | wc -l

echo ""
echo "Carpetas con más archivos:"
find . -type d | while read dir; do
    count=$(find "$dir" -maxdepth 1 -type f | wc -l)
    if [ $count -gt 5 ]; then
        echo "$dir: $count archivos"
    fi
done | sort -k2 -nr | head -10 