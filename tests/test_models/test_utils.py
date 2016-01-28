from qsardb.models.utils import ModelMixin
import pytest

@pytest.mark.parametrize('repr_props, props, expected', [
    ([], {}, '<TestModel()>'),
    ([], {'test1': 'value1'}, '<TestModel()>'),
    (['test2'], {}, '<TestModel(test2=\'None\')>'),
    (['test3'], {'test3': 'value3'}, '<TestModel(test3=\'value3\')>'),
    (['test4', 'test5'], {'test4': 'value4', 'test5': 'value5'}, '<TestModel(test4=\'value4\', test5=\'value5\')>'),
    (['test6', 'test7'], {'test7': 'value7', 'test8': 'value8'}, '<TestModel(test6=\'None\', test7=\'value7\')>')
])
def test(repr_props, props, expected):
    class TestModel(ModelMixin):
        __repr_props__ = repr_props

        def __init__(self, props):
            self.__dict__.update(props)
    assert repr(TestModel(props)) == expected
