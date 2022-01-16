import pytest

from app.local.persister.datum import Datum
from app.local.persister.in_memory_persister import InMemoryPersister
from app.test.persister.persister_test_base import PersisterTestBase


class TestInMemoryPersister(PersisterTestBase):
    def get_persister(self):
        return InMemoryPersister()