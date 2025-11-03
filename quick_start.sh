#!/bin/bash

# Script de inicio rápido con entorno virtual
# Ejecutar con: bash quick_start.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🎬 Dashboard de Películas - MongoDB Atlas               ║"
echo "║   Inicio Rápido con Entorno Virtual                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    print_warning "No se encontró el entorno virtual"
    print_step "Creando entorno virtual..."
    bash setup_venv.sh
    if [ $? -ne 0 ]; then
        print_error "Error al crear el entorno virtual"
        exit 1
    fi
fi

# Activar entorno virtual
print_step "Activando entorno virtual..."
source venv/bin/activate
print_success "Entorno virtual activado"

# Verificar conexión (opcional)
echo ""
print_step "¿Deseas verificar la conexión a MongoDB? (s/n)"
read -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    print_step "Verificando conexión a MongoDB Atlas..."
    python test_connection.py
    echo ""
    print_step "¿La conexión fue exitosa? ¿Continuar? (s/n)"
    read -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_error "Verifica tu conexión y credenciales"
        deactivate
        exit 1
    fi
fi

# Cargar datos
echo ""
print_step "¿Cuántos registros deseas cargar?"
echo "  1) 50,000 registros (rápido - ~1 min)"
echo "  2) 100,000 registros (recomendado - ~2-3 min)"
echo "  3) 200,000 registros (~5 min)"
echo "  4) Todos (~1.6M registros - ⚠️ verificar espacio)"
echo "  5) Saltar carga (ya tengo datos)"
read -p "Selecciona una opción (1-5): " LOAD_OPTION
echo ""

case $LOAD_OPTION in
    1)
        print_step "Cargando 50,000 registros..."
        python load_data.py 50000
        ;;
    2)
        print_step "Cargando 100,000 registros..."
        python load_data.py 100000
        ;;
    3)
        print_step "Cargando 200,000 registros..."
        python load_data.py 200000
        ;;
    4)
        print_warning "Cargando TODOS los registros (puede tomar 10+ minutos)..."
        python load_data.py all
        ;;
    5)
        print_warning "Saltando carga de datos..."
        ;;
    *)
        print_error "Opción inválida"
        deactivate
        exit 1
        ;;
esac

# Iniciar aplicación
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

python app.py

# Desactivar entorno virtual al salir
deactivate

