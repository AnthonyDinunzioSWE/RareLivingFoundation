from flask import Flask, jsonify, request
from dotenv import load_dotenv
from mongoengine import *
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)

CORS(app)

connect('rare_diseases', host=os.getenv('MONGO_URI'))

class DiseaseCard(Document):
    name = StringField(required=True)
    symptoms = ListField(StringField())
    causes = ListField(StringField())
    treatments = ListField(StringField())
    prevalance = StringField()
    resourses = ListField(URLField())


@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    query = request.args.get('q', '').lower()
    if query:
        cards = DiseaseCard.objects(name__icontains=query)
    else:
        cards = DiseaseCard.objects()
    return jsonify([card.to_mongo().to_dict() for card in cards])


if __name__ == '__main__':
    connect('rare_diseases', host=os.getenv('MONGO_URI'))
    app.run(debug=True)

