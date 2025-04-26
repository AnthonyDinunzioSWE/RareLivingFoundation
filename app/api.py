from flask import Flask, jsonify, request
from mongoengine import *
from flask_cors import CORS


connect('rare_diseases', host='mongodb+srv://Admin:@databasecluster.v3bvhqc.mongodb.net/?retryWrites=true&w=majority&appName=DatabaseCluster')

app = Flask(__name__)
CORS(app)

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
    return jsonify(cards)


if __name__ == '__main__':
    app.run(debug=True)

