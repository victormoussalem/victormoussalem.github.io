import simplejson as json
from flask import jsonify
import urllib2
import urllib
import jsonpath
from app import *

TEST_API_KEY = 'f247296fc35c9f7acadb3551b4c612a2'

API_BASE_URL = "http://api.crunchbase.com/"
API_VERSION = "2"
API_URL = API_BASE_URL + "v" + "/" + API_VERSION + "/"

companies = ["Facebook", "Google", "Apple", "Microsoft", "Yahoo", "Dropbox", "Twitter", "Box", "Amazon", "Linkedin" ]

def __webRequest(url):
    try:
      response = urllib2.urlopen(url)
      result = response.read()
      return result
    except urllib2.HTTPError as e:
      raise Exception

def __getJsonData2(namespace, query=""):
    url = API_URL + namespace + "?user_key=" + TEST_API_KEY + query
#    print url
    response_dict = json.loads(__webRequest(url))
    return response_dict

def getOrganizationData(permalink):
    result = __getJsonData2("organization/" + permalink)
    return result

def getCompetitorsData(permalink):
    result = __getJsonData2("organization/" + permalink + "/competitors/")
    return result

def getCategoriesData(permalink):
    result = __getJsonData2("organization/" + permalink + "/categories/")
    return result

def getAcquisitionsData(permalink):
    result = __getJsonData2("organization/" + permalink + "/acquisitions/")
    return result

def getInvestmentsData(permalink):
    result = __getJsonData2("organization/" + permalink + "/investments/")
    return result

def getProductsData(permalink):
    result = __getJsonData2("organization/" + permalink + "/products/")
    return result

def getFundingRoundData(path):
    result = __getJsonData2(path)
    return result

def getNewsData(permalink):
    result = __getJsonData2("organization/" + permalink + "/news/")
    return result

def getFoundersData(permalink):
    result = __getJsonData2("organization/" + permalink + "/founders/")
    return result

def getAllOrganizations():
    result = __getJsonData2("organizations")
    return result

def getAcquisitionData(path):
    result = __getJsonData2(path)
    return result

"""
customResponse = getAllOrganizations()
allCompanies = list()
#nameLength = int(customResponse["data"]["items"][].length)

#print nameLength

for x in range(0, 1000):
	allCompanies.append(json.dumps(customResponse["data"]["items"][x]["name"]))

allStrippedCompanies = list()

for x in allCompanies:
	x = x[1:-1]
	print x
	allStrippedCompanies.append(x)
"""

def createCompany(x):
	#TODO add if statements to find keys (for example: funding_rounds for google and facebook, but funding_rounds for apple. also, not all companies have the same fields
	response = getOrganizationData(x)

	#print json.dumps(response, sort_keys=True, indent=4)

	#uuid
#	uuid = str(json.dumps(response["data"]["uuid"]))

	#permalink
#	permalink = json.dumps(response["data"]["properties"]["permalink"])

	#name
#	name = json.dumps(response["data"]["properties"]["name"])

	#homepage_url
#	homepage_url = json.dumps(response["data"]["properties"]["homepage_url"])
#	print homepage_url
	#description
#	description = json.dumps(response["data"]["properties"]["description"])

	#founded_day
#	founded_day = json.dumps(response["data"]["properties"]["founded_on_day"])

	#founded_month
#	founded_month = json.dumps(response["data"]["properties"]["founded_on_month"])

	#founded_year
#	founded_year = json.dumps(response["data"]["properties"]["founded_on_year"])

#	company = models.Company(uuid=uuid, permalink=permalink, name=name, homepage_url=homepage_url, description=description, founded_day=founded_day, founded_month=founded_month, founded_year=founded_year)
	company = models.Company(dict=response)

	#founders

	#TODO organize funding_rounds appropriately. it's currently just in json format
#	if (json.dumps(response["data"]["relationships"].get("funding_rounds")==True)):
#		funding_rounds = json.dumps(response["data"]["relationships"]["funding_rounds"])
#	else:
#		funding_rounds = json.dumps(response["data"]["relationships"]["funding_round"])

	#acquisitions
	#acquisitions = json.dumps(response["data"]["relationships"]["acquisitions"])

	"""
	for l,a in response:
		if l == "acquisitions":
			acquisitions_url = json.dumps(l["paging"]["first_page_url"])
			numAcquisitions = int(json.dumps(l["acquisitions"]["paging"]["total_items"]))
			acquisitions_reponse = getAcquisitionsData(x)
			acquisitions = list()
		elif isinstance(a, dict):
	"""			


	acquisitions_url = json.dumps(response["data"]["relationships"]["acquisitions"]["paging"]["first_page_url"])
	numAcquisitions = int(json.dumps(response["data"]["relationships"]["acquisitions"]["paging"]["total_items"]))
	acquisitions_response = getAcquisitionsData(x)
	acquisitions = list()
	acqui = {}

	for i in range(0, numAcquisitions):
		acqui = acquisitions_response["data"]["items"][i]["path"]
		acquisition_response = getAcquisitionData(acqui)
		acquisitions.append(json.dumps(acquisition_response["data"]["relationships"]["acquiree"]["items"][0]["name"]))
		#print (acquisition_response["data"]["relationships"]["acquiree"]["items"][0]["name"])

	#Parse for just the third word (name of acquisition)

	#	for i in range(0, numAcquisitions):
	#		acq = acquisitions_response["data"]["items"][i]["name"]
	#		if acq != "Acquisition":
	#			acq = acq.split(' ', 2)[2]
	#		acquisitions.append(acq)

	for a in acquisitions:
		company.aq.append(a)

	#competitors
	#extract list of competitors
	competitors_url = json.dumps(response["data"]["relationships"]["competitors"]["paging"]["first_page_url"])
	numCompetitors = int(json.dumps(response["data"]["relationships"]["competitors"]["paging"]["total_items"]))
	competitors_response = getCompetitorsData(x)
	competitors = list()

	for i in range(0, numCompetitors):
		competitors.append(competitors_response["data"]["items"][i]["name"])

	#categories
	categories_url = json.dumps(response["data"]["relationships"]["categories"]["paging"]["first_page_url"])
	numCategories = int(json.dumps(response["data"]["relationships"]["categories"]["paging"]["total_items"]))
	categories_response = getCategoriesData(x)
	#markets = json.dumps(response["data"]["relationships"].get("markets"))
	categories = list()

	for i in range(0, numCategories):
		categories.append(categories_response["data"]["items"][i]["name"])

	for m in categories:
		company.ct.append(m)

	#investments
	#investments = json.dumps(response["data"]["relationships"].get("investments"))
	#TODO also pull out investment round for each investment
	"""
	investments_url = json.dumps(response["data"]["relationships"]["investments"]["paging"]["first_page_url"])
	numInvestments = int(json.dumps(response["data"]["relationships"]["investments"]["paging"]["total_items"]))
	investments_response = getInvestmentsData(x)
	investments = list()
	fundingRoundPath = list()
	
	if (investments is not None):
		for i in range(0, numInvestments):
			investments.append(investments_response["data"]["items"][i]["invested_in"]["name"])
			fundingRoundPath.append(investments_response["data"]["items"][i]["funding_round"]["path"])
	"""
	#TODO fix this later, keep out for now
	"""	
		for path in fundingRoundPath:
			if(getFundingRoundData(path)):
				fundingRoundPath_response = getFundingRoundData(path)
				numInvestments = int(json.dumps(fundingRoundPath_response["data"]["relationships"]["investments"]["paging"]["total_items"]))
			#TODO get funding_type, date, name, etc.
	"""

	#founders
	founders = list()
	founders_url = json.dumps(response["data"]["relationships"]["founders"]["paging"]["first_page_url"])
	numFounders = int(json.dumps(response["data"]["relationships"]["founders"]["paging"].get("total_items")))
	founders_response = getFoundersData(x)

	for i in range(0, numFounders):
		founders.append(founders_response["data"]["items"][i]["name"])

	for f in founders:
		company.fd.append(f)

	#TODO now that I have recursive iteration over JSON nested fields working, loop through to find the Products key, then loop through the fields "url" "name" etc within that key to find the below parameters
	#products
	products = list()
	products_url = json.dumps(response["data"]["relationships"]["products"]["paging"]["first_page_url"])
	numProducts = int(json.dumps(response["data"]["relationships"]["products"]["paging"]["total_items"]))
	products_response = getProductsData(x)

	for i in range(0, numProducts):
		products.append(products_response["data"]["items"][i]["name"])

	for p in products:
	#	product = models.Product(name=p)
		company.pd.append(p)

	#press
	news = list()
	news_url = json.dumps(response["data"]["relationships"]["news"]["paging"]["first_page_url"])	
	numArticles = int(json.dumps(response["data"]["relationships"]["news"]["paging"]["total_items"]))
	news_response = getNewsData(x)

	#TODO Take care of case where numArtciles is greater than 1000 (Limit per page)
	"""
		for i in range(0, numArticles):
			article_url = press_response["data"]["items"][i]["url"]
			print article_url
			article_title = press_response["data"]["items"][i]["title"]
			print article_title
			article_date = press_response["data"]["items"][i]["posted_on"]
			print article_date
		#	print article_url + " " + article_title + " " + article_date
	"""

	#ipo
	#TODO convert from json to organized format
	ipo = json.dumps(response["data"]["relationships"].get("ipo"))

	#TODO insert functions to access companies (get), delete

	db.session.add(company)
	db.session.commit()

	#insert everything into database
#	company = models.Company(uuid=uuid, permalink=permalink, name=name, homepage_url=homepage_url, description=description, founded_day=founded_day, founded_month=founded_month, founded_year=founded_year, acquisitions="acquisitions", markets="markets", investments="investments", founders="founders", ipo="ipo")
#	company = models.Company(name = "Facebook")
#	db.session.add(company)
#db.session.commit()
"""
for y in allStrippedCompanies:
	createCompany(y)
"""
for x in companies:
	createCompany(x)

users =  models.Company.query.all()
for u in users:
	print u.id, u.name, u.founded_on_year, u.aq
