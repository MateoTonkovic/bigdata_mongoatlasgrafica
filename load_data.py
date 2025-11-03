"""
Script para cargar datos de title.ratings.tsv a MongoDB Atlas
"""
import csv
from pymongo import MongoClient, ASCENDING
from pymongo.errors import BulkWriteError
import sys

# Configuración de MongoDB
MONGO_URI = "mongodb+srv://mateotonkovic03_db_user:cbX1qFogvtWp13ce@bases-datos.am7jdh7.mongodb.net/"
DATABASE_NAME = "movies_db"
COLLECTION_NAME = "ratings"

def load_data_to_mongo(tsv_file, batch_size=1000, max_records=None):
    """
    Carga datos del TSV a MongoDB en lotes para optimizar memoria
    
    Args:
        tsv_file: Ruta al archivo TSV
        batch_size: Tamaño de lotes para inserción
        max_records: Máximo de registros a cargar (None = todos)
    """
    try:
        # Conectar a MongoDB
        print("Conectando a MongoDB Atlas...")
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # Limpiar colección existente (opcional)
        print(f"Limpiando colección '{COLLECTION_NAME}'...")
        collection.delete_many({})
        
        # Leer y cargar datos
        print(f"Cargando datos desde {tsv_file}...")
        batch = []
        total_inserted = 0
        
        with open(tsv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            
            for i, row in enumerate(reader):
                # Limitar registros si se especifica
                if max_records and i >= max_records:
                    break
                
                # Convertir tipos de datos
                try:
                    document = {
                        'tconst': row['tconst'],
                        'averageRating': float(row['averageRating']),
                        'numVotes': int(row['numVotes'])
                    }
                    batch.append(document)
                    
                    # Insertar lote cuando alcance el tamaño
                    if len(batch) >= batch_size:
                        try:
                            collection.insert_many(batch, ordered=False)
                            total_inserted += len(batch)
                            print(f"Insertados {total_inserted} registros...")
                            batch = []
                        except BulkWriteError as e:
                            print(f"Error en lote: {e.details}")
                            batch = []
                            
                except (ValueError, KeyError) as e:
                    print(f"Error procesando línea {i}: {e}")
                    continue
        
        # Insertar registros restantes
        if batch:
            try:
                collection.insert_many(batch, ordered=False)
                total_inserted += len(batch)
            except BulkWriteError as e:
                print(f"Error en último lote: {e.details}")
        
        print(f"\n✓ Carga completada: {total_inserted} registros insertados")
        
        # Crear índices para optimizar consultas
        print("Creando índices...")
        collection.create_index([("averageRating", ASCENDING)])
        collection.create_index([("numVotes", ASCENDING)])
        
        # Mostrar estadísticas
        print("\n--- Estadísticas ---")
        print(f"Total de documentos: {collection.count_documents({})}")
        
        # Estadísticas básicas
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avgRating": {"$avg": "$averageRating"},
                    "maxRating": {"$max": "$averageRating"},
                    "minRating": {"$min": "$averageRating"},
                    "totalVotes": {"$sum": "$numVotes"}
                }
            }
        ]
        stats = list(collection.aggregate(pipeline))
        if stats:
            print(f"Rating promedio: {stats[0]['avgRating']:.2f}")
            print(f"Rating máximo: {stats[0]['maxRating']:.2f}")
            print(f"Rating mínimo: {stats[0]['minRating']:.2f}")
            print(f"Total de votos: {stats[0]['totalVotes']:,}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Por defecto, carga solo los primeros 100,000 registros por espacio limitado
    # Para cargar todo, cambiar max_records=None
    max_records = 100000
    
    if len(sys.argv) > 1:
        max_records = int(sys.argv[1]) if sys.argv[1] != "all" else None
    
    print(f"Cargando {'todos los registros' if max_records is None else f'{max_records:,} registros'}...")
    
    success = load_data_to_mongo(
        'title.ratings.tsv',
        batch_size=40000,  # Aumentado de 1000 a 10000 para mayor velocidad
        max_records=max_records
    )
    
    if success:
        print("\n¡Datos cargados exitosamente!")
    else:
        print("\nError al cargar datos")
        sys.exit(1)

