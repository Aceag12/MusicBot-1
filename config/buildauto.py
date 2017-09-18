#!/bin/python
import os

files = []
open("./autoplaylist.txt","w").close()
file1 = open("./autoplaylist.txt","a")
for file in os.listdir("./pls"):
	if file.endswith(".txt"):
		with open(os.path.join("./pls",file),"r") as textfile:
			for line in textfile.readlines():
				file1.write(line)
			textfile.close

file1.close
				
			
