'''A simplified knowledge base with just
links between entities and labels'''

__author__ = "Jonathan Lajus"

def load(fileName, container, reverseContainer = None):
    with open(fileName, encoding="utf-8") as file:
        print("Loading",fileName,end="...",flush=True)
        for line in file:
        	splitLine = line.split('\t')
        	#print("splitline", splitLine)
        	if len(splitLine) is not 2:
        		raise RuntimeError('The file is not a valid KB file')
        	subject = splitLine[0]
        	#print("subject", subject)
        	obj = splitLine[1].strip('"\n')
        	#print("object", obj)
        	container.setdefault(subject, set()).add(obj)
        	if reverseContainer != None:
        		reverseContainer.setdefault(obj, set()).add(subject)
        print("done", flush=True)

class SimpleKB:
    def __init__(self, yagoLinksFile, yagoLabelsFile):
        self.links = {}
        self.labels = {}
        self.rlabels = {}
        load(yagoLinksFile, self.links, self.links)
        load(yagoLabelsFile, self.labels, self.rlabels)

    def __str__(self):
    	return 'SimpleKB: "'+str(self.links)+"/ " + str(self.labels)+ "/ "+ str(self.rlabels)



