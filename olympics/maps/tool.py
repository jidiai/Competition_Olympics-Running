import json


def load_map(path):
    file = open(path, "rb")
    filejson = json.load(file)
    return filejson


def store(record, name):
    with open(str(name)+'.json', 'w') as f:
        f.write(json.dumps(record))


def rewrite(a_map):
    lines = list()
    wall = a_map["wall"]["objects"]
    for a, w in wall.items():
        init_pos = w["initial_position"]
        combine = False
        for l in lines:

            condition1 = (init_pos[0] in l) or (init_pos[1] in l)
            if condition1:
                if init_pos[0] in l:
                    another = init_pos[1]  # 另一个点
                    x_in, y_in = init_pos[0]  # 重合的点
                else:
                    another = init_pos[0]
                    x_in, y_in = init_pos[1]

                x0, y0 = l[0]
                x1, y1 = l[1]
                stamp = 0 if x0 == x1 else 1  # 如果x相同，y则是变量
                condition2 = (another[stamp] == l[0][stamp])

                if condition2:
                    combine = True
                    l.extend(init_pos)
                    break
        if not combine:
            lines.append(init_pos)

    new_lines = list()

    for l_n in lines:
        x0, y0 = l_n[0]
        x1, y1 = l_n[1]
        stamp = 1 if x0 == x1 else 0
        points = [i[stamp] for i in l_n]
        new_line = [[x0, min(points)], [x0, max(points)]] if stamp == 1 else [[min(points), y0], [max(points), y0]]
        new_lines.append(new_line)


    return new_lines


def rewrite2(maps):
    for key, map in maps.items():
        lines = list()
        wall = map["wall"]["objects"]
        for a, w in wall.items():
            init_pos = w["initial_position"]
            combine = False
            for l in lines:

                condition1 = (init_pos[0] in l) or (init_pos[1] in l)
                if condition1:
                    if init_pos[0] in l:
                        another = init_pos[1]  # 另一个点
                        x_in, y_in = init_pos[0]  # 重合的点
                    else:
                        another = init_pos[0]
                        x_in, y_in = init_pos[1]

                    x0, y0 = l[0]
                    x1, y1 = l[1]
                    stamp = 0 if x0 == x1 else 1  # 如果x相同，y则是变量
                    condition2 = (another[stamp] == l[0][stamp])

                    if condition2:
                        combine = True
                        l.extend(init_pos)
                        break
            if not combine:
                lines.append(init_pos)

        new_lines = list()

        for l_n in lines:
            x0, y0 = l_n[0]
            x1, y1 = l_n[1]
            stamp = 1 if x0 == x1 else 0
            points = [i[stamp] for i in l_n]
            new_line = [[x0, min(points)], [x0, max(points)]] if stamp == 1 else [[min(points), y0], [max(points), y0]]
            new_lines.append(new_line)

        new_objects = dict()
        count = 1
        for n in new_lines:
            new_objects["component"+str(count)] = dict()
            new_objects["component" + str(count)]["initial_position"] = n
            new_objects["component" + str(count)]["color"] = "black"
            count += 1
        map["wall"]["objects"] = new_objects
    return maps


if __name__ == "__main__":
    a_map = load_map("test.json")
    print("test_map: ", a_map)
    lines = rewrite(a_map)
    for l in lines:
        print(l)
    maps = load_map("maps.json")
    new_maps = rewrite2(maps)
    print("new_maps: ", new_maps)
    store(new_maps, name="maps_new")
