import os
import pandas as pd
from flask import Flask, jsonify
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# إعدادات قاعدة البيانات (بناخدها من الـ Environment Variables في Docker Compose)
DB_URL = os.getenv('DATABASE_URL', 'postgresql://devops_user:devops_password@db:5432/energy_data')

def check_db_connection():
    try:
        connection = psycopg2.connect(DB_URL)
        connection.close()
        return "Connected to PostgreSQL ✅"
    except (Exception, Error) as e:
        return f"Database Connection Failed ❌: {e}"

@app.route('/')
def home():
    return {
        "message": "GreenEnergy API is Running!",
        "status": "Online",
        "database": check_db_connection()
    }

@app.route('/data')
def get_energy_data():
    try:
        # قراءة ملف الـ CSV اللي العميل بعته (باستخدام Pandas)
        df = pd.read_csv('data_sample.csv')
        
        # تحويل البيانات لـ JSON عشان العميل يشوفها
        data_json = df.to_dict(orient='records')
        return jsonify({
            "source": "data_sample.csv",
            "total_records": len(df),
            "data": data_json
        })
    except Exception as e:
        return jsonify({"error": f"Could not read CSV file: {e}"}), 500

if __name__ == '__main__':
    # بورت 5000 عشان يوافق الـ Docker Compose
    app.run(host='0.0.0.0', port=5000)
