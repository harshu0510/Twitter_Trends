from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from main import main  # Importing the main script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    main()
    client = MongoClient("mongodb://localhost:27017/")
    db = client.twitter_trends
    collection = db.trends
    latest_record = collection.find().sort([('_id', -1)]).limit(1)[0]
    client.close()
    return jsonify(latest_record)

if __name__ == "__main__":
    app.run(debug=True)
