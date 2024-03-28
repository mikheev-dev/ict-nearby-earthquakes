from typing import List, Type, Dict

import pytest
import uuid

from src.utils.squeezing_strategies import OnlyOneSqueezingStrategy


def assert_eq_arrays(l: List, r: List):
    assert sorted(l, key=lambda x: (x.key, x.value)) == sorted(r, key=lambda x: (x.key, x.value))


class DataForTest:
    value: int
    key: str

    def __init__(self, key: str, value: int):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"key={self.key},value={self.value}"


MOD_NUMBER = 10
SIZE_OF_INPUT_DATA = MOD_NUMBER * 10


class TestOnlyOneSqueezingStrategy:
    __strategy = OnlyOneSqueezingStrategy(field_to_squeeze_on='value')

    @staticmethod
    def _gen_input_data(
            t: Type[Dict] | Type[DataForTest],
            gen_equal_values: bool = False
    ) -> List:
        data = []
        mod_value = SIZE_OF_INPUT_DATA if not gen_equal_values else MOD_NUMBER
        for idx in range(SIZE_OF_INPUT_DATA):
            key = str(uuid.uuid4())
            value = idx % mod_value
            data.append(t(key=key, value=value) if t == DataForTest else {key: value})
        return data

    def test_correct_data_different_values(self):
        data = self._gen_input_data(DataForTest, gen_equal_values=False)
        squeezed = self.__strategy.squeeze(data)

        assert len(squeezed) == len(data)
        assert_eq_arrays(squeezed, data)

    def test_correct_data_equal_values(self):
        data = self._gen_input_data(DataForTest, gen_equal_values=True)
        squeezed = self.__strategy.squeeze(data)

        assert len(squeezed) != len(data)
        assert len(squeezed) == MOD_NUMBER

        assert_eq_arrays(
            data[:MOD_NUMBER],
            squeezed,
        )

    def test_empty_data(self):
        data = []
        squeezed = self.__strategy.squeeze(data)

        assert len(squeezed) == 0

    def test_invalid_data(self):
        data = self._gen_input_data(t=dict)
        with pytest.raises(
                Exception,
                match="Can't squeeze list, no field value of instances inside the list."
        ):
            self.__strategy.squeeze(data)




