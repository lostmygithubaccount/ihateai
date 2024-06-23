import random

from ihateai.grid import InputOutputPair


def show_rand_io_pair(t):
    t_len = t.count().to_pyarrow().as_py()

    offset = random.randint(0, t_len - 1)

    row = t.limit(1, offset=offset)
    print(row.to_pyarrow().to_pylist())
    print()
    grids = row["input", "output"].to_pyarrow().to_pylist()[0]

    InputOutputPair(grids["input"], grids["output"]).show()


def show_rand_task_pairs(t):
    task_nums = sorted(t.distinct(on="task_num")["task_num"].to_pyarrow().to_pylist())

    task_num = random.choice(task_nums)

    task = t.filter(t["task_num"] == task_num)
    for i in range(task.count().to_pyarrow().as_py()):
        row = task.limit(1, offset=i)
        print(row.to_pyarrow().to_pylist())
        print()
        grids = row["input", "output"].to_pyarrow().to_pylist()[0]

        InputOutputPair(grids["input"], grids["output"]).show()
