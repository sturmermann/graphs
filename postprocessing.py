def postprocessingMain(matrix):
    writed = f"{len(matrix)} \n"
    for i in matrix:
        for j in i:
            writed += f"{j}, "
        writed = writed[:-2]
        writed += "\n"
    with open("graph.out", "w") as text:
        text.write(writed)
    return 1
