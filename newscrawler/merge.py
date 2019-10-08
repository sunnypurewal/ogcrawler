import os
import json
import random

allobjects = []
for filename in os.listdir("../data/urlsets"):
  path = f"../data/urlsets/{filename}"
  with open(path, "r") as f:
    line = f.readline()
    while (len(line) != 0):
      try:
        j = json.loads(line)
        allobjects.append(j)
      except:
        pass
      finally:
        line = f.readline()

random.shuffle(allobjects)

with open("../data/recent.urlset", "w") as f:
  for obj in allobjects:
    try:
      json.dump(obj, f)
      f.write("\n")
    except:
      pass