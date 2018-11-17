# csv reader
import csv

csvfile = open('OfficeSupplies.csv','rb')
reader = csv.reader(csvfile)

for row in reader:
	print row

