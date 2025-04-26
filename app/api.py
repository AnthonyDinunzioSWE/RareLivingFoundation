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
    # Convert ObjectId to string for JSON serialization
    result = []
    for card in cards:
        card_dict = card.to_mongo().to_dict()
        card_dict['id'] = str(card_dict.pop('_id'))  # Convert _id to string and rename to id
        result.append(card_dict)
    return jsonify(result)


@app.route('/api/seed_data', methods=['GET'])
def seed_data():
    try:
        data = [
                    {
                        "name": "Diabetes",
                        "symptoms": ["Frequent urination", "Increased thirst", "Unexplained weight loss"],
                        "causes": ["Insulin resistance", "Genetic factors", "Obesity"],
                        "treatments": ["Insulin therapy", "Diet management", "Exercise"],
                        "prevalance": "Common",
                        "resourses": ["https://www.cdc.gov/diabetes", "https://www.diabetes.org"]
                    },
                    {
                        "name": "Hypertension",
                        "symptoms": ["Headache", "Shortness of breath", "Nosebleeds"],
                        "causes": ["Genetic factors", "High salt diet", "Stress"],
                        "treatments": ["Lifestyle changes", "Blood pressure medications"],
                        "prevalance": "Very common",
                        "resourses": ["https://www.heart.org/en/health-topics/high-blood-pressure"]
                    },
                    {
                        "name": "Asthma",
                        "symptoms": ["Wheezing", "Shortness of breath", "Chest tightness"],
                        "causes": ["Allergens", "Air pollution", "Genetic predisposition"],
                        "treatments": ["Inhalers", "Corticosteroids", "Avoiding triggers"],
                        "prevalance": "Common",
                        "resourses": ["https://www.cdc.gov/asthma"]
                    },
                    {
                        "name": "Alzheimer's Disease",
                        "symptoms": ["Memory loss", "Confusion", "Difficulty completing familiar tasks"],
                        "causes": ["Age", "Genetics", "Brain plaque buildup"],
                        "treatments": ["Medication", "Cognitive therapy"],
                        "prevalance": "Common in elderly",
                        "resourses": ["https://www.alz.org"]
                    },
                    {
                        "name": "Parkinson's Disease",
                        "symptoms": ["Tremors", "Slowed movement", "Stiff muscles"],
                        "causes": ["Genetics", "Environmental factors"],
                        "treatments": ["Levodopa", "Physical therapy"],
                        "prevalance": "Less common",
                        "resourses": ["https://www.parkinson.org"]
                    },
                    {
                        "name": "Tuberculosis",
                        "symptoms": ["Coughing blood", "Chest pain", "Fatigue"],
                        "causes": ["Mycobacterium tuberculosis"],
                        "treatments": ["Antibiotics for 6–9 months"],
                        "prevalance": "Moderately common worldwide",
                        "resourses": ["https://www.cdc.gov/tb"]
                    },
                    {
                        "name": "COVID-19",
                        "symptoms": ["Fever", "Cough", "Loss of taste or smell"],
                        "causes": ["SARS-CoV-2 virus"],
                        "treatments": ["Antivirals", "Supportive care", "Vaccination"],
                        "prevalance": "Widespread pandemic",
                        "resourses": ["https://www.who.int/emergencies/diseases/novel-coronavirus-2019"]
                    },
                    {
                        "name": "Influenza",
                        "symptoms": ["Fever", "Chills", "Body aches"],
                        "causes": ["Influenza virus"],
                        "treatments": ["Rest", "Antivirals", "Fluids"],
                        "prevalance": "Seasonal outbreaks",
                        "resourses": ["https://www.cdc.gov/flu"]
                    },
                    {
                        "name": "HIV/AIDS",
                        "symptoms": ["Fatigue", "Weight loss", "Frequent infections"],
                        "causes": ["HIV virus"],
                        "treatments": ["Antiretroviral therapy (ART)"],
                        "prevalance": "Global issue",
                        "resourses": ["https://www.hiv.gov"]
                    },
                    {
                        "name": "Chickenpox",
                        "symptoms": ["Itchy rash", "Fever", "Fatigue"],
                        "causes": ["Varicella-zoster virus"],
                        "treatments": ["Antihistamines", "Antivirals", "Rest"],
                        "prevalance": "Rare in vaccinated populations",
                        "resourses": ["https://www.cdc.gov/chickenpox"]
                    },
                    {
                        "name": "Eczema",
                        "symptoms": ["Dry skin", "Itching", "Red patches"],
                        "causes": ["Genetics", "Immune system overreaction", "Irritants"],
                        "treatments": ["Moisturizers", "Topical steroids"],
                        "prevalance": "Very common",
                        "resourses": ["https://nationaleczema.org"]
                    },
                    {
                        "name": "Lupus",
                        "symptoms": ["Joint pain", "Fatigue", "Butterfly rash"],
                        "causes": ["Autoimmune disorder"],
                        "treatments": ["Immunosuppressants", "Anti-inflammatories"],
                        "prevalance": "Relatively rare",
                        "resourses": ["https://www.lupus.org"]
                    },
                    {
                        "name": "Anemia",
                        "symptoms": ["Fatigue", "Pale skin", "Shortness of breath"],
                        "causes": ["Iron deficiency", "Vitamin B12 deficiency"],
                        "treatments": ["Iron supplements", "Dietary changes"],
                        "prevalance": "Very common",
                        "resourses": ["https://www.mayoclinic.org/diseases-conditions/anemia"]
                    },
                    {
                        "name": "Migraine",
                        "symptoms": ["Throbbing headache", "Nausea", "Sensitivity to light"],
                        "causes": ["Genetics", "Hormonal changes", "Stress"],
                        "treatments": ["Pain relievers", "Preventive medications"],
                        "prevalance": "Common",
                        "resourses": ["https://www.migrainetrust.org"]
                    },
                    {
                        "name": "Celiac Disease",
                        "symptoms": ["Abdominal pain", "Bloating", "Diarrhea"],
                        "causes": ["Autoimmune response to gluten"],
                        "treatments": ["Gluten-free diet"],
                        "prevalance": "Fairly common",
                        "resourses": ["https://celiac.org"]
                    }
                ]

        for item in data:
            DiseaseCard(
                name=item['name'],
                symptoms=item['symptoms'],
                causes=item['causes'],
                treatments=item['treatments'],
            ).save()
        return jsonify({'message': 'Data seeded successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error seeding data', 'error': str(e)}), 500



if __name__ == '__main__':
    connect('rare_diseases', host=os.getenv('MONGO_URI'))
    app.run(debug=True)

