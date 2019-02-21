import csv
import os
import datetime
def getInfo(action):
	cpt=0
	filename=os.environ["PUBLIC"]+'\\'+action+'Info.csv'
	with open(filename, 'r') as textfile:
		for row in reversed(list(csv.DictReader(textfile, fieldnames = ("date", "info", "pertinence", "note"), delimiter = ';'))):
			date = row['date']
			if date == "date":
				break
			info = row['info']
			pertinence = row['pertinence']
			note = row['note']
			datetime.datetime.strptime(row['date'], "%Y-%m-%d %H:%M")
			limit = datetime.datetime.now()
			limit = limit - datetime.timedelta(hours=2)
			if datetime.datetime.strptime(row['date'], "%Y-%m-%d %H:%M") < limit:
				if cpt==0:
					tab=[date,info,pertinence,note]
					cpt=1
				else:
					tab=tab,[date,info,pertinence,note]
	cpt = 0
	res=[]
	res.append(0)
	res.append('')
	for i in tab:
		res[0]+=5 + float(i[3]) * float(i[2])
		res[1]+=i[1]+'\n'
		cpt+=1
	res[0]=res[0]/cpt
	return res

print(getInfo('technipfmc'))