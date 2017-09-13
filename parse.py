# 1. read xml file in (decompress if needed)
# 2. read all elemets out -> save to a file
# 3. show nesting level -> if nested and does not have any text -> don't show in tags with content
# 4. can location have multiple locations?
# 5. xmllint, https://wiki.libvirt.org/page/Common_XML_errors 
import xml.etree.ElementTree as ET
import datetime
import os
import sys

content = {}

def detect_root(tree):
	root = tree.getroot()
	return root

def read_tree(fileName):
	try:
		tree = ET.parse(fileName)
	except ET.ParseError as err:
		raise
	return tree

def detect_nested(disc):
	nested = []
	for elem in disc.iter():
		if elem.tag not in nested and len(list(elem)) > 0:
			nested.append(elem.tag)
	nested.remove(disc.tag)
	return nested

def has_text(elem):
	if not elem.text or not elem.text.strip():
		return False		 
	else:
		return True

def find_dicriminator(root):
	helper = {}
	# check for nestedness
	for item in root:
		if item.tag not in helper.keys():
			helper[item.tag] = 1
		else:
			helper[item.tag] += 1
	helper_nested = helper.copy()

	counter = 0
	for i in range(0, len(helper.keys())):
		for item in root.find(list(helper.keys())[i]):
			counter += 1
		helper_nested[list(helper.keys())[i]] = counter
	disc = max(value for value in helper_nested.values())
	for k,v in helper_nested.items():
		if v == disc:
			return root.find(k), v

def get_tags(element):
	notNestedTags = []
	nestedTags = []
	for item in element.iter():
		if has_text(item):
			notNestedTags.append(item.tag)
		else:
			nestedTags.append(item.tag)
	return set(notNestedTags), set(nestedTags)

def analyze_feed(fileName):
	tree = read_tree(fileName)
	root = detect_root(tree)
	disc, amountItems =  find_dicriminator(root)
	notNested, nested = get_tags(disc)
	# print("the root is {}".format(root.tag))
	print("this feed contains {} items".format(amountItems))
	# print("discriminator is: {}".format(disc.tag))
	print("this feed contains following fields:")
	for t in notNested:
		print("-",t)
	print("for more information on specific field use:\n python validate.py fileName fieldName False")

def collect_specified_tags(fileName, field):
	root = detect_root(read_tree(fileName))
	res = []
	for item in root.iter():
		if item.tag == field:
			res.append(item.text)
	return res

def count_unique_values(words):
	return {i:words.count(i) for i in set(words)}

def show_tag_info(fileName, field, save, outputFile=None):
	# show as many items as given
	res = collect_specified_tags(fileName, field)
	# show frequency for chosen tag
	freq = count_unique_values(res)
	for k,v in freq.items():
		print(k,":",v)

	f = os.path.splitext(fileName)[0]
	if save=="save":
		fileName = "{}.txt".format(outputFile)
		with open(fileName, "w") as w:
			for item in res:
				w.write(item)
				w.write('\n')

if __name__ == '__main__':
	pass
