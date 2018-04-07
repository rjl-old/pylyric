from pylyric.influx import Influx

db = Influx(db_name="test")


def test_initialise():
    assert isinstance(db, Influx)


def xtest_write():
    print(db.write("lyric", outdoorTemperature=21.3, heating=True))


