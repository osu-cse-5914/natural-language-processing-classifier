import http
import os
from typing import List, Any

import jsons
import logging
import uuid

from flask import Flask, request, jsonify
from flasgger import Swagger
from sklearn.linear_model import Perceptron

from app.local.featuregen.unigram_feature_generator import UnigramFeatureGenerator
from app.local.persister.datum import Datum
from app.local.persister.file_persister import FilePersister
from app.local.persister.in_memory_persister import InMemoryPersister
from app.local.persister.model import Model
from app.local.persister.pickle_persister import PicklePersister

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SWAGGER'] = {
    "title": "sample",
    "uiversion": 3
}

Swagger(app)
persister_implementation = os.environ.get("NLPC_PERSIST", "PICKLE")
if persister_implementation == "IN_MEMORY":
    persister = InMemoryPersister()
    model_persister = InMemoryPersister()
elif persister_implementation == "PICKLE":
    persister = PicklePersister(os.path.join(os.environ.get("NLPC_FILE_SYSTEM_DATA_DIR", "/nlpc_data"), "data"))
    model_persister = PicklePersister(os.path.join(os.environ.get("NLPC_FILE_SYSTEM_DATA_DIR", "/nlpc_data"), "models"))
else:
    persister = FilePersister(os.path.join(os.environ.get("NLPC_FILE_SYSTEM_DATA_DIR", "/nlpc_data"), "data"))
    model_persister = FilePersister(os.path.join(os.environ.get("NLPC_FILE_SYSTEM_DATA_DIR", "/nlpc_data"), "models"))

language_classifier_feature_generator = UnigramFeatureGenerator()


@app.route('/languageclassifier/data/<project_id>/<model_id>', methods=['POST'])
def nlc_get(project_id, model_id: str):
    '''
       Get one data point
       ---
       tags:
         - natural language classifier
       parameters:
          - in: path
            name: project_id
            type: string
            required: true
            description: project id
          - in: path
            name: model_id
            type: string
            required: true
            description: ID to get
          - name: text
            in: body
            schema:
              type: array
              items:
                type: string
       responses:
         200:
           description: OK

       '''
    j = jsons.loads(request.data)
    model = model_persister.get(project_id, uuid.UUID(model_id))
    features = []
    for input_datum in j:
        lc_feats = language_classifier_feature_generator.generate_features(input_datum)
        features_for_this_datum = []
        for feature_name in model.feature_names:
            features_for_this_datum.append(lc_feats.get(feature_name, 0.0))
        features.append(features_for_this_datum)
    predictions = model.clf.predict(features)
    return jsons.dumps(predictions)


@app.route('/languageclassifier/data/<project_id>', methods=['POST'])
def nlc_add(project_id):
    '''adding endpoint
        This is a description
        ---
        tags:
         - natural language classifier
        parameters:
          - in: path
            name: project_id
            type: string
            required: true
            description: project id
          - name: text
            in: body
            schema:
              type: array
              items:
                type: object
                properties:
                  label:
                    type: string
                  passage:
                    type: string
        responses:
          200:
            description: OK

        '''
    result = []
    for d in jsons.loads(request.data):
        feats = language_classifier_feature_generator.generate_features(d["passage"])
        id_for_this_datum = persister.add(project_id, Datum(d["label"], feats))
        result.append(id_for_this_datum)
    return jsons.dumps(result)


@app.route('/model/<project_id>/<model_id>', methods=['GET'])
def get_model(project_id, model_id):
    '''
       Get one data point
       ---
       tags:
         - model
       parameters:
           - in: path
             name: project_id
             type: string
             required: true
             description: project id
           - in: path
             name: model_id
             type: string
             required: true
             description: ID to get
       responses:
         200:
           description: OK

       '''

    return jsons.dumps(model_persister.get(project_id, uuid.UUID(model_id)))


@app.route('/model/<project_id>', methods=['GET'])
def get_all_models(project_id):
    '''
       Get all model ids
       ---
       tags:
         - model
       parameters:
         - in: path
           name: project_id
           type: string
           required: true
           description: project id
       responses:
         200:
           description: OK

       '''

    return jsons.dumps(model_persister.get_all(project_id))


@app.route('/model/<project_id>', methods=['POST'])
def train(project_id):
    '''
    Model training endpoint
    This is a model training endpoint description
    ---
    tags:
      - model
    parameters:
      - in: path
        name: project_id
        type: string
        required: true
        description: project id
      - name: text
        in: body
        schema:
          type: object
          properties:
            model_name:
              type: string
    responses:
      200:
        description: ok
    '''

    all_feature_names = set()
    all_outcome_names = set()
    for datumId in persister.get_all(project_id):
        datum = persister.get(project_id, datumId)
        print(str(datum))
        all_feature_names.update(datum.features.keys())
        all_outcome_names.add(datum.outcome)
    all_feature_names_as_list = list(all_feature_names)
    all_outcome_names_as_list = list(all_outcome_names)
    all_features = []
    all_outcomes = []
    for datumId in persister.get_all(project_id):
        datum = persister.get(project_id, datumId)
        all_features_for_this_data_point = list()
        for feature_name in all_feature_names_as_list:
            val = datum.features.get(feature_name,0.0)
            all_features_for_this_data_point.append(val)
        all_features.append(all_features_for_this_data_point)
        all_outcomes.append(datum.outcome)
    clf = Perceptron(max_iter=50)
    clf.fit(all_features, all_outcomes)
    model_val = Model(clf, all_feature_names_as_list, all_outcome_names_as_list)
    model_id = model_persister.add(project_id, model_val)
    return jsons.dumps(model_id)


@app.route('/data/<project_id>/<datum_id>', methods=['GET'])
def get(project_id, datum_id):
    '''
    Get one data point
    ---
    tags:
      - data
    parameters:
        - in: path
          name: project_id
          type: string
          required: true
          description: project id
        - in: path
          name: datum_id
          type: string
          required: true
          description: ID to get
    responses:
      200:
        description: OK

    '''

    return jsons.dumps(persister.get(project_id, uuid.UUID(datum_id)))


@app.route('/data/<project_id>/<datum_id>', methods=['DELETE'])
def delete(project_id, datum_id):
    '''
    Get one data point
    ---
    tags:
      - data
    parameters:
        - in: path
          name: project_id
          type: string
          required: true
          description: project id
        - in: path
          name: datum_id
          type: string
          required: true
          description: ID to delete
    responses:
      200:
        description: OK

    '''

    persister.delete(project_id, uuid.UUID(datum_id))
    return '', http.HTTPStatus.NO_CONTENT


@app.route('/data/<project_id>', methods=['GET'])
def getAll(project_id):
    '''
    Get all data points
    ---
    tags:
      - data
    parameters:
        - in: path
          name: project_id
          type: string
          required: true
          description: project id
    responses:
      200:
        description: OK

    '''
    return jsons.dumps(persister.get_all(project_id))


class DevServer:
    def __init__(self):
        self.port = 8081

    def run(self):
        app.run("localhost", self.port, debug=True)
