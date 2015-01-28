#!/usr/bin/env python
import os, sys
import cStringIO
import xml.etree.ElementTree as xml
import hashlib

def process(tree):
  root = xml.fromstring(tree)
  DD = root.find("Doc") # each tree only has one DD
  Props = DD.findall("./MetadataPT/Properties/PropertySet/Property")
  for p in Props:
    if p.get('name') == "ipid" and p.get('value') != None:
      IP = p.get('value')
    elif p.get('name') == "srccode" and p.get('value') != None:
      SourceC = p.get('value')
  MetaData = SourceC+"_"+IP
  for para in DD.getiterator("Para"): # search all <Para> nodes in layers
    value = para.text
    if value != None:
      HashKey = hashlib.md5(value.encode('utf8')).hexdigest()
      MapperOut = HashKey + "_" + MetaData + "\t" + value.encode('utf8')
      print MapperOut

def main():
  buff = None
  intext = False
  for line in sys.stdin:
    line = line.strip()
    if line.find("<Doc") != -1:
      intext = True
      Head = line.index("<Doc") # beginning of DD
      buff = cStringIO.StringIO()
      buff.write(line[Head:]) # excluding text before head tag
    elif line.find("</Doc>") != -1:
      intext = False
      Tail = line.index("</Doc>") # end of DD
      if buff != None:
        buff.write(line[:(Tail+10)]) # excluding junk after tail tag
        val = buff.getvalue()
        buff.close()
        buff = None
        process('<MR xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'+val+'</MR>')
    else:
      if intext:
        buff.write(line)

if __name__ == "__main__":
  main()
