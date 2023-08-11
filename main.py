import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from flask import Flask, render_template, jsonify, json, request, url_for

import mysql.connector

app = Flask(__name__, static_url_path='/static')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pertanian'
}
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/api/data', methods=['GET'])
def getData():
    try:
        data = request.json
        nm_komoditas = request.get('nm_komoditas')
        nm_pasar = request.get('nm_pasar')
        tgl_awal = request.get('tgl_awal')
        tgl_akhir = request.get('tgl_akhir')

        query = "SELECT tanggal, harga_current FROM pertanian.daftar_harga WHERE nm_komoditas = %s AND nm_pasar = %s AND tanggal BETWEEN %s AND %s"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        return jsonify(data)
    except mysql.connector.Error as db_error:
        return jsonify({'error': f"Database Error: {db_error}"})
    except Exception as api_error:
        return jsonify({'error': f"API Error: {api_error}"})

@app.route('/plot')
def plot():
    return

if __name__ == '__main__':
    app.run(debug=True)