"""
Aplicación Flask para visualizar gráficas de análisis de películas
"""
from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Configuración de MongoDB
MONGO_URI = "mongodb+srv://mateotonkovic03_db_user:cbX1qFogvtWp13ce@bases-datos.am7jdh7.mongodb.net/"
DATABASE_NAME = "movies_db"
COLLECTION_NAME = "ratings"

def get_db_connection():
    """Obtiene conexión a MongoDB"""
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]

@app.route('/')
def index():
    """Página principal con visualizaciones"""
    return render_template('index.html')

@app.route('/api/rating-distribution')
def rating_distribution():
    """
    Distribuci\u00f3n de ratings por rangos
    An\u00e1lisis de negocio: Muestra c\u00f3mo se distribuyen las calificaciones
    """
    try:
        db = get_db_connection()
        collection = db[COLLECTION_NAME]
        
        pipeline = [
            {
                "$bucket": {
                    "groupBy": "$averageRating",
                    "boundaries": [0, 2, 4, 6, 8, 10],
                    "default": "Other",
                    "output": {
                        "count": {"$sum": 1},
                        "avgVotes": {"$avg": "$numVotes"}
                    }
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        results = list(collection.aggregate(pipeline))
        
        # Formatear para gráfica
        labels = []
        counts = []
        avg_votes = []
        
        for item in results:
            if isinstance(item['_id'], (int, float)):
                labels.append(f"{item['_id']}-{item['_id']+2}")
            else:
                labels.append(item['_id'])
            counts.append(item['count'])
            avg_votes.append(round(item['avgVotes'], 2))
        
        return jsonify({
            'labels': labels,
            'counts': counts,
            'avgVotes': avg_votes
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-rated-popular')
def top_rated_popular():
    """
    Top películas mejor calificadas con popularidad
    An\u00e1lisis de negocio: Identifica contenido de alta calidad con audiencia
    """
    try:
        db = get_db_connection()
        collection = db[COLLECTION_NAME]
        
        # Películas con al menos 10,000 votos y rating >= 7
        pipeline = [
            {
                "$match": {
                    "numVotes": {"$gte": 10000},
                    "averageRating": {"$gte": 7.0}
                }
            },
            {"$sort": {"averageRating": -1, "numVotes": -1}},
            {"$limit": 20},
            {
                "$project": {
                    "_id": 0,
                    "tconst": 1,
                    "averageRating": 1,
                    "numVotes": 1
                }
            }
        ]
        
        results = list(collection.aggregate(pipeline))
        
        return jsonify({
            'movies': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/votes-analysis')
def votes_analysis():
    """
    An\u00e1lisis de engagement por rango de votos
    An\u00e1lisis de negocio: Mide el engagement de la audiencia
    """
    try:
        db = get_db_connection()
        collection = db[COLLECTION_NAME]
        
        pipeline = [
            {
                "$bucket": {
                    "groupBy": "$numVotes",
                    "boundaries": [0, 100, 1000, 10000, 100000, 1000000, 10000000],
                    "default": "Over 10M",
                    "output": {
                        "count": {"$sum": 1},
                        "avgRating": {"$avg": "$averageRating"}
                    }
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        results = list(collection.aggregate(pipeline))
        
        labels = []
        counts = []
        ratings = []
        
        for item in results:
            if isinstance(item['_id'], (int, float)):
                if item['_id'] == 0:
                    labels.append("0-100")
                elif item['_id'] == 100:
                    labels.append("100-1K")
                elif item['_id'] == 1000:
                    labels.append("1K-10K")
                elif item['_id'] == 10000:
                    labels.append("10K-100K")
                elif item['_id'] == 100000:
                    labels.append("100K-1M")
                elif item['_id'] == 1000000:
                    labels.append("1M-10M")
            else:
                labels.append(item['_id'])
            
            counts.append(item['count'])
            ratings.append(round(item['avgRating'], 2))
        
        return jsonify({
            'labels': labels,
            'counts': counts,
            'avgRatings': ratings
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quality-metrics')
def quality_metrics():
    """
    Métricas generales de calidad del contenido
    An\u00e1lisis de negocio: KPIs de calidad de catálogo
    """
    try:
        db = get_db_connection()
        collection = db[COLLECTION_NAME]
        
        pipeline = [
            {
                "$facet": {
                    "general": [
                        {
                            "$group": {
                                "_id": None,
                                "totalMovies": {"$sum": 1},
                                "avgRating": {"$avg": "$averageRating"},
                                "avgVotes": {"$avg": "$numVotes"},
                                "totalVotes": {"$sum": "$numVotes"}
                            }
                        }
                    ],
                    "highQuality": [
                        {"$match": {"averageRating": {"$gte": 8.0}}},
                        {"$count": "count"}
                    ],
                    "popular": [
                        {"$match": {"numVotes": {"$gte": 10000}}},
                        {"$count": "count"}
                    ],
                    "lowRated": [
                        {"$match": {"averageRating": {"$lte": 4.0}}},
                        {"$count": "count"}
                    ]
                }
            }
        ]
        
        result = list(collection.aggregate(pipeline))[0]
        
        general = result['general'][0] if result['general'] else {}
        high_quality = result['highQuality'][0]['count'] if result['highQuality'] else 0
        popular = result['popular'][0]['count'] if result['popular'] else 0
        low_rated = result['lowRated'][0]['count'] if result['lowRated'] else 0
        
        return jsonify({
            'totalMovies': general.get('totalMovies', 0),
            'avgRating': round(general.get('avgRating', 0), 2),
            'avgVotes': round(general.get('avgVotes', 0), 2),
            'totalVotes': general.get('totalVotes', 0),
            'highQuality': high_quality,
            'popular': popular,
            'lowRated': low_rated
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Iniciando aplicación en http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)

