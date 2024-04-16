from flask import Flask, render_template, request, jsonify
import os 

from src.load_index import load_index

index_var = load_index()

app = Flask(__name__, static_folder="statics") 

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        query_engine = index_var.as_query_engine()
        user_query = request.form["msg"]
        print(user_query)
        result = query_engine.query(user_query)
        return jsonify({"message":(result.response)})   # Use jsonify
    except Exception as e:
        print("Error in /get route:", e)
        return jsonify({"error": str(e)}), 500 

if __name__ == '__main__':
    app.run(debug=True) 
