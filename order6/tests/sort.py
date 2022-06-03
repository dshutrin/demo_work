clans = [10, 100, 300, 0, 3000, 10]

for i in range(len(clans)):
		for k in range(i, len(clans)):
			if clans[i] < clans[k]:
				clans[i], clans[k] = clans[k], clans[i]

input(clans[:3])