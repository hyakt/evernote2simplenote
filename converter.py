# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser
import time
from datetime import datetime as dt
from simplenote import Simplenote

class EnexParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.text = ""
    def handle_starttag(self, tag, attrs):
        if tag == 'en-note':
            self.flag = True
    def handle_data(self, data):
        if self.flag:
            self.text = self.text + data + "\n"
    def handle_endtag(self, tag):
        if tag == 'en-note':
            self.flag = False

def parseNoteXML(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    notes = []
    note = {}
    for e in root.getiterator():
        if e.tag == 'title':
            note['title'] = e.text.encode('utf-8')
        elif e.tag == 'content':
            parser = EnexParser()
            parser.feed(e.text.encode('utf-8'))
            note['content'] = parser.text
        elif e.tag == 'created':
            note['created'] = e.text.encode('utf-8')
        elif e.tag == 'note':
            if note:
                notes.append(note)
                note = {}
    return notes

def makeContent(note,tags=['']):
    pattern = '%Y%m%dT%H%M%SZ'
    epoch = time.mktime(time.strptime(note['created'], pattern))
    d = dt.fromtimestamp(epoch)

    content = "** " + d.strftime('%Y-%m-%d') + " " + note['title'] + "\n\n " + note['content']
    return {"tags":tags, "content":content, "createdate": epoch}


def main():
    argvs = sys.argv
    argc = len(argvs)

    if not argc == 2:
        print 'Usage: # python %s filename' % argvs[0]
        quit()

    notes = parseNoteXML(argvs[1])

    print "simplenote address:"
    address = raw_input()
    print "simplenote password:"
    passwd = raw_input()

    sm = Simplenote(address, passwd)

    for note in notes:
        try:
            print note['title']
            sm.add_note(makeContent(note,['']))
        except:
            print "Wrong simplenote address or password."
            quit()

if __name__ == '__main__':
    main()
