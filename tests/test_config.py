import enum
import pytest
from hazel.config import (
    asbool,
    asenum,
    aslist,
    aslist_cronly,
    uuid_to_slug,
    slug_to_uuid,
)


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2


class TestUtilityFunctions:
    @pytest.mark.parametrize(
        'value,result',
        [
            (1, True),
            ('t', True),
            ('T', True),
            ('true', True),
            ('True', True),
            ('TRUE', True),
            ('y', True),
            ('yes', True),
            ('Yes', True),
            ('YES', True),
            (0, False),
            ('f', False),
            ('F', False),
            ('false', False),
            ('False', False),
            ('FALSE', False),
            ('n', False),
            ('no', False),
            ('No', False),
            ('NO', False),
            (2, False),
            ('Z', False),
        ],
    )
    def test_asbool(self, value, result):
        assert asbool(value) == result

    @pytest.mark.parametrize(
        'value,result',
        [('1\n2', ['1', '2']), ('1 2', ['1 2']), ('one two 3', ['one two 3'])],
    )
    def test_aslist_cronly(self, value, result):
        assert aslist_cronly(value) == result

    @pytest.mark.parametrize(
        'value,result,flatten',
        [
            ('1 2', ['1', '2'], True),
            ('1\n2', ['1', '2'], True),
            ('one two 3', ['one', 'two', '3'], True),
            ('one two\n3', ['one two', '3'], False),
            ('one two\n3', ['one', 'two', '3'], True),
        ],
    )
    def test_aslist(self, value, result, flatten):
        assert aslist(value, flatten) == result

    @pytest.mark.parametrize(
        'enum_type,value,result',
        [
            (Gender, 1, Gender.MALE),
            (Gender, '1', Gender.MALE),
            (Gender, 'male', None),
            (Gender, 'Male', None),
            (Gender, 'MALE', Gender.MALE),
            (Gender, 2, Gender.FEMALE),
            (Gender, '2', Gender.FEMALE),
            (Gender, 3, None),
            (Gender, 'UNKNOWN', None),
        ],
    )
    def test_asenum(self, enum_type, value, result):
        assert asenum(enum_type, value) == result

    def test_uuid_to_slug_and_back(self):
        from uuid import uuid4

        # working with 5 randomly generated uuid
        for _ in range(5):
            raw_value = uuid4()
            assert slug_to_uuid(uuid_to_slug(raw_value)) == raw_value

    def test_cannot_convert_invalid_slug_to_uuid(self):
        from uuid import uuid4

        slug = uuid_to_slug(uuid4())[:-4]
        with pytest.raises(ValueError):
            slug_to_uuid(slug)
