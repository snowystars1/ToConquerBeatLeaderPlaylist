PATH_TO_BEAT_SABER_PLAYLISTS="C:\\Users\\Chris\\BSManager\\BSInstances\\1.39.1\\Playlists"

from os import getcwd
from os.path import join
from json import load, dump
import requests

def main():
    # Query top 100 LUCK leaderboards that are closest to being conquered.
    url = "https://api.beatleader.com/clan/LUCK/maps?page=1&count=100&sortBy=toconquer&leaderboardContext=general&order=desc&playedStatus=any"
    response = requests.get(url)


    # Parse json response if it was received successfully.
    if response.status_code == 200:
        queryResponseJson = response.json()

        playlist = join(PATH_TO_BEAT_SABER_PLAYLISTS, "LUCKToConquer.bplist")

        playlistTitle = "LUCKToConquer"
        playlistAuthor = "LUCK"

        # Being writing a new playlist file.
        with open(playlist, "w", encoding="utf-8") as playlist:
            fullplaylistJson = {}

            fullplaylistJson["playlistTitle"] = playlistTitle
            fullplaylistJson["playlistAuthor"] = playlistAuthor
            fullplaylistJson["songs"] = []

            # Parse out the important fields from the query response and store those
            # in a JSON format that will be readable by BS as a playlist.
            print("parsing fields...")     
            for entry in queryResponseJson["data"]:
                songName = entry["leaderboard"]["song"]["name"]
                levelAuthorName = entry["leaderboard"]["song"]["mapper"]
                hash = entry["leaderboard"]["song"]["hash"]
                levelid = "custom_level_" + hash

                characteristic = entry["leaderboard"]["difficulty"]["modeName"]
                name = entry["leaderboard"]["difficulty"]["difficultyName"]

                difficulties = {}
                difficulties["characteristic"] = characteristic
                difficulties["name"] = name

                songDict = {}
                songDict["songName"] = songName
                songDict["levelAuthorName"] = levelAuthorName
                songDict["hash"] = hash
                songDict["levelid"] = levelid
                songDict["difficulties"] = [difficulties]
                
                fullplaylistJson["songs"].append(songDict)
                print(f"parsed song: {songName}")

            print("dumping...")        
            dump(fullplaylistJson, playlist, indent=3)
    else:
        print("Failed to query BL API for LUCK Conquerable maps! There might be internet connectivity issues!")

# Main
if __name__ == "__main__":
    main()