import pytest

from dataclasses import dataclass


@dataclass(slots=True)
class Data:
    x: int = 0
    y: int = 0


def test_data():
    data_1 = Data()
    data_2 = Data()

    data_1.x = 2

    with pytest.raises(AttributeError):
        data_1.z = 3

    # Update on 'data_1' does not affect 'data_1'
    assert data_2.x != data_1.x


if __name__ == '__main__':
    pytest.main([__file__])
