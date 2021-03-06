
# X - Plex - Token = y9pLd6uPWXpwbw14sRYf
# http://plex.colarietitosti.info/library/sections/2/all?X-Plex-Token=y9pLd6uPWXpwbw14sRYf
# http://plex.colarietitosti.info/library/sections?X-Plex-Token=y9pLd6uPWXpwbw14sRYf
import xml.etree.ElementTree as ET
import requests
from collections import defaultdict
from json import load, dump

from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer



token = "y9pLd6uPWXpwbw14sRYf"
plexurl = "http://plex.colarietitosti.info:32400"
"""
plex = PlexServer(plexurl, token)

#client = plex.client("Plex Client")

section = plex.library.section('Music')
tracks = section.searchArtists()[0]
#print(section.searchTracks())

#client = plex.client(section)

print(tracks.key)
print(tracks.title)
"""
def json_save(data, fname):
    with open(fname, 'w') as fp:
        dump(data, fp)


def get_tokenized_uri(uri):
    return plexurl+uri+token


xml = requests.get(get_tokenized_uri("/library/sections")).text
root = ET.fromstring(xml)
artisturi = ""
for child in root:
    if "music" in child.attrib["title"].lower():
        artisturi = get_tokenized_uri("/library/sections/"+child.attrib["key"]+"/all")
        # print(musicuri)
        # print(child.attrib)

xml = requests.get( artisturi ).text
root = ET.fromstring(xml)
artists = defaultdict(list)
albums = defaultdict(list)
titles = defaultdict(list)
count = 0
songs = {}
for artist in root:
    songs[artist.get("title")] = {}
    artist_uri = get_tokenized_uri(artist.get("key"))
    plexalbums = ET.fromstring( requests.get( artist_uri ).text)
    for album in plexalbums:
        songs[artist.get("title")][album.get("title")] = []
        album_uri = get_tokenized_uri(album.get("key"))
        plexsongs = ET.fromstring(requests.get(album_uri).text)
        for songmeta in plexsongs:
            song_uri = get_tokenized_uri(songmeta.get("key"))
            song = ET.fromstring(requests.get(song_uri).text)
            for p in song.iter("Part"):
                title = songmeta.get("title")
                file = get_tokenized_uri(p.get("key"))
                songs[artist.get("title")][album.get("title")].append([title, file])
                # print(songs)
                # albums[album.get("title")].append(file)
                # artists[artist.get("title")].append(file)
                # titles[song.get("title")].append(file)
                print("""%d 
%s -- %s 
%s
                  
                """ % (count, artist.get("title"), album.get("title"), title))
                count += 1
                if count % 2000 == 0:
                    print("+ 2000")
                elif count % 100 == 0:
                    print(".", end="")

json_save(songs, "data.json")
        #print(album.items())

#print(xml)


#print(root.attrib)
#print(type(root))