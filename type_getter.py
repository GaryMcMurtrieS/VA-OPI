va_pvs = open("VA_pvlist.txt", "r")
raw_data = va_pvs.readlines()

data = {}
for line in raw_data:
    line = line.rstrip()

    end_type = line.split(":")[-1]

    if end_type not in data:
        data[end_type] = []

    data[end_type].append(line)

for type in data:
    print(type)
