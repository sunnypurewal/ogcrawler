import os
import sys
import shutil
import json

sys.path.append("newscrawler/spiders")

def main(domainsfile):
  with open(domainsfile, "r") as f:
    domains = json.loads(f.read())
    print (len(domains["domains"]["politics"]))

if __name__ == "__main__":
    main(sys.argv[1])
