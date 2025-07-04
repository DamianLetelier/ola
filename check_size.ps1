# Script para analizar el tamaño de archivos y carpetas (Windows PowerShell)

Write-Host "=== ANÁLISIS DE TAMAÑO DEL PROYECTO ===" -ForegroundColor Green
Write-Host ""

# Tamaño total del proyecto
Write-Host "Tamaño total del proyecto:" -ForegroundColor Yellow
try {
    $totalSize = (Get-ChildItem -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $totalSizeMB = [math]::Round($totalSize / 1MB, 2)
    Write-Host "$totalSizeMB MB" -ForegroundColor Green
} catch {
    Write-Host "No se pudo calcular" -ForegroundColor Red
}

Write-Host ""
Write-Host "Tamaño de carpetas principales:" -ForegroundColor Yellow
Get-ChildItem -Directory | ForEach-Object {
    try {
        $folderSize = (Get-ChildItem -Recurse -File $_.FullName | Measure-Object -Property Length -Sum).Sum
        $folderSizeMB = [math]::Round($folderSize / 1MB, 2)
        Write-Host "$($_.Name): $folderSizeMB MB" -ForegroundColor White
    } catch {
        Write-Host "$($_.Name): Error al calcular" -ForegroundColor Red
    }
} | Sort-Object { [double]($_ -split ': ')[1] -replace ' MB', '' } -Descending | Select-Object -First 10

Write-Host ""
Write-Host "Archivos más grandes:" -ForegroundColor Yellow
Get-ChildItem -Recurse -File | Where-Object { $_.Length -gt 1MB } | Sort-Object Length -Descending | Select-Object -First 10 | ForEach-Object {
    $sizeMB = [math]::Round($_.Length / 1MB, 2)
    Write-Host "$($_.Name): $sizeMB MB" -ForegroundColor White
}

Write-Host ""
Write-Host "Archivos por tipo:" -ForegroundColor Yellow
$extensions = @("*.py", "*.html", "*.css", "*.js", "*.png", "*.jpg", "*.gif", "*.mp4", "*.pptx", "*.docx")
foreach ($ext in $extensions) {
    $count = (Get-ChildItem -Recurse -Name $ext -ErrorAction SilentlyContinue).Count
    Write-Host "Archivos $ext`: $count" -ForegroundColor White
}

Write-Host ""
Write-Host "Carpetas con más archivos:" -ForegroundColor Yellow
Get-ChildItem -Directory | ForEach-Object {
    $fileCount = (Get-ChildItem -File $_.FullName -Recurse -ErrorAction SilentlyContinue).Count
    if ($fileCount -gt 5) {
        Write-Host "$($_.Name): $fileCount archivos" -ForegroundColor White
    }
} | Sort-Object { [int]($_ -split ': ')[1] -replace ' archivos', '' } -Descending | Select-Object -First 10 