import requests
import re
import sys
import codecs

count = 0

def handle_items(items, url):
	for item in items:
		item_url = url + "/%s" % (item)
		r = requests.get(item_url)
		if r.status_code == 200:
			fp = open("%s.html"%(item),'wb')
			fp.write(r.text.encode('utf-8'))
			fp.close()
			global count
			count += 1


def handle_store(url,fp):

	all = "/category/ALL"
	store_url = url + all

	item_req = requests.get(store_url)
	fp.write(item_req.text.encode('utf-8'))
	if item_req.status_code == 200:
		item_body = item_req.text
		item_search = re.findall(r'[A-Z]{2}[0-9]{6}',item_body)
		items = list(set(item_search))
		print("Length of Item List: %s" % (str(len(items))))
		handle_items(items, url)



def main():
	fp = open("output.txt","wb")
	starting_url = "http://bidfta.com/search?utf8=%E2%9C%93&keywords=&search%5Btagged_with%5D=&location=Columbus%2C+Oh&seller=&button="

	r = requests.get(starting_url)
	if r.status_code == 200:
		body = r.text
		store_search = re.finditer(r'(http://bid.bidfta.com/cgi-bin/mndetails.cgi?(.*))\"\s',body)
		url_list = []
		for k in store_search:
			url = re.sub(r'mndetails','mnlist',k.group(1))
			url_list.append(url)
		print("Length of Store List: %s" % (str(len(url_list))))
		for url in url_list:
			handle_store(url,fp)



if __name__ == '__main__':
	main()