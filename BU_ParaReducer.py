#!/usr/bin/env python
from operator import itemgetter
import sys

ParaCount = {}#key - paragraph hash key, value - aggregated count of hash key
ParaText = {}#key - paragraph hash key (same as above), value - para text
ParaMeta = {}

for line in sys.stdin:
  line = line.strip()
  try:
    keyMeta, para = line.split("\t", 1)
  except ValueError:
    pass
  else:
    key, IP, SC = keyMeta.split("_", 2)
    try:
      ParaCount[key] = ParaCount[key] + 1
      ParaMeta[key].append(IP)
      ParaMeta[key].append(SC)
    except:
      ParaCount[key] = 1
      ParaText[key] = para
      ParaMeta[key] = [IP, SC]
sortBYvalue = sorted(ParaCount.iteritems(), key=itemgetter(1))
for pair in sortBYvalue:
  if pair[1] > 9:
    print "%s\t%s\t%s\t%s" % (pair[0],pair[1],ParaText[pair[0]],set(ParaMeta[pair[0]]))
