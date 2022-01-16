
from app.local.persister.file_persister import FilePersister
from app.test.persister.persister_test_base import PersisterTestBase
import tempfile

class TestFilePersister(PersisterTestBase):
    def get_persister(self):
        tempfile_name = tempfile.NamedTemporaryFile("w").name
        return FilePersister(tempfile_name)
