from pylyric.influx import Influx

db = Influx(dbname="test")


def test_initialise():
    assert isinstance(db, Influx)


def test_write():
    print(db.write("lyric", outdoorTemperature=21.3, heating=True))


