
import datetime, json, time, heapq, random
import pandas as pd
import dateutil.parser

#### A data set in an epoch
class dataSet:
	def __init__(self):
		# self.data = pd.dataframe()
		self.totalSpending = dict()
		self.totalImageUpload = dict()
		self.totalVisit = dict()
		self.firstAppear = dict()
		self.lastRecordTime = None

#### Ingest every event according to its type. Take O(1) time
def Ingest(e, D):
	if type(e) is str: new_event = json.loads(e)
	else: new_event = e

	now_time = dateutil.parser.parse(new_event['event_time'])
	if D.lastRecordTime:
		D.lastRecordTime = now_time if now_time > D.lastRecordTime else D.lastRecordTime
	else:
		D.lastRecordTime = now_time

	if new_event['type'] == 'CUSTOMER':
		customerID = new_event['key']
		if customerID not in D.firstAppear:
			D.totalVisit[customerID] = 0
			D.totalImageUpload[customerID] = 0
			D.totalSpending[customerID] = 0.0
			D.firstAppear[customerID] = now_time

	else:
		customerID = new_event['customer_id']

		# In case of the missing of "CUSTOMER" event, create the customer profile once the first event of his/her appears
		if customerID not in D.firstAppear:
			D.totalVisit[customerID] = 0
			D.totalImageUpload[customerID] = 0
			D.totalSpending[customerID] = 0.0
			D.firstAppear[customerID] = now_time

		if new_event['type'] == 'SITE_VISIT':
			D.totalVisit[customerID] += 1
		elif new_event['type'] == 'IMAGE':
			D.totalImageUpload[customerID] += 1
		elif new_event['type'] == 'ORDER':
			D.totalSpending[customerID] += float(new_event['total_amount'].split(" ")[0])

#### Calculate how long the customer has been on our platform, in weeks. Take O(1) time
def WeekDifference(start, end):
    assert start <= end
    start_year, start_week, start_dayofweek = start.isocalendar()
    end_year, end_week, end_dayofweek = end.isocalendar()
    return ((end_year - start_year) * 52) + (end_week - start_week) + (end_dayofweek - start_dayofweek)/7.0

#### Calaulate visit/week for requested customer. Take O(1) time
def AvgWeeklyVisit(customerID, D):

	customerDatedLifeSpan = WeekDifference(D.firstAppear[customerID], D.lastRecordTime)
	if customerDatedLifeSpan == 0 and D.totalVisit[customerID] == 0: return 0.0
	elif customerDatedLifeSpan == 0 and D.totalVisit[customerID] > 0: return float(D.totalVisit[customerID])
	else: return D.totalVisit[customerID]/customerDatedLifeSpan

#### Calculate how much he/she spends averagely per visit. Take O(1) time
def AvgExpenditurePerVisit(customerID, D): 

	if D.totalVisit[customerID] == 0 and D.totalSpending[customerID] == 0: return 0
	elif D.totalVisit[customerID] == 0 and D.totalSpending[customerID] !=0:
		print "A SITE_VISIT event might be missing."
		return D.totalSpending[customerID]
	return float(D.totalSpending[customerID])/D.totalVisit[customerID]


#### Calculate his/her weekly average expenditure. Take O(1) time
def AvgWeeklyExpenditure(customerID, D):
	return AvgExpenditurePerVisit(customerID, D)*AvgWeeklyVisit(customerID, D)


'''
Find top x greatest Simple LTV customers among n customers. Time: O(n + xlogn), Space: O(n + x) 
Assumptions:
1. The time span of D is within all customers recorded's 10 year life span
2. Week is define is length instead of in real calendar week.
3. Customer whose recorded events have the span shorter than 1 day and has the total perchase of x dollars, will have the weekly expenditure of x
'''
def TopXSimpleLTVCustomers(x, D):

	heap = [ (-AvgWeeklyExpenditure(customerID, D), customerID) for customerID, spending in D.totalSpending.iteritems()]
	heapq.heapify(heap)
	TopSpending = list()
	x = x if x <= len(D.totalSpending) else len(D.totalSpending)

	for i in range(x):
		negSpending, customerID = heapq.heappop(heap)
		TopSpending.append((-negSpending, customerID))

	TopSimpleLTV = list()
	for AvgWExp, customerID in TopSpending:
		customerSimpleLTV = AvgWExp*52*10
		TopSimpleLTV.append((customerID, customerSimpleLTV))

	return TopSimpleLTV

'''
Create simulated input for the sake of this coding challenge. 
Assumptions:
1. Every 'IMAGE', 'ORDER' event comes after a 'SITE_VISIT' event
2. Time span only from 2006.1.1 - 2017.12.28
3. Day generator could only generate day from 1 - 28 every month for simplicity.

Default:
1. 300 events
2. 10 total customers
'''
def inputGenerator(eventCounts= 300, totalCustomer = 10):
	events = list()

	for i in xrange(eventCounts):
		# random.seed() 
		year = random.randint(2006, 2017)
		month = random.randint(1, 12)
		day = random.randint(1, 28)
		hour = random.randint(0,23)
		m = random.randint(0,59)
		sec = random.randint(0,59)
		eventTime = datetime.datetime(year, month, day, hour, m, sec)

		eventType = random.choice(['CUSTOMER', 'SITE_VISIT', 'IMAGE','ORDER'])
		# eventType = random.choice(['CUSTOMER'])
		if eventType == 'CUSTOMER':
			event = {'type': eventType,
					'verb': random.choice(['NEW','UPDATE']),
					'key': random.randint(0, totalCustomer),
					'event_time': eventTime.isoformat(),
					'last_name': None,
					'adr_city': None
			}
			events.append(event)
		elif eventType == 'SITE_VISIT':
			event = {'type': eventType,
					'verb': 'NEW',
					'key': None,
					'event_time': eventTime.isoformat(),
					'customer_id': random.randint(0, totalCustomer),
					'tags': list()
			}
			events.append(event)
		elif eventType == 'IMAGE':
			customerID = random.randint(0, totalCustomer)
			visitEvent = {'type': 'SITE_VISIT',
						'verb': random.choice(['NEW','UPDATE']),
						'key': None,
						'event_time': eventTime.isoformat(),
						'customer_id': customerID,
						'tags': list()
			}
			events.append(visitEvent)

			imageEventTime = eventTime + datetime.timedelta(minutes = 10)
			imageEvent = {'type': 'IMAGE',
						'verb': 'UPLOAD',
						'key': None,
						'event_time': imageEventTime.isoformat(),
						'customer_id': customerID,
						'camera_make': None,
						'camera_model': None
			}
			events.append(imageEvent)

		elif eventType == 'ORDER':
			customerID = random.randint(0, totalCustomer)
			visitEvent = {'type': 'SITE_VISIT',
						'verb': random.choice(['NEW','UPDATE']),
						'key': None,
						'event_time': eventTime.isoformat(),
						'customer_id': customerID,
						'tags': list()
			}
			events.append(visitEvent)

			orderEventTime = eventTime + datetime.timedelta(minutes = 10)
			dollar = random.randint(1,100)
			cent = random.randint(0,99)
			cost_str = str(dollar) + "." + str(cent) + " USD"
			
			orderEvent = {'type': 'ORDER',
						'verb': random.choice(['NEW','UPDATE']),
						'key': None,
						'event_time': orderEventTime.isoformat(),
						'customer_id': customerID,
						'total_amount': cost_str
			}
			events.append(orderEvent)
		else:
			print "Unrecognized event type: ", eventType

	return events

#### Assign parameters
eventCounts = 3000
customerCounts = 1000

#### Genearte simulated input events
testInput = inputGenerator(eventCounts, customerCounts)

#### Write it into a txt file as give on github
with open('input.txt', 'w') as outfile:
    json.dump(testInput, outfile)

#### Read the simulated input file
with open('input.txt') as infile:
	inputEvents = json.loads(infile.read()) 

#### Create a data object explicit for this batch of data
testData = dataSet()

#### Ingest every event. Take O(n) time
for event in inputEvents:
	Ingest(event, testData)


#### Top x customer with greatest Simple LTV
TopX = 10
output = TopXSimpleLTVCustomers(TopX, testData)

with open('output.txt', 'w') as outfile:
	for customerID, amount in output:
		out_str = str(customerID) + ": " + str(amount)
		outfile.write("%s\n" % out_str)




