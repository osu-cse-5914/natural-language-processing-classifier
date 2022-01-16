import time

from app.local.persister.datum import Datum
from app.local.persister.persister import Persister
import uuid
import os
import jsons
import json
import pickle

class PicklePersister(Persister):
    def __init__(self, data_directory):
        self.data_directory = data_directory
        print(f"Data dir: {data_directory}")
        os.makedirs(self.data_directory, exist_ok=True)

    def add(self, project_id, datum):
        project_dir = os.path.join(self.data_directory, project_id)
        os.makedirs(project_dir, exist_ok=True)

        my_uuid = uuid.uuid4()
        filepath = os.path.join(project_dir, str(my_uuid) + ".pickle")

        with open(filepath, "wb") as outfile:
            pickle.dump(datum, outfile)
        return my_uuid

    def get(self, project_id, my_uuid):
        file_path = os.path.join(self.data_directory, project_id, str(my_uuid) + ".pickle")
        if os.path.isfile(file_path):
            with open(os.path.join(file_path), "rb") as outfile:
                return pickle.load(outfile)
        else:
            return None

    def get_all(self, project_id):
        result = []
        if os.path.exists(os.path.join(self.data_directory, project_id)):
            for f in os.listdir(os.path.join(self.data_directory, project_id)):
                if f.endswith(".pickle"):
                    result.append(f[:-7])
        return result

    def delete(self, project_id, my_uuid):
        os.remove(os.path.join(self.data_directory, project_id, str(my_uuid)+".pickle"))
