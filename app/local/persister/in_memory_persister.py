from app.local.persister.persister import Persister
import uuid


class InMemoryPersister(Persister):
    def __init__(self):
        self.d = {}

    def add(self, project_id, datum):
        my_uuid = uuid.uuid4()
        if project_id in self.d:
            project = self.d[project_id]
        else:
            project = {}
            self.d[project_id] = project
        project[my_uuid] = datum
        return my_uuid

    def get(self, project_id, my_uuid):
        project = self.d[project_id]
        if project is None:
            return None
        return project.get(my_uuid, None)

    def get_all(self, project_id):
        project = self.d.get(project_id, None)
        if project is None:
            return None
        return list(project.keys())

    def delete(self, project_id, my_uuid):
        project = self.d.get(project_id, None)
        if project is not None:
            project.pop(my_uuid)

