
from app.local.persister.pickle_persister import PicklePersister
from app.test.persister.persister_test_base import PersisterTestBase
import tempfile

class TestFilePersister(PersisterTestBase):
    def get_persister(self):
        tempfile_name = tempfile.NamedTemporaryFile("w").name
        return PicklePersister(tempfile_name)
