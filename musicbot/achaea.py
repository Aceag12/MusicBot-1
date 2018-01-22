import urllib.request, json
#import pprint
import datetime
from PIL import Image
from io import BytesIO

class Achaea:
    def urlerr(e):
        return "Error: " + str(e.code) + " (" + e.reason + ")"

    def get_who():
        url = "https://www.achaea.com/api/characters.json"
        try:
            data = json.loads(urllib.request.urlopen(url).read().decode())
            name_list = ""
            for value in data["characters"]:
                if name_list == "":
                    name_list = value["name"]
                else:
                    name_list = name_list + ", " + value["name"]

            #print(name_list)
            #print("\nTry out AWHO <name> for character details")
            return name_list
        except urllib.error.HTTPError as e:
            err = urlerr(e)
            return err
            #print("Error: " + str(e.code) + " (" + e.reason + ")")

    def get_who_details(name):
        url = "https://www.achaea.com/api/characters/" + name + ".json"
        try:
            char = json.loads(urllib.request.urlopen(url).read().decode())
            charstring = "**Name:** " + char["fullname"] + "\n**City:** " + char["city"] + "\n"
            charstring += "**House:** " + char["house"] + "\n**Level:** " + char["level"] + " (*Rank " + char["xp_rank"] + "*)\n"
            charstring += "**Explorer Rank:** " + char["explorer_rank"] + "\n" 
            charstring += "**Mobs/Players Killed:** " + char["mob_kills"] + "/" + char["player_kills"] + "\n"
            charstring += "*Official Link:* <https://www.achaea.com/game/honours/" + name + ">\n"
            
            return charstring
        except urllib.error.HTTPError as e:
            err = urlerr(e)
            return err
            #print("Error: " + str(e.code) + " (" + e.reason + ")")
        #with urllib.request.urlopen(url) as get:
            #print("test")
            #data = json.loads(get.read().decode())
            #print(data)

    def get_banner(name):
        url = "https://www.achaea.com/banner/" + name + ".jpg"
        try:
            with urllib.request.urlopen(url) as bannerReq:
                with open('audio_cache/banner.jpg','wb') as f:
                    f.write(bannerReq.read())
            
            return 'audio_cache/banner.jpg'
        except urllib.error.HTTPError as e:
            err = urlerr(e)
            return err
            
    #get_achaea_who()
    #print(get_achaea_who_details("samakhulis"))

    def get_news(channame="",channum=""):
        url = "https://www.achaea.com/api/news"
        if channame == "":
            url += ".json"
            type = 0 # Channel list only
        else:
            url += "/" + channame.lower()
            if channum == "":
                url += ".json"
                type = 1
            else:
                url += "/" + str(int(channum)) + ".json"
                type = 2
        try:
            if type == 0:
                print("Parsing " + url)
                posts = json.loads(urllib.request.urlopen(url).read().decode())
                chan_list = ""
                for value in posts:
                    if chan_list == "":
                        chan_list = value["name"]
                    else:
                        chan_list += ", " + value["name"]
                return "__**Channel list:**__\n```" + chan_list + "```"
            elif type == 1:
                url_pc = "https://www.achaea.com/api/news.json"
                chans = json.loads(urllib.request.urlopen(url_pc).read().decode())
                ischan = False
                post_num = 0
                chan_name = ""
                for clval in chans:
                    if clval["name"].lower() == channame.lower(): # Validate this channel.
                        ischan = True
                        post_num = clval["total"]
                        chan_name = clval["name"]
                        page = post_num/26
                        if page < 1:
                            page = 0 # The API will take a float and properly display stuff except when page < 1.0
                        url += "?page=" + str(page)
                        #print(post_num_fmt.format(post_num,page))
                        break

                if ischan:
                    print("Parsing " + url)
                    posts = json.loads(urllib.request.urlopen(url).read().decode())
                    #pp = pprint.PrettyPrinter(depth=6)
                    #pp.pprint(posts)
                    post_list = ""
                    for value in posts["news"]:
                        if post_list == "":
                            post_list = "**" + str(value["id"]) + "** *(" + value["from"] + ")*: " + value["subject"]
                        else:
                            post_list += "\n**" + str(value["id"]) + "** *(" + value["from"] + ")*: " + value["subject"]
                            
                    return "__**Recent " + chan_name + "" + " posts**__\n\n" + post_list + ""
                else:
                    return "Invalid channel name"
            elif type == 2:
                print("Parsing " + url)
                post = json.loads(urllib.request.urlopen(url).read().decode())
                post_str = "__**" + post["post"]["subject"] + " *(" + post["post"]["section"] + " " + str(post["post"]["id"]) + ")***__\n***From: " + post["post"]["from"] + "***\n***To: " + post["post"]["to"] + "***\n***Date: " + datetime.datetime.fromtimestamp(post["post"]["date"]).strftime("%Y-%m-%d %H:%M:%S") + "***\n" + post["post"]["message"]
                return post_str
        except urllib.error.HTTPError as e:
            err = urlerr(e)
            return err