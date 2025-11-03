"""
Aplicación Flask simplificada para mostrar MongoDB Charts embebidos
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal con MongoDB Charts embebidos"""
    return render_template('index_charts.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

