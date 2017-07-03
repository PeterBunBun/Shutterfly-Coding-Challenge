# Shutterfly-Coding-Challenge
07-03-2017

Details:
1. I ceated a class dataSet to store all necessary date of a batch of a data. 
2. Different data batch would stays in different dataSet object. The object is store in python register so the access time is constant, O(1)
3. Within every dataSet object, there are 5 attributes, 4 dictionaies and 1 variable. Accessing dictionary (HashMap) in python take constant time, O(1)
4. Even though AvgExpenditurePerVisit and AvgWeeklyVisit are not required for this challenge, I still built the function for them for the sake of thier importance and convenience 
5. Assumption: The overall size of events does not exceed python runtime memory limit
6. Future improvement: I have add little error handler in this version. I use if-else to handle most of the case and leave all of the basic error to default error handler. Future version may include different error handler to cope with missing data or oversized data 



Find top x greatest Simple LTV customers among n customers. Time: O(n + xlogn), Space: O(n + x) 
Assumptions:
1. The time span of D is within all recorded customers' 10 year life span
2. Week is define in length instead of in real calendar week.
3. Customer whose recorded events have the span shorter than 1 day and has the total perchase of x dollars, will have the weekly expenditure of x


Create simulated input for the sake of this coding challenge. 
Assumptions:
1. Every 'IMAGE', 'ORDER' event comes after a 'SITE_VISIT' event
2. Time spans only from 2006.1.1(Shutterlfy IPO) - 2017.12.28
3. Day generator could only generate day from 1 - 28 every month for simplicity.

Default:
1. 3000 events (actual events might be more than this value due to the limitaion of 'IMAGE' and 'ORDER' events)
2. 1000 total customers

