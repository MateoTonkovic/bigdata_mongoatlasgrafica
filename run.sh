echo "🎬 Iniciando Dashboard de Películas..."
echo ""

if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Entorno virtual activado"
else
    echo "⚠️  No se encontró entorno virtual. Ejecuta primero: bash setup_venv.sh"
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Dashboard disponible en: http://localhost:5000           ║"
echo "║  Presiona Ctrl+C para detener                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

python app.py

deactivate

