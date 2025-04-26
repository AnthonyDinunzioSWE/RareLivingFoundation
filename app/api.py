from flask import Flask, jsonify, request
from dotenv import load_dotenv
from mongoengine import *
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)

CORS(app)

try:
    connect('rare_diseases', host=os.getenv('MONGO_URI'))
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed:", e)


class DiseaseCard(Document):
    name = StringField(required=True)
    symptoms = ListField(StringField())
    causes = ListField(StringField())
    treatments = ListField(StringField())
    prevalance = StringField()
    resourses = ListField(URLField())

class ProfessionalCenter(Document):
    name = StringField(required=True)
    location = StringField(required=True)
    google_maps_embed = URLField(required=True)
    diseases = ListField(StringField())
    contact_info = DictField()  # {'phone': '...', 'email': '...', 'website': '...'}
    hours_of_operation = StringField()  # Simple for now ("24/7", "9am-5pm Mon-Fri", etc.)



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


@app.route('/api/professional_centers', methods=['GET'])
def get_professional_centers():
    query = request.args.get('q', '').lower()
    if query:
        centers = ProfessionalCenter.objects.filter(
            __raw__={
                "$or": [
                    {"name": {"$regex": query, "$options": "i"}},
                    {"location": {"$regex": query, "$options": "i"}},
                    {"diseases": {"$elemMatch": {"$regex": query, "$options": "i"}}}
                ]
            }
        )
    else:
        centers = ProfessionalCenter.objects()
    
    result = []
    for center in centers:
        center_dict = center.to_mongo().to_dict()
        center_dict['id'] = str(center_dict.pop('_id'))
        result.append(center_dict)
    
    return jsonify(result)


@app.route('/api/seed_data', methods=['GET'])
def seed_data():
    try:
        # First, clear existing collections if you want a clean start (optional)
        DiseaseCard.objects.delete()
        ProfessionalCenter.objects.delete()

        disease_data = [
    {
        "name": "Stiff Person Syndrome",
        "symptoms": ["Muscle stiffness", "Severe muscle spasms", "Difficulty walking"],
        "causes": ["Autoimmune reaction", "Genetic factors", "Environmental triggers"],
        "treatments": ["Muscle relaxants", "Immunosuppressants", "Physical therapy"],
        "prevalance": "Very rare",
        "resourses": ["https://www.rarediseases.org"],
    },
    {
        "name": "Kuru",
        "symptoms": ["Loss of coordination", "Tremors", "Difficulty swallowing"],
        "causes": ["Prion infection", "Consumption of contaminated human brain tissue"],
        "treatments": ["No cure, supportive care"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.cdc.gov/prions/kuru"],
    },
    {
        "name": "Fibrodysplasia Ossificans Progressiva (FOP)",
        "symptoms": ["Progressive loss of mobility", "Bone formation in soft tissues", "Soreness in muscles and joints"],
        "causes": ["Genetic mutation", "Autosomal dominant inheritance"],
        "treatments": ["No cure, but symptom management with pain relievers and physical therapy"],
        "prevalance": "Very rare",
        "resourses": ["https://www.ifopa.org"],
    },
    {
        "name": "Alkaptonuria",
        "symptoms": ["Dark urine", "Arthritis", "Heart disease"],
        "causes": ["Deficiency of the enzyme homogentisate oxidase", "Genetic mutation"],
        "treatments": ["Symptom management", "Joint replacements", "Diet management"],
        "prevalance": "Very rare",
        "resourses": ["https://rarediseases.info.nih.gov"],
    },
    {
        "name": "Progeria (Hutchinson-Gilford Progeria Syndrome)",
        "symptoms": ["Accelerated aging", "Growth failure", "Joint stiffness"],
        "causes": ["Mutations in the LMNA gene"],
        "treatments": ["No cure, but supportive treatments"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.progeriaresearch.org"],
    },
    {
        "name": "Hyper IgM Syndrome",
        "symptoms": ["Recurrent infections", "Severe pneumonia", "Increased risk of autoimmune diseases"],
        "causes": ["Genetic mutations affecting immune function", "Deficiency of IgM antibodies"],
        "treatments": ["Antibiotics", "Immunoglobulin replacement therapy", "Stem cell transplant"],
        "prevalance": "Very rare",
        "resourses": ["https://www.rarediseases.org"],
    },
    {
        "name": "Ondine's Curse (Congenital Central Hypoventilation Syndrome)",
        "symptoms": ["Inability to sense low oxygen levels", "Sleep apnea", "Irregular breathing patterns"],
        "causes": ["Genetic mutation affecting oxygen regulation"],
        "treatments": ["Ventilator support during sleep", "Oxygen therapy"],
        "prevalance": "Very rare",
        "resourses": ["https://www.rarediseases.org"],
    },
    {
        "name": "Pachyonychia Congenita",
        "symptoms": ["Thickened nails", "Painful calluses", "Oral leukokeratosis"],
        "causes": ["Genetic mutations affecting keratin production"],
        "treatments": ["Pain management", "Skin care", "Orthopedic support"],
        "prevalance": "Very rare",
        "resourses": ["https://www.pachyonychia.org"],
    },
    {
        "name": "Cushing's Disease",
        "symptoms": ["Weight gain", "High blood pressure", "Thin skin"],
        "causes": ["Excess cortisol production", "Pituitary tumor"],
        "treatments": ["Surgery", "Radiation therapy", "Medications to block cortisol"],
        "prevalance": "Rare",
        "resourses": ["https://www.cushingshelp.org"],
    },
    {
        "name": "Ehlers-Danlos Syndrome (EDS)",
        "symptoms": ["Hyperflexible joints", "Skin that bruises easily", "Chronic pain"],
        "causes": ["Genetic mutations affecting collagen production"],
        "treatments": ["Pain management", "Physical therapy", "Surgical interventions for joint stabilization"],
        "prevalance": "Rare",
        "resourses": ["https://www.ehlers-danlos.com"],
    },
    {
        "name": "Harlequin Ichthyosis",
        "symptoms": ["Thick, hard skin", "Red, inflamed patches", "Cracked skin"],
        "causes": ["Deficiency in the gene responsible for skin production"],
        "treatments": ["Skin care", "Antibiotic therapy for infections", "Topical treatments"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.ichthyosis.org"],
    },
    {
        "name": "X-Linked Agammaglobulinemia",
        "symptoms": ["Recurrent infections", "Respiratory infections", "Delayed growth"],
        "causes": ["Genetic mutation affecting B cell production"],
        "treatments": ["Immunoglobulin therapy", "Antibiotics", "Bone marrow transplant"],
        "prevalance": "Very rare",
        "resourses": ["https://www.ninds.nih.gov"],
    },
    {
        "name": "Autoimmune Polyglandular Syndrome Type 1",
        "symptoms": ["Chronic diarrhea", "Weight loss", "Adrenal insufficiency"],
        "causes": ["Autoimmune destruction of multiple endocrine glands"],
        "treatments": ["Hormone replacement therapy", "Corticosteroids", "Immunosuppressants"],
        "prevalance": "Very rare",
        "resourses": ["https://www.rarediseases.org"],
    },
    {
        "name": "Hypereosinophilic Syndrome",
        "symptoms": ["Fatigue", "Shortness of breath", "Skin rashes"],
        "causes": ["Excess eosinophils in the blood", "Idiopathic or secondary causes"],
        "treatments": ["Corticosteroids", "Chemotherapy", "Immunosuppressive drugs"],
        "prevalance": "Very rare",
        "resourses": ["https://www.rareconnect.org"],
    },
    {
        "name": "Aicardi Syndrome",
        "symptoms": ["Seizures", "Cognitive delays", "Eye abnormalities"],
        "causes": ["X-linked genetic mutation affecting the brain"],
        "treatments": ["Anticonvulsants", "Physical therapy", "Supportive care"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.aicardisyndrome.org"],
    },
    {
        "name": "Menkes Disease",
        "symptoms": ["Weak muscle tone", "Seizures", "Cognitive delays"],
        "causes": ["Deficiency of copper transport protein"],
        "treatments": ["Copper supplementation", "Supportive care"],
        "prevalance": "Very rare",
        "resourses": ["https://www.menkes.org"],
    },
    {
        "name": "Wilson's Disease",
        "symptoms": ["Jaundice", "Liver damage", "Neurological symptoms"],
        "causes": ["Copper buildup due to defective copper metabolism"],
        "treatments": ["Copper chelation", "Liver transplant"],
        "prevalance": "Rare",
        "resourses": ["https://www.wilsonsdisease.org"],
    },
    {
        "name": "Huntington's Disease",
        "symptoms": ["Involuntary movements", "Cognitive decline", "Personality changes"],
        "causes": ["Genetic mutation in the HTT gene"],
        "treatments": ["Symptom management", "Physical therapy", "Supportive care"],
        "prevalance": "Rare",
        "resourses": ["https://www.hdsa.org"],
    },
    {
        "name": "Leber's Hereditary Optic Neuropathy",
        "symptoms": ["Sudden vision loss", "Color blindness", "Eye pain"],
        "causes": ["Mitochondrial mutations affecting optic nerve function"],
        "treatments": ["No cure, but genetic counseling and supportive care"],
        "prevalance": "Rare",
        "resourses": ["https://www.lhon.org"],
    },
    {
        "name": "Chronic Fatigue Syndrome (CFS)",
        "symptoms": ["Extreme fatigue", "Sleep disturbances", "Muscle pain"],
        "causes": ["Viral infections", "Immune system dysfunction", "Genetic predisposition"],
        "treatments": ["Symptom management", "Cognitive behavioral therapy", "Exercise therapy"],
        "prevalance": "Rare",
        "resourses": ["https://www.cdc.gov/cfs"],
    },
    {
        "name": "Sjögren's Syndrome",
        "symptoms": ["Dry mouth", "Dry eyes", "Fatigue"],
        "causes": ["Autoimmune attack on moisture-producing glands"],
        "treatments": ["Hydration", "Immunosuppressive drugs", "Symptom management"],
        "prevalance": "Rare",
        "resourses": ["https://www.sjogrens.org"],
    },
    {
        "name": "Neurofibromatosis Type 1",
        "symptoms": ["Café-au-lait spots", "Lumps under the skin", "Learning disabilities"],
        "causes": ["Genetic mutation in the NF1 gene"],
        "treatments": ["Surgical removal of tumors", "Symptom management"],
        "prevalance": "Rare",
        "resourses": ["https://www.nfnetwork.org"],
    },
    {
        "name": "Angelman Syndrome",
        "symptoms": ["Severe intellectual disability", "Speech impairment", "Seizures"],
        "causes": ["Deletion of UBE3A gene"],
        "treatments": ["Behavioral therapy", "Anticonvulsants", "Speech therapy"],
        "prevalance": "Very rare",
        "resourses": ["https://www.angelman.org"],
    }
]

        disease_data.extend([
    {
        "name": "Adenylosuccinate Lyase Deficiency",
        "symptoms": ["Developmental delay", "Severe speech impairment", "Movement disorders"],
        "causes": ["Deficiency of adenylosuccinate lyase enzyme", "Genetic mutation"],
        "treatments": ["Symptomatic treatment", "Speech therapy", "Physical therapy"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.rareconnect.org"],
    },
    {
        "name": "Churg-Strauss Syndrome",
        "symptoms": ["Asthma", "Eosinophilia", "Fatigue"],
        "causes": ["Autoimmune disease affecting blood vessels", "Allergic reactions"],
        "treatments": ["Corticosteroids", "Immunosuppressive drugs", "Biologics"],
        "prevalance": "Very rare",
        "resourses": ["https://www.rarediseases.org"],
    },
    {
        "name": "Focal Segmental Glomerulosclerosis",
        "symptoms": ["Edema", "Proteinuria", "High blood pressure"],
        "causes": ["Scarring of kidney tissue", "Genetic factors", "Unknown"],
        "treatments": ["Steroids", "Immunosuppressive drugs", "Dialysis"],
        "prevalance": "Rare",
        "resourses": ["https://www.kidney.org"],
    },
    {
        "name": "Angelman Syndrome",
        "symptoms": ["Severe intellectual disability", "Seizures", "Speech impairment"],
        "causes": ["Deletion of UBE3A gene"],
        "treatments": ["Behavioral therapy", "Speech therapy", "Seizure management"],
        "prevalance": "Very rare",
        "resourses": ["https://www.angelman.org"],
    },
    {
        "name": "Morgellons Disease",
        "symptoms": ["Itching", "Skin sores", "Crawling sensations on the skin"],
        "causes": ["Cause unknown, possibly related to infectious or environmental factors"],
        "treatments": ["Symptom management", "Antibiotics", "Psychological support"],
        "prevalance": "Rare",
        "resourses": ["https://www.morgellons.org"],
    },
    {
        "name": "Gorlin Syndrome (Nevoid Basal Cell Carcinoma Syndrome)",
        "symptoms": ["Basal cell carcinomas", "Jaw cysts", "Neurofibromas"],
        "causes": ["Mutations in the PTCH1 gene"],
        "treatments": ["Surgical removal of tumors", "Skin protection from UV exposure"],
        "prevalance": "Very rare",
        "resourses": ["https://www.gorlin.org"],
    },
    {
        "name": "Menkes Disease",
        "symptoms": ["Weak muscle tone", "Seizures", "Cognitive delays"],
        "causes": ["Copper transport gene mutation"],
        "treatments": ["Copper supplementation", "Supportive care"],
        "prevalance": "Very rare",
        "resourses": ["https://www.menkes.org"],
    },
    {
        "name": "DiGeorge Syndrome",
        "symptoms": ["Heart defects", "Cleft palate", "Immunodeficiency"],
        "causes": ["Deletion of a portion of chromosome 22"],
        "treatments": ["Surgical repair of heart defects", "Immunoglobulin therapy", "Speech therapy"],
        "prevalance": "Rare",
        "resourses": ["https://www.digeorgesyndrome.org"],
    },
    {
        "name": "Hypohidrotic Ectodermal Dysplasia",
        "symptoms": ["Hypohidrosis", "Absent or sparse hair", "Missing teeth"],
        "causes": ["Genetic mutations in ectodermal development"],
        "treatments": ["Symptom management", "Prosthetic dental implants", "Thermal regulation strategies"],
        "prevalance": "Very rare",
        "resourses": ["https://www.hedfoundation.org"],
    },
    {
        "name": "Zellweger Syndrome",
        "symptoms": ["Liver dysfunction", "Neurological impairment", "Developmental delays"],
        "causes": ["Peroxisome biogenesis disorder due to genetic mutations"],
        "treatments": ["No cure, symptom management", "Supportive care"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.rarediseases.org"],
    },
    {
        "name": "Hyper IgM Syndrome",
        "symptoms": ["Recurrent infections", "Respiratory issues", "Delayed growth"],
        "causes": ["Genetic mutation in immune system regulation"],
        "treatments": ["Immunoglobulin replacement", "Stem cell transplant", "Antibiotic therapy"],
        "prevalance": "Very rare",
        "resourses": ["https://www.rarediseases.org"],
    },
    {
        "name": "Osteogenesis Imperfecta",
        "symptoms": ["Fragile bones", "Frequent fractures", "Short stature"],
        "causes": ["Defective collagen production", "Genetic mutations"],
        "treatments": ["Bisphosphonates", "Physical therapy", "Bone surgery"],
        "prevalance": "Rare",
        "resourses": ["https://www.oif.org"],
    },
    {
        "name": "Rett Syndrome",
        "symptoms": ["Loss of purposeful hand movements", "Speech loss", "Severe developmental regression"],
        "causes": ["Mutation in the MECP2 gene"],
        "treatments": ["Symptom management", "Physical therapy", "Speech therapy"],
        "prevalance": "Very rare",
        "resourses": ["https://www.rettsyndrome.org"],
    },
    {
        "name": "Tay-Sachs Disease",
        "symptoms": ["Severe developmental regression", "Vision and hearing loss", "Seizures"],
        "causes": ["Deficiency in hexosaminidase A enzyme"],
        "treatments": ["No cure, supportive care"],
        "prevalance": "Rare",
        "resourses": ["https://www.taysachs.org"],
    },
    {
        "name": "Shwachman-Diamond Syndrome",
        "symptoms": ["Pancreatic insufficiency", "Bone marrow failure", "Growth retardation"],
        "causes": ["Mutation in the SBDS gene"],
        "treatments": ["Pancreatic enzyme replacement", "Blood transfusions", "Bone marrow transplant"],
        "prevalance": "Very rare",
        "resourses": ["https://www.shwachman-diamond.org"],
    },
    {
        "name": "Lysosomal Acid Lipase Deficiency",
        "symptoms": ["Fatty liver", "Abnormal cholesterol levels", "Growth failure"],
        "causes": ["Deficiency of the enzyme lysosomal acid lipase"],
        "treatments": ["Enzyme replacement therapy", "Liver transplant"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.rarediseases.org"],
    },
    {
        "name": "Neurofibromatosis Type 2",
        "symptoms": ["Hearing loss", "Tinnitus", "Balance problems"],
        "causes": ["Mutation in the NF2 gene"],
        "treatments": ["Surgical removal of tumors", "Hearing aids", "Physical therapy"],
        "prevalance": "Rare",
        "resourses": ["https://www.nf2is.org"],
    },
    {
        "name": "Tuberous Sclerosis Complex",
        "symptoms": ["Seizures", "Developmental delays", "Skin lesions"],
        "causes": ["Genetic mutations affecting tumor suppression genes"],
        "treatments": ["Anticonvulsants", "Surgical removal of tumors", "Symptom management"],
        "prevalance": "Rare",
        "resourses": ["https://www.tsalliance.org"],
    },
    {
        "name": "Bardet-Biedl Syndrome",
        "symptoms": ["Vision loss", "Obesity", "Polydactyly"],
        "causes": ["Genetic mutations affecting cilia function"],
        "treatments": ["Symptom management", "Weight control", "Vision aids"],
        "prevalance": "Very rare",
        "resourses": ["https://www.bardetbiedl.org"],
    },
    {
        "name": "Noonan Syndrome",
        "symptoms": ["Heart defects", "Short stature", "Learning difficulties"],
        "causes": ["Genetic mutations affecting RAS-MAPK signaling pathway"],
        "treatments": ["Surgical interventions", "Growth hormone therapy", "Cardiac care"],
        "prevalance": "Rare",
        "resourses": ["https://www.raisingnoonan.org"],
    },
    {
        "name": "Batten Disease",
        "symptoms": ["Seizures", "Vision loss", "Cognitive decline"],
        "causes": ["Genetic mutations affecting lysosomal function"],
        "treatments": ["No cure, but symptomatic care"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.bdsra.org"],
    },
    {
        "name": "Cystinosis",
        "symptoms": ["Kidney failure", "Corneal crystals", "Delayed growth"],
        "causes": ["Deficiency in cystinosin, leading to cystine accumulation"],
        "treatments": ["Cystine-depleting drugs", "Kidney transplant", "Supportive care"],
        "prevalance": "Rare",
        "resourses": ["https://www.cystinosis.org"],
    }
])

        disease_data.extend([
    {
        "name": "Alkaptonuria",
        "symptoms": ["Dark urine", "Osteoarthritis", "Pigmented connective tissue"],
        "causes": ["Deficiency of homogentisate 1,2-dioxygenase enzyme"],
        "treatments": ["Symptom management", "Pain relief", "Joint replacement surgery"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.alkaptonuria.org"],
    },
    {
        "name": "Lesch-Nyhan Syndrome",
        "symptoms": ["Self-mutilation", "Gout", "Neurological impairment"],
        "causes": ["Deficiency of hypoxanthine-guanine phosphoribosyltransferase"],
        "treatments": ["Symptom management", "Psychiatric care", "Gout treatment"],
        "prevalance": "Very rare",
        "resourses": ["https://www.lns-foundation.org"],
    },
    {
        "name": "Friedreich's Ataxia",
        "symptoms": ["Ataxia", "Muscle weakness", "Vision and hearing loss"],
        "causes": ["Deficiency of frataxin due to genetic mutations"],
        "treatments": ["Physical therapy", "Cardiac care", "Supportive care"],
        "prevalance": "Rare",
        "resourses": ["https://www.curefa.org"],
    },
    {
        "name": "Cystic Fibrosis",
        "symptoms": ["Chronic cough", "Frequent lung infections", "Poor growth"],
        "causes": ["Mutation in the CFTR gene"],
        "treatments": ["Chest physiotherapy", "Enzyme replacement", "Lung transplant"],
        "prevalance": "Rare",
        "resourses": ["https://www.cff.org"],
    },
    {
        "name": "Huntington's Disease",
        "symptoms": ["Chorea", "Cognitive decline", "Mood swings"],
        "causes": ["Mutation of the HTT gene"],
        "treatments": ["Symptomatic treatment", "Physical therapy", "Psychiatric care"],
        "prevalance": "Rare",
        "resourses": ["https://www.hdsa.org"],
    },
    {
        "name": "Pachyonychia Congenita",
        "symptoms": ["Thickened nails", "Painful calluses", "Oral leukokeratosis"],
        "causes": ["Mutation in the keratin genes"],
        "treatments": ["Pain management", "Surgical removal of calluses", "Podiatric care"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.pachyonychia.org"],
    },
    {
        "name": "Gaucher's Disease",
        "symptoms": ["Enlarged liver and spleen", "Bone pain", "Fatigue"],
        "causes": ["Deficiency of glucocerebrosidase enzyme"],
        "treatments": ["Enzyme replacement therapy", "Bone pain management"],
        "prevalance": "Rare",
        "resourses": ["https://www.gaucherdisease.org"],
    },
    {
        "name": "Prader-Willi Syndrome",
        "symptoms": ["Insatiable appetite", "Obesity", "Cognitive impairment"],
        "causes": ["Loss of function of genes on chromosome 15"],
        "treatments": ["Dietary management", "Growth hormone therapy", "Behavioral therapy"],
        "prevalance": "Rare",
        "resourses": ["https://www.pwsausa.org"],
    },
    {
        "name": "Wolfram Syndrome",
        "symptoms": ["Diabetes insipidus", "Optic atrophy", "Sensorineural hearing loss"],
        "causes": ["Mutation in the WFS1 gene"],
        "treatments": ["Insulin therapy", "Visual aids", "Hearing aids"],
        "prevalance": "Very rare",
        "resourses": ["https://www.wolframsyndrome.org"],
    },
    {
        "name": "Alport Syndrome",
        "symptoms": ["Progressive kidney disease", "Hearing loss", "Eye abnormalities"],
        "causes": ["Mutations in collagen genes affecting kidney function"],
        "treatments": ["Kidney transplant", "Hearing aids", "Supportive care"],
        "prevalance": "Rare",
        "resourses": ["https://www.alportsyndrome.org"],
    },
    {
        "name": "Batten Disease",
        "symptoms": ["Seizures", "Cognitive decline", "Vision loss"],
        "causes": ["Mutations in lysosomal storage genes"],
        "treatments": ["Symptom management", "Seizure control"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.bdsra.org"],
    },
    {
        "name": "Klinefelter Syndrome",
        "symptoms": ["Infertility", "Learning difficulties", "Low testosterone"],
        "causes": ["Extra X chromosome in males (XXY genotype)"],
        "treatments": ["Testosterone replacement therapy", "Speech therapy", "Fertility treatments"],
        "prevalance": "Rare",
        "resourses": ["https://www.klinefeltersyndrome.org"],
    },
    {
        "name": "Cohen Syndrome",
        "symptoms": ["Developmental delay", "Coarse facial features", "Retinal degeneration"],
        "causes": ["Mutation in the COH1 gene"],
        "treatments": ["Speech therapy", "Physical therapy", "Vision aids"],
        "prevalance": "Very rare",
        "resourses": ["https://www.cohensyndrome.org"],
    },
    {
        "name": "Mechel's Syndrome",
        "symptoms": ["Microcephaly", "Seizures", "Eye abnormalities"],
        "causes": ["Mutation in the MKS1 gene"],
        "treatments": ["Symptomatic treatment", "Seizure management"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.mksfoundation.org"],
    },
    {
        "name": "Menke's Syndrome",
        "symptoms": ["Hypotonia", "Seizures", "Developmental delay"],
        "causes": ["Deficiency of copper transport"],
        "treatments": ["Copper supplementation", "Supportive care"],
        "prevalance": "Very rare",
        "resourses": ["https://www.menkessyndrome.org"],
    },
    {
        "name": "Osteopetrosis",
        "symptoms": ["Bone pain", "Bone fractures", "Delayed growth"],
        "causes": ["Defective osteoclast function leading to dense bones"],
        "treatments": ["Bone marrow transplant", "Symptomatic treatment"],
        "prevalance": "Rare",
        "resourses": ["https://www.osteopetrosis.org"],
    },
    {
        "name": "Leigh Syndrome",
        "symptoms": ["Developmental regression", "Respiratory problems", "Movement disorders"],
        "causes": ["Mitochondrial mutations"],
        "treatments": ["Symptom management", "Respiratory support", "Nutritional support"],
        "prevalance": "Rare",
        "resourses": ["https://www.leighsyndrome.org"],
    },
    {
        "name": "Williams Syndrome",
        "symptoms": ["Cardiovascular problems", "Developmental delays", "Hypercalcemia"],
        "causes": ["Deletion of genes on chromosome 7"],
        "treatments": ["Cardiovascular management", "Speech therapy", "Physical therapy"],
        "prevalance": "Rare",
        "resourses": ["https://www.williams-syndrome.org"],
    },
    {
        "name": "Sickle Cell Disease",
        "symptoms": ["Pain episodes", "Fatigue", "Anemia"],
        "causes": ["Mutation in the hemoglobin gene"],
        "treatments": ["Pain management", "Hydroxyurea", "Blood transfusions"],
        "prevalance": "Rare",
        "resourses": ["https://www.sicklecelldisease.org"],
    },
    {
        "name": "Kawasaki Disease",
        "symptoms": ["Fever", "Rash", "Conjunctivitis"],
        "causes": ["Unknown, possibly autoimmune or infection-triggered"],
        "treatments": ["IV immunoglobulin", "Aspirin therapy"],
        "prevalance": "Rare",
        "resourses": ["https://www.kdfoundation.org"],
    },
    {
        "name": "Prion Disease",
        "symptoms": ["Rapid mental deterioration", "Motor issues", "Memory loss"],
        "causes": ["Misfolded prion proteins"],
        "treatments": ["No cure, symptom management"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.cjd-foundation.org"],
    },
])

        disease_data.extend([
    {
        "name": "Alexander Disease",
        "symptoms": ["Seizures", "Muscle weakness", "Cognitive decline"],
        "causes": ["Mutation in the GFAP gene"],
        "treatments": ["Symptom management", "Physical therapy", "Anticonvulsants"],
        "prevalance": "Very rare",
        "resourses": ["https://www.alexanderdisease.org"],
    },
    {
        "name": "Bardet-Biedl Syndrome",
        "symptoms": ["Obesity", "Retinal degeneration", "Polydactyly"],
        "causes": ["Mutations in multiple genes involved in cilia function"],
        "treatments": ["Symptom management", "Vision aids", "Weight management"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.bardetbiedl.org"],
    },
    {
        "name": "Rett Syndrome",
        "symptoms": ["Loss of motor skills", "Repetitive hand movements", "Speech loss"],
        "causes": ["Mutations in the MECP2 gene"],
        "treatments": ["Physical therapy", "Speech therapy", "Seizure management"],
        "prevalance": "Rare",
        "resourses": ["https://www.rettsyndrome.org"],
    },
    {
        "name": "Menkes Syndrome",
        "symptoms": ["Copper deficiency", "Hypotonia", "Seizures"],
        "causes": ["Mutation in the ATP7A gene affecting copper transport"],
        "treatments": ["Copper supplementation", "Supportive care"],
        "prevalance": "Very rare",
        "resourses": ["https://www.menkessyndrome.org"],
    },
    {
        "name": "Hypophosphatasia",
        "symptoms": ["Brittle bones", "Premature loss of teeth", "Short stature"],
        "causes": ["Deficiency in the tissue-nonspecific alkaline phosphatase enzyme"],
        "treatments": ["Enzyme replacement therapy", "Pain management"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.hypophosphatasia.org"],
    },
    {
        "name": "Hyper IgM Syndrome",
        "symptoms": ["Frequent infections", "Low immunoglobulin levels", "Fatigue"],
        "causes": ["Deficiency in CD40 ligand affecting immune function"],
        "treatments": ["Antibiotics", "Immunoglobulin replacement", "Stem cell transplant"],
        "prevalance": "Rare",
        "resourses": ["https://www.hyperigm.org"],
    },
    {
        "name": "Pinealoma",
        "symptoms": ["Headache", "Vision problems", "Hormonal imbalance"],
        "causes": ["Tumors in the pineal gland"],
        "treatments": ["Surgical removal", "Radiation therapy"],
        "prevalance": "Very rare",
        "resourses": ["https://www.pinealoma.org"],
    },
    {
        "name": "Spinal Muscular Atrophy",
        "symptoms": ["Progressive muscle weakness", "Loss of motor skills", "Respiratory failure"],
        "causes": ["Mutation in the SMN1 gene affecting motor neurons"],
        "treatments": ["Gene therapy", "Physical therapy", "Respiratory support"],
        "prevalance": "Rare",
        "resourses": ["https://www.curesma.org"],
    },
    {
        "name": "Niemann-Pick Disease",
        "symptoms": ["Enlarged liver and spleen", "Cognitive decline", "Movement problems"],
        "causes": ["Deficiency of acid sphingomyelinase"],
        "treatments": ["Symptom management", "Liver transplant", "Supportive care"],
        "prevalance": "Very rare",
        "resourses": ["https://www.nnpdf.org"],
    },
    {
        "name": "Ondine's Curse",
        "symptoms": ["Failure to breathe during sleep", "Hypoventilation", "Cyanosis"],
        "causes": ["Deficiency in automatic control of breathing"],
        "treatments": ["Ventilatory support", "Positive pressure therapy"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.ondinescurse.org"],
    },
    {
        "name": "Syringomyelia",
        "symptoms": ["Pain", "Muscle weakness", "Loss of sensation"],
        "causes": ["Fluid-filled cysts in the spinal cord"],
        "treatments": ["Surgery", "Pain management", "Physical therapy"],
        "prevalance": "Rare",
        "resourses": ["https://www.syringomyelia.org"],
    },
    {
        "name": "Ehlers-Danlos Syndrome",
        "symptoms": ["Hyperflexible joints", "Skin hyper-elasticity", "Frequent bruising"],
        "causes": ["Defects in collagen synthesis"],
        "treatments": ["Physical therapy", "Pain management", "Surgical intervention for joint issues"],
        "prevalance": "Rare",
        "resourses": ["https://www.ehlers-danlos.com"],
    },
    {
        "name": "FOP (Fibrodysplasia Ossificans Progressiva)",
        "symptoms": ["Progressive bone formation", "Immobility", "Painful swelling"],
        "causes": ["Mutations in the ACVR1 gene"],
        "treatments": ["Symptom management", "Pain control", "Mobility aids"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.ifopa.org"],
    },
    {
        "name": "Cerebrotendinous Xanthomatosis",
        "symptoms": ["Neurological issues", "Tendon xanthomas", "Ataxia"],
        "causes": ["Defective cholesterol metabolism"],
        "treatments": ["Cholesterol-lowering drugs", "Symptom management"],
        "prevalance": "Very rare",
        "resourses": ["https://www.cerebrotendinous.org"],
    },
    {
        "name": "Churg-Strauss Syndrome",
        "symptoms": ["Asthma", "Eosinophilia", "Vasculitis"],
        "causes": ["Autoimmune disease affecting small blood vessels"],
        "treatments": ["Steroids", "Immunosuppressive therapy", "Symptom management"],
        "prevalance": "Rare",
        "resourses": ["https://www.churgstrausssyndrome.org"],
    },
    {
        "name": "Hermansky-Pudlak Syndrome",
        "symptoms": ["Bleeding issues", "Albinism", "Pulmonary fibrosis"],
        "causes": ["Defects in lysosomal function"],
        "treatments": ["Bone marrow transplant", "Bleeding disorder management"],
        "prevalance": "Very rare",
        "resourses": ["https://www.hpsnetwork.org"],
    },
    {
        "name": "Celiac Disease",
        "symptoms": ["Diarrhea", "Abdominal pain", "Fatigue"],
        "causes": ["Gluten intolerance triggering immune response"],
        "treatments": ["Gluten-free diet"],
        "prevalance": "Rare",
        "resourses": ["https://www.celiac.org"],
    },
    {
        "name": "Marfan Syndrome",
        "symptoms": ["Tall stature", "Heart issues", "Flexible joints"],
        "causes": ["Mutation in the fibrillin-1 gene affecting connective tissue"],
        "treatments": ["Cardiovascular care", "Physical therapy", "Surgical intervention for aortic issues"],
        "prevalance": "Rare",
        "resourses": ["https://www.marfan.org"],
    },
    {
        "name": "Hematohidrosis",
        "symptoms": ["Sweating blood", "Headaches", "Fatigue"],
        "causes": ["Extreme stress causing blood vessels to rupture"],
        "treatments": ["Stress management", "Symptom relief"],
        "prevalance": "Extremely rare",
        "resourses": ["https://www.hematohidrosis.org"],
    },
    {
        "name": "Vascular Ehlers-Danlos Syndrome",
        "symptoms": ["Thin skin", "Easy bruising", "Vascular rupture"],
        "causes": ["Mutation in the COL3A1 gene affecting collagen synthesis"],
        "treatments": ["Cardiovascular care", "Surgical repair of ruptured vessels"],
        "prevalance": "Very rare",
        "resourses": ["https://www.vedsfoundation.org"],
    },
    {
        "name": "Batten Disease",
        "symptoms": ["Seizures", "Vision loss", "Cognitive decline"],
        "causes": ["Lysosomal storage disorders"],
        "treatments": ["Seizure management", "Supportive care"],
        "prevalance": "Very rare",
        "resourses": ["https://www.bdsra.org"],
    },
    {
        "name": "Tay-Sachs Disease",
        "symptoms": ["Progressive mental and physical deterioration", "Cherry-red spot in the eyes", "Deafness"],
        "causes": ["Deficiency of hexosaminidase A enzyme"],
        "treatments": ["Symptom management", "Palliative care"],
        "prevalance": "Very rare",
        "resourses": ["https://www.ntsad.org"],
    },
])


        for item in disease_data:
            DiseaseCard(
                name=item['name'],
                symptoms=item['symptoms'],
                causes=item['causes'],
                treatments=item['treatments'],
                prevalance=item['prevalance'],
                resourses=item['resourses']
            ).save()

        professional_centers_data = [
    {
        "name": "Toronto Rare Disease Clinic",
        "location": "Toronto, Ontario, Canada",
        "google_maps_embed": "https://maps.google.com/?q=Toronto+Rare+Disease+Clinic",
        "diseases": ["Diabetes", "Hypertension"],
        "contact_info": {
            "phone": "+1 416-555-1234",
            "email": "info@torontorarediseaseclinic.ca",
            "website": "https://torontorarediseaseclinic.ca"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Los Angeles Center for Rare Diseases",
        "location": "Los Angeles, California, USA",
        "google_maps_embed": "https://maps.google.com/?q=Los+Angeles+Center+for+Rare+Diseases",
        "diseases": ["Asthma", "Alzheimer's Disease"],
        "contact_info": {
            "phone": "+1 213-555-5678",
            "email": "contact@lararediseasecenter.org",
            "website": "https://lararediseasecenter.org"
        },
        "hours_of_operation": "24/7"
    },
    {
        "name": "Mexico City Rare Disorders Institute",
        "location": "Mexico City, Mexico",
        "google_maps_embed": "https://maps.google.com/?q=Mexico+City+Rare+Disorders+Institute",
        "diseases": ["Tuberculosis", "COVID-19"],
        "contact_info": {
            "phone": "+52 55 1234 5678",
            "email": "atencion@institutoraredisorders.mx",
            "website": "https://institutoraredisorders.mx"
        },
        "hours_of_operation": "8am - 6pm Mon-Sat"
    },
    {
        "name": "London Rare Disease Center",
        "location": "London, England, UK",
        "google_maps_embed": "https://maps.google.com/?q=London+Rare+Disease+Center",
        "diseases": ["Cystic Fibrosis", "Gaucher's Disease"],
        "contact_info": {
            "phone": "+44 20 7946 1234",
            "email": "contact@londonrarediseasecentre.org",
            "website": "https://londonrarediseasecentre.org"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Paris Institute for Rare Diseases",
        "location": "Paris, France",
        "google_maps_embed": "https://maps.google.com/?q=Paris+Institute+for+Rare+Diseases",
        "diseases": ["Marfan Syndrome", "Duchenne Muscular Dystrophy"],
        "contact_info": {
            "phone": "+33 1 70 18 62 94",
            "email": "contact@rare-diseases-paris.fr",
            "website": "https://rare-diseases-paris.fr"
        },
        "hours_of_operation": "9am - 6pm Mon-Fri"
    },
    {
        "name": "Berlin Rare Disease Treatment Center",
        "location": "Berlin, Germany",
        "google_maps_embed": "https://maps.google.com/?q=Berlin+Rare+Disease+Treatment+Center",
        "diseases": ["Huntington's Disease", "Wilson's Disease"],
        "contact_info": {
            "phone": "+49 30 12345678",
            "email": "info@berlinrarediseasecenter.de",
            "website": "https://berlinrarediseasecenter.de"
        },
        "hours_of_operation": "8am - 4pm Mon-Fri"
    },
    {
        "name": "New York Rare Disease Research Institute",
        "location": "New York, New York, USA",
        "google_maps_embed": "https://maps.google.com/?q=New+York+Rare+Disease+Research+Institute",
        "diseases": ["Multiple Sclerosis", "Amyotrophic Lateral Sclerosis"],
        "contact_info": {
            "phone": "+1 212-555-9876",
            "email": "info@nyrareinstitute.org",
            "website": "https://nyrareinstitute.org"
        },
        "hours_of_operation": "9am - 6pm Mon-Fri"
    },
    {
        "name": "Sydney Rare Disease Clinic",
        "location": "Sydney, New South Wales, Australia",
        "google_maps_embed": "https://maps.google.com/?q=Sydney+Rare+Disease+Clinic",
        "diseases": ["Ehlers-Danlos Syndrome", "Fabry Disease"],
        "contact_info": {
            "phone": "+61 2 1234 5678",
            "email": "contact@sydneyrarediseaseclinic.com.au",
            "website": "https://sydneyrarediseaseclinic.com.au"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Toronto Neurology and Rare Disease Center",
        "location": "Toronto, Ontario, Canada",
        "google_maps_embed": "https://maps.google.com/?q=Toronto+Neurology+and+Rare+Disease+Center",
        "diseases": ["Parkinson's Disease", "Neurofibromatosis"],
        "contact_info": {
            "phone": "+1 416-555-7890",
            "email": "contact@torontoneurologycenter.ca",
            "website": "https://torontoneurologycenter.ca"
        },
        "hours_of_operation": "8am - 6pm Mon-Fri"
    },
    {
        "name": "São Paulo Rare Disease Center",
        "location": "São Paulo, Brazil",
        "google_maps_embed": "https://maps.google.com/?q=São+Paulo+Rare+Disease+Center",
        "diseases": ["Hemophilia", "Spinal Muscular Atrophy"],
        "contact_info": {
            "phone": "+55 11 1234 5678",
            "email": "contato@sprarecenter.com.br",
            "website": "https://sprarecenter.com.br"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Madrid Rare Disease Institute",
        "location": "Madrid, Spain",
        "google_maps_embed": "https://maps.google.com/?q=Madrid+Rare+Disease+Institute",
        "diseases": ["Tay-Sachs Disease", "Menkes Syndrome"],
        "contact_info": {
            "phone": "+34 91 123 4567",
            "email": "contact@madridraredisease.org",
            "website": "https://madridraredisease.org"
        },
        "hours_of_operation": "8am - 4pm Mon-Fri"
    },
    {
        "name": "Dubai Rare Disease Center",
        "location": "Dubai, United Arab Emirates",
        "google_maps_embed": "https://maps.google.com/?q=Dubai+Rare+Disease+Center",
        "diseases": ["Cystic Fibrosis", "Batten Disease"],
        "contact_info": {
            "phone": "+971 4 123 4567",
            "email": "info@dubairarediseasecenter.ae",
            "website": "https://dubairarediseasecenter.ae"
        },
        "hours_of_operation": "9am - 5pm Sun-Thurs"
    },
    {
        "name": "Mumbai Rare Disease Clinic",
        "location": "Mumbai, Maharashtra, India",
        "google_maps_embed": "https://maps.google.com/?q=Mumbai+Rare+Disease+Clinic",
        "diseases": ["Progeria", "Celiac Disease"],
        "contact_info": {
            "phone": "+91 22 1234 5678",
            "email": "contact@mumbai.rarediseaseclinic.in",
            "website": "https://mumbai.rarediseaseclinic.in"
        },
        "hours_of_operation": "9am - 5pm Mon-Sat"
    },
    {
        "name": "Hong Kong Rare Disease Treatment Center",
        "location": "Hong Kong",
        "google_maps_embed": "https://maps.google.com/?q=Hong+Kong+Rare+Disease+Treatment+Center",
        "diseases": ["Albinism", "Alpha-1 Antitrypsin Deficiency"],
        "contact_info": {
            "phone": "+852 1234 5678",
            "email": "contact@hongkongrarecenter.hk",
            "website": "https://hongkongrarecenter.hk"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Seoul Rare Disease Institute",
        "location": "Seoul, South Korea",
        "google_maps_embed": "https://maps.google.com/?q=Seoul+Rare+Disease+Institute",
        "diseases": ["Osteogenesis Imperfecta", "Lysosomal Storage Disorders"],
        "contact_info": {
            "phone": "+82 2 1234 5678",
            "email": "contact@seoulraredisease.org",
            "website": "https://seoulraredisease.org"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Tokyo Rare Disease Center",
        "location": "Tokyo, Japan",
        "google_maps_embed": "https://maps.google.com/?q=Tokyo+Rare+Disease+Center",
        "diseases": ["Spinal Muscular Atrophy", "Neurodegenerative Diseases"],
        "contact_info": {
            "phone": "+81 3 1234 5678",
            "email": "info@tokyorarediseasecenter.jp",
            "website": "https://tokyorarediseasecenter.jp"
        },
        "hours_of_operation": "9am - 6pm Mon-Fri"
    },
    {
        "name": "Cape Town Rare Disease Institute",
        "location": "Cape Town, South Africa",
        "google_maps_embed": "https://maps.google.com/?q=Cape+Town+Rare+Disease+Institute",
        "diseases": ["Tuberous Sclerosis", "Ehlers-Danlos Syndrome"],
        "contact_info": {
            "phone": "+27 21 123 4567",
            "email": "info@capetownraredisease.org",
            "website": "https://capetownraredisease.org"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Moscow Rare Disease Clinic",
        "location": "Moscow, Russia",
        "google_maps_embed": "https://maps.google.com/?q=Moscow+Rare+Disease+Clinic",
        "diseases": ["Sickle Cell Anemia", "Huntington's Disease"],
        "contact_info": {
            "phone": "+7 495 123 4567",
            "email": "contact@moscowrarediseaseclinic.ru",
            "website": "https://moscowrarediseaseclinic.ru"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Rome Rare Disease Center",
        "location": "Rome, Italy",
        "google_maps_embed": "https://maps.google.com/?q=Rome+Rare+Disease+Center",
        "diseases": ["Hemophilia", "Marfan Syndrome"],
        "contact_info": {
            "phone": "+39 06 1234 5678",
            "email": "info@romeraresdiseasecenter.it",
            "website": "https://romeraresdiseasecenter.it"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Vienna Rare Disease Institute",
        "location": "Vienna, Austria",
        "google_maps_embed": "https://maps.google.com/?q=Vienna+Rare+Disease+Institute",
        "diseases": ["Tay-Sachs Disease", "Lynch Syndrome"],
        "contact_info": {
            "phone": "+43 1 12345678",
            "email": "contact@viennararesdisease.org",
            "website": "https://viennararesdisease.org"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Zurich Rare Disease Center",
        "location": "Zurich, Switzerland",
        "google_maps_embed": "https://maps.google.com/?q=Zurich+Rare+Disease+Center",
        "diseases": ["Von Willebrand Disease", "Pulmonary Arterial Hypertension"],
        "contact_info": {
            "phone": "+41 44 123 4567",
            "email": "info@zurichrarediseasecenter.ch",
            "website": "https://zurichrarediseasecenter.ch"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    },
    {
        "name": "Beijing Rare Disease Clinic",
        "location": "Beijing, China",
        "google_maps_embed": "https://maps.google.com/?q=Beijing+Rare+Disease+Clinic",
        "diseases": ["Hemophilia", "Cystic Fibrosis"],
        "contact_info": {
            "phone": "+86 10 1234 5678",
            "email": "info@beijingrarediseaseclinic.cn",
            "website": "https://beijingrarediseaseclinic.cn"
        },
        "hours_of_operation": "9am - 6pm Mon-Fri"
    },
    {
        "name": "Singapore Rare Disease Center",
        "location": "Singapore",
        "google_maps_embed": "https://maps.google.com/?q=Singapore+Rare+Disease+Center",
        "diseases": ["Thalassemia", "Duchenne Muscular Dystrophy"],
        "contact_info": {
            "phone": "+65 1234 5678",
            "email": "info@singaporeraredisease.org",
            "website": "https://singaporeraredisease.org"
        },
        "hours_of_operation": "9am - 5pm Mon-Fri"
    }
]


        for center in professional_centers_data:
            ProfessionalCenter(
                name=center['name'],
                location=center['location'],
                google_maps_embed=center['google_maps_embed'],
                diseases=center['diseases'],
                contact_info=center['contact_info'],
                hours_of_operation=center['hours_of_operation']
            ).save()

        return jsonify({"message": "Database seeded successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    try:
        connect('rare_diseases', host=os.getenv('MONGO_URI'))
        print("MongoDB connection successful!")
    except Exception as e:
        print("MongoDB connection failed:", e)
    app.run(debug=True)

