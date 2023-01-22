
def load_data(filename):

    data = {}

    with open (filename) as f:
        for line in f:
            line_list = line.strip().split(',')
            line_list = list(map(lambda w: w.strip(), line_list))
            day_data = []
            if line_list[0] not in data:
                data[line_list[0]] = day_data
            for i in range (1, len(line_list)):
                day_data.append(int(line_list[i]))
        return data


def daily_cases(cumulative):
  
    case = {}
    cum_keys = cumulative.keys()
    for key in cum_keys:
        new_data = []
        case[key] = new_data
        old_data = cumulative[key]
        for i in range(len(old_data)):
            if i == 0:
                new_data.append(old_data[i])
            else:
                new_data.append(old_data[i] - old_data[i-1])
    return case


def main():
    filename = 'data/disease1.txt'

    data = load_data(filename)
    print(f"Loaded datafile {filename}:")
    print(data)

    print("Daily infections: ")
    print(daily_cases(data))


if __name__ == '__main__':
    main()
