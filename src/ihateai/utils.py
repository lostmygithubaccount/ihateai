import random

from ihateai.grid import InputOutputPair


def random_task_num(t):
    task_nums = sorted(t.distinct(on="task_num")["task_num"].to_pyarrow().to_pylist())
    task_num = random.choice(task_nums)

    t = t.filter(t["task_num"] == task_num)
    example_nums = sorted(
        t.distinct(on="example_num")["example_num"].to_pyarrow().to_pylist()
    )
    example_num = random.choice(example_nums)

    return task_num, example_num


def show_task_pairs(t, task_num=None):
    if not task_num:
        task_num = random_task_num(t)

    task = t.filter(t["task_num"] == task_num)
    for i in range(task.count().to_pyarrow().as_py()):
        row = task.limit(1, offset=i)
        print(row.to_pyarrow().to_pylist())
        print()
        grids = row["input", "output"].to_pyarrow().to_pylist()[0]

        InputOutputPair(grids["input"], grids["output"]).show()

    return task_num


def show_rand_io_pair(t):
    t_len = t.count().to_pyarrow().as_py()

    offset = random.randint(0, t_len - 1)

    row = t.limit(1, offset=offset)
    print(row.to_pyarrow().to_pylist())
    print()
    grids = row["input", "output"].to_pyarrow().to_pylist()[0]

    InputOutputPair(grids["input"], grids["output"]).show()
