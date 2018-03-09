from pylyric.lyric import Lyric

client = Lyric()

# print(client.access_token)
# client.refresh_tokens()
#
# print(client.access_token)

client.get_tokens()