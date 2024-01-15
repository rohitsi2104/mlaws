from flask import Flask, request, jsonify
from pymongo import MongoClient
from urllib.parse import quote_plus
app = Flask(__name__)

mongo_username = 'rohitsi2104'
mongo_password = 'Tome@nothing0'

cluster_uri = 'mongodb+srv://{}:{}@codingtask.eizj4j4.mongodb.net/?retryWrites=true&w=majority'.format(
    quote_plus(mongo_username), quote_plus(mongo_password)
)
client = MongoClient(cluster_uri)
db = client["ModelMetaData"]
tenant_collection = db['tenant']
project_metadata_collection = db['project_metadata']


class Tenant:
    def __init__(self, name):
        self.name = name

class ProjectMetadata:
    def __init__(self, tenant, local_csv_location, s3_model_location, model_evaluation_results):
        self.tenant = tenant
        self.local_csv_location = local_csv_location
        self.s3_model_location = s3_model_location
        self.model_evaluation_results = model_evaluation_results

@app.route('/')
def home():
    return 'Model Data Saved'
@app.route('/create_project', methods=['POST'])
def create_project_rout():


    data = request.get_json()

    tenant_name = data.get('tenant_name', 'Default Tenant')
    local_csv_location = data.get('local_csv_location', '/path/to/local/csv')
    s3_model_location = data.get('s3_model_location', 's3://bucket/model')
    model_evaluation_results = data.get('model_evaluation_results', 'Evaluation: 90% accuracy')

    tenant = Tenant(name=tenant_name)
    tenant_collection.insert_one({'name': tenant.name})

    project_metadata_collection.insert_one({
        'tenant': tenant.name,
        'local_csv_location': local_csv_location,
        's3_model_location': s3_model_location,
        'model_evaluation_results': model_evaluation_results
    })


    return jsonify({'message': 'Project created successfully'})



@app.teardown_appcontext
def close_mongo_connection(exception):
    client.close()

if __name__ == '__main__':
    app.run(debug=True)
