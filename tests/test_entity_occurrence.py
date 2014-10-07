from .manager_case import ManagerTestCase
from iepy.data.models import EntityOccurrence
from .factories import (
    EntityFactory, EntityKindFactory,
    TextSegmentFactory, RelationFactory,
    EntityOccurrenceFactory
)

class TestEntityOccurrences(ManagerTestCase):
    def setUp(self):
        self.k_person = EntityKindFactory(name='person')
        self.k_location = EntityKindFactory(name='location')
        self.e_john = EntityFactory(key='john', kind=self.k_person)
        self.e_bob = EntityFactory(key='bob', kind=self.k_person)
        self.e_argentina = EntityFactory(key='argentina', kind=self.k_location)
        self.e_germany = EntityFactory(key='germany', kind=self.k_location)
        self.e_australia = EntityFactory(key='australia', kind=self.k_location)
        self.person_location_relation = RelationFactory(
            left_entity_kind=self.k_person,
            right_entity_kind=self.k_location
        )

    def create_segment_with_eos(self, entities):
        segment = TextSegmentFactory()
        doc = segment.document
        offset = 0
        eos = []
        for entity in entities:
            eo = EntityOccurrenceFactory(
                document=doc, entity=entity,
                offset=offset, offset_end=offset+1
            )
            eos.append(eo)
            offset += 2
            segment.entity_occurrences.add(eo)
        return segment, eos

    def test_delete_removes_one_evidences(self):
        segment, eos = self.create_segment_with_eos([self.e_john, self.e_argentina])
        evidences_before = segment.get_labeled_evidences(self.person_location_relation)
        self.assertEqual(len(list(evidences_before)), 1)
        eo = eos[0]
        eo.delete()
        evidences_after = segment.get_labeled_evidences(self.person_location_relation)
        self.assertEqual(len(list(evidences_after)), 0)

    def test_delete_removes_multiple_evidences(self):
        segment, eos = self.create_segment_with_eos([
            self.e_john, self.e_bob, self.e_argentina, self.e_germany
        ])
        evidences_before = segment.get_labeled_evidences(self.person_location_relation)
        self.assertEqual(len(list(evidences_before)), 4)  # each person with each location
        eo = eos[0]
        eo.delete()
        evidences_after = segment.get_labeled_evidences(self.person_location_relation)
        self.assertEqual(len(list(evidences_after)), 2)  # only bob with each location