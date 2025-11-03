#!/bin/bash

# Script de inicio rápido para el proyecto MongoDB Dashboard
# Ejecutar con: bash start.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🎬 Dashboard de Películas - MongoDB Atlas               ║"
echo "║   Setup y Ejecución Automática                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_step() {
    echo -e "${BLUE}➜${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Paso 1: Verificar Python
print_step "Verificando instalación de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python 3 no está instalado"
    exit 1
fi

# Paso 2: Instalar dependencias
print_step "Instalando dependencias..."
if pip3 install -r requirements.txt > /dev/null 2>&1; then
    print_success "Dependencias instaladas correctamente"
else
    print_error "Error al instalar dependencias"
    echo "Ejecuta manualmente: pip3 install -r requirements.txt"
    exit 1
fi

# Paso 3: Verificar conexión (opcional)
echo ""
read -p "¿Deseas verificar la conexión a MongoDB? (s/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    print_step "Verificando conexión a MongoDB Atlas..."
    python3 test_connection.py
    echo ""
    read -p "¿La conexión fue exitosa? ¿Continuar? (s/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_error "Verifica tu conexión y credenciales"
        exit 1
    fi
fi

# Paso 4: Cargar datos
echo ""
print_step "¿Cuántos registros deseas cargar?"
echo "  1) 50,000 registros (rápido - ~1 min)"
echo "  2) 100,000 registros (recomendado - ~2-3 min)"
echo "  3) 200,000 registros (~5 min)"
echo "  4) Todos (~1.6M registros - ⚠️ verificar espacio)"
echo "  5) Saltar carga (ya tengo datos)"
read -p "Selecciona una opción (1-5): " -n 1 -r LOAD_OPTION
echo ""

case $LOAD_OPTION in
    1)
        print_step "Cargando 50,000 registros..."
        python3 load_data.py 50000
        ;;
    2)
        print_step "Cargando 100,000 registros..."
        python3 load_data.py 100000
        ;;
    3)
        print_step "Cargando 200,000 registros..."
        python3 load_data.py 200000
        ;;
    4)
        print_warning "Cargando TODOS los registros (puede tomar 10+ minutos)..."
        python3 load_data.py all
        ;;
    5)
        print_warning "Saltando carga de datos..."
        ;;
    *)
        print_error "Opción inválida"
        exit 1
        ;;
esac

# Paso 5: Iniciar aplicación
echo ""
print_success "¡Setup completado!"
echo ""
print_step "Iniciando aplicación Flask..."
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Dashboard disponible en: http://localhost:5000           ║"
echo "║                                                            ║"
echo "║  Presiona Ctrl+C para detener el servidor                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

python3 app.py

