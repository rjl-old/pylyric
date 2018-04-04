from pylyric.influx import Influx

i = Influx()


def test_initialise():
    assert isinstance(i, Influx)


def test_write():
    print(i.write("lyric", outdoorTemperature=21.3, heating=True))
