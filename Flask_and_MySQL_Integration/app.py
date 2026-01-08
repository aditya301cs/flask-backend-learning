from flask import Flask, jsonify
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Aditya@12345',
        database='users',  # database name
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    connection = get_db_connection()
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM flaskapp")  
            results = cur.fetchall()
    finally:
        connection.close()

    return jsonify(results)   

if __name__ == '__main__':
    app.run(debug=True)
