from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

# import bs4 as bs
import requests
import urllib
import urllib2,json

# user_input = raw_input("Some input please: ")

def search(requests,user_input):

	print "user_input:",user_input

	user_input = urllib.quote_plus(user_input)

	# source = urllib2.urlopen('https://www.googleapis.com/books/v1/volumes?q='+user_input+'+inauthor:keyes&key=AIzaSyC9pt3MZyxh8vvysP-VMacEaisuli2KyBg').read()
	source = urllib2.urlopen('https://www.googleapis.com/books/v1/volumes?q='+user_input).read()

	#soup = bs.BeautifulSoup(source,'lxml')

	data = json.loads(source)


	# print """info""",(data)

	# print type(data["items"])
	results = []
	# print len(data["items"])
	for d in range(len (data["items"])):
		# print "booooooooooook========",d
		booktitle=""
		booklanguage=""
		bookauthor=""
		bookImage=""
		bookDescription=""
		bookpublisher=""

		booktitle = data["items"][d]["volumeInfo"]["title"]
		booklanguage =data["items"][d]["volumeInfo"]["language"]
		bookauthor =""
		bauthorfirst= True
		# print data["items"][d]["volumeInfo"]["authors"]
		try:

			for a in data["items"][d]["volumeInfo"]["authors"]:
					if bauthorfirst:
						bauthorfirst = False

						bookauthor = bookauthor+a
					else:
						bookauthor = bookauthor+", "+a
		except:
			bookauthor =""

		# print "author--",bookauthor
		try:
			bookDescription =data["items"][d]["volumeInfo"]["description"]
		except:
			bookDescription =""

		try:
			bookpublisher =data["items"][d]["volumeInfo"]["publisher"]
		except:
			bookpublisher =""
		# bookpublisherISBIN =data["items"][d]["volumeInfo"]["industryIdentifiers"]
		bImage=False
		try:
		# print "Image-info",data["items"][d]["volumeInfo"]["imageLinks"]
			# print "inside booooooooooook========",d
		# print "Image==1",data["items"][d]["volumeInfo"]["imageLinks"]["smallThumbnail"]
		# print "Image==2",data["items"][d]["volumeInfo"]["imageLinks"]["thumbnail"]

			bookImage = data["items"][d]["volumeInfo"]["imageLinks"]["thumbnail"]
			bImage=True
			# print "imageLinks",bookImage
		except:
			bookImage = "--------------"
		bookwebReaderLink=data["items"][d]["accessInfo"]["webReaderLink"]

		# if user_input in bookauthor or user_input in booktitle :
		# print user_input,"===",booktitle

		found=False

		if user_input.lower() in booktitle.lower() or user_input.lower() in bookauthor.lower():
			found=True
			# subdata={'booktitle':booktitle,'booklanguage':booklanguage,'bookauthor':bookauthor,'bookImage':bookImage,'bookDescription':bookDescription,'bookpublisher':bookpublisher}
			print "found"
		else:
			print "not found "
		
			# subdata={'booktitle':booktitle,'booklanguage':booklanguage,'bookauthor':bookauthor,'bookImage':bookImage,'bookDescription':bookDescription,'bookpublisher':bookpublisher}
		# if user_input.lower() in bookauthor.lower() :
		# 	print "found in authors"
		# 	found=True
		# 	subdata={'booktitle':booktitle,'booklanguage':booklanguage,'bookauthor':bookauthor,'bookImage':bookImage,'bookDescription':bookDescription,'bookpublisher':bookpublisher}
		# else:
		# 	print "not found in authors"
			# subdata={'booktitle':booktitle,'booklanguage':booklanguage,'bookauthor':bookauthor,'bookImage':bookImage,'bookDescription':bookDescription,'bookpublisher':bookpublisher}
		if bImage and found :
			subdata={'booktitle':booktitle,'booklanguage':booklanguage,'bookauthor':bookauthor,'bookImage':bookImage,'bookDescription':bookDescription,'bookpublisher':bookpublisher}
			results.append(subdata)
	# print json.dumps(results)
	return HttpResponse(json.dumps(results),content_type="application/json")
