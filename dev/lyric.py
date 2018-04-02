from pylyric.lyric import Lyric
import pprint
pp = pprint.PrettyPrinter(indent=4)

client = Lyric()

# print(client.access_token)
# client.refresh_tokens()
#
# print(client.access_token)

# pp.pprint(client.locations)
device = client.devices(locationID=199754)[0]
pp.pprint(device.json)
print(device.operationStatus)


# print(client.device('LCC-00D02DB6B4A8'))

print(device.on(19))
# device.off()