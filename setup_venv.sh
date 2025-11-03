#!/bin/bash

# Script para crear y configurar entorno virtual
# Ejecutar con: bash setup_venv.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🔧 Configuración de Entorno Virtual                     ║"
echo "║   MongoDB Dashboard - Python 3.13                         ║"
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

# Paso 1: Verificar Python
print_step "Verificando instalación de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python encontrado: $PYTHON_VERSION"
else
    print_error "Python 3 no está instalado"
    exit 1
fi

# Paso 2: Crear entorno virtual
print_step "Creando entorno virtual..."
if [ -d "venv" ]; then
    print_warning "El entorno virtual ya existe. ¿Deseas recrearlo? (s/n)"
    read -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Entorno virtual recreado"
    else
        print_success "Usando entorno virtual existente"
    fi
else
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Paso 3: Activar entorno virtual
print_step "Activando entorno virtual..."
source venv/bin/activate
print_success "Entorno virtual activado"

# Paso 4: Actualizar pip
print_step "Actualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip actualizado"

# Paso 5: Instalar dependencias
print_step "Instalando dependencias..."
if pip install -r requirements.txt > /dev/null 2>&1; then
    print_success "Dependencias instaladas correctamente"
else
    print_error "Error al instalar dependencias"
    print_warning "Intentando instalar manualmente..."
    pip install Flask pymongo dnspython
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETADO                                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
print_success "Entorno virtual configurado correctamente"
echo ""
echo "Para usar el proyecto:"
echo "  1. Activa el entorno virtual:"
echo "     ${GREEN}source venv/bin/activate${NC}"
echo ""
echo "  2. Ejecuta el proyecto:"
echo "     ${GREEN}bash run.sh${NC}"
echo ""
echo "  O ejecuta directamente:"
echo "     ${GREEN}bash quick_start.sh${NC}"
echo ""

