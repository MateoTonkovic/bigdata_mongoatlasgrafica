"""
Script para verificar la conexión a MongoDB Atlas antes de cargar datos
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError

MONGO_URI = "mongodb+srv://mateotonkovic03_db_user:cbX1qFogvtWp13ce@bases-datos.am7jdh7.mongodb.net/"

def test_connection():
    """Prueba la conexión a MongoDB Atlas"""
    print("=" * 60)
    print("🔍 VERIFICACIÓN DE CONEXIÓN A MONGODB ATLAS")
    print("=" * 60)
    
    try:
        print("\n1. Intentando conectar a MongoDB Atlas...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Forzar una operación para verificar la conexión
        client.admin.command('ping')
        print("   ✅ Conexión exitosa!")
        
        print("\n2. Verificando información del servidor...")
        server_info = client.server_info()
        print(f"   ✅ Versión de MongoDB: {server_info.get('version', 'N/A')}")
        
        print("\n3. Listando bases de datos disponibles...")
        databases = client.list_database_names()
        print(f"   ✅ Bases de datos encontradas: {len(databases)}")
        for db in databases:
            print(f"      - {db}")
        
        print("\n4. Verificando base de datos 'movies_db'...")
        db = client['movies_db']
        collections = db.list_collection_names()
        if collections:
            print(f"   ✅ Colecciones encontradas: {collections}")
            
            # Si existe la colección ratings, mostrar estadísticas
            if 'ratings' in collections:
                count = db['ratings'].count_documents({})
                print(f"   ℹ️  Documentos en 'ratings': {count:,}")
                
                if count > 0:
                    print("\n5. Muestra de datos:")
                    sample = db['ratings'].find_one()
                    print(f"      {sample}")
        else:
            print("   ℹ️  La base de datos está vacía (ejecutar load_data.py)")
        
        client.close()
        
        print("\n" + "=" * 60)
        print("✅ VERIFICACIÓN COMPLETADA - TODO OK")
        print("=" * 60)
        print("\n💡 Siguiente paso: python load_data.py")
        
        return True
        
    except ConnectionFailure:
        print("\n❌ ERROR: No se pudo conectar a MongoDB Atlas")
        print("   Verifica:")
        print("   - Tu conexión a Internet")
        print("   - El connection string")
        print("   - Las credenciales de acceso")
        return False
        
    except ConfigurationError as e:
        print(f"\n❌ ERROR DE CONFIGURACIÓN: {e}")
        print("   Verifica el formato del connection string")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        return False

if __name__ == "__main__":
    test_connection()

