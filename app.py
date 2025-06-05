from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, text
from os import getenv
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

USER = getenv("user")
PASSWORD = getenv("password")
HOST = getenv("host")
DBNAME = getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL)

@app.route('/usda')
def index():
    return render_template('index.html')  # Serves single-page UI

@app.route('/usda/filter/<query>')
def filter_data(query):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT fdc_id, description, nutrients FROM foods WHERE description ILIKE :query OR nutrients ILIKE :query"),
                {"query": f"%{query}%"}
            )
            data = [{"fdcId": row[0], "description": row[1], "nutrients": row[2]} for row in result]
        return jsonify(data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run()