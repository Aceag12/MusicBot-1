import urllib.request, json
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
		charstring += "*Official Link:* https://www.achaea.com/game/honours/" + name
		
		return charstring
	except urllib.error.HTTPError as e:
		err = urlerr(e)
		return err
		#print("Error: " + str(e.code) + " (" + e.reason + ")")
	#with urllib.request.urlopen(url) as get:
		#print("test")
		#data = json.loads(get.read().decode())
		#print(data)


#get_achaea_who()
#print(get_achaea_who_details("samakhulis"))

