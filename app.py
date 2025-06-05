from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/usda')
def index():
    return render_template('index.html')  # Serves single-page UI

@app.route('/usda/filter/<query>')
def filter_data(query):
    conn = sqlite3.connect('usda.db')
    cursor = conn.cursor()
    cursor.execute("SELECT fdcId, description, nutrients FROM foods WHERE description LIKE ? OR nutrients LIKE ?", (f'%{query}%', f'%{query}%'))
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run()