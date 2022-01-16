from abc import ABC, abstractmethod
from app.local.persister.datum import Datum


class PersisterTestBase(ABC):

    @abstractmethod
    def get_persister(self):
        pass

    def test_add(self):
        persister = self.get_persister()
        project_id = "myproject"
        datum_uuid = persister.add(project_id, Datum("cat", {"meows": 1.0}))
        datum = persister.get(project_id, datum_uuid)
        assert ("cat" == datum.outcome)

    def test_delete(self):
        persister = self.get_persister()
        project_id = "myproject"
        datum_uuid = persister.add(project_id, Datum("cat", {"meows": 1.0}))
        persister.delete(project_id, datum_uuid)
        assert persister.get(project_id, datum_uuid) is None
