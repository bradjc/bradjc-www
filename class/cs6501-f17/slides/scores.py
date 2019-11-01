import csv
import statistics

papers = {}

with open('cs6501f17-scores.csv') as f:
	reader = csv.reader(f)
	li = list(reader)

for fields in li:
	# fields = l.split(',')
	# print()

	try:
		paper = int(fields[0])
		presentation = int(fields[4])
		interest = int(fields[5])
		impact = int(fields[6])
		overall = int(fields[7])
		confidence = int(fields[8])


		if paper not in papers:
			papers[paper] = [[], [], [], [], [], '']

		papers[paper][0].append(presentation)
		papers[paper][1].append(interest)
		papers[paper][2].append(impact)
		papers[paper][3].append(overall)
		papers[paper][4].append(confidence)
		papers[paper][5] = fields[1]
	except:
		print(fields)



print(papers)


with open('results.csv', 'w') as f:
	for paperid,values in papers.items():
		pres = statistics.mean(values[0])
		inte = statistics.mean(values[1])
		impa = statistics.mean(values[2])
		over = statistics.mean(values[3])
		conf = statistics.mean(values[4])

		f.write('{},"{}",{},{},{},{},{},{}\n'.format(paperid, values[5], len(values[0]), pres, inte, impa, over, conf))

