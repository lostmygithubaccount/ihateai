import ibis
import ibis.selectors as s


def read_training():
    t = ibis.read_json("data/training/*.json", filename=True)

    transforms = {
        "task_num": ibis.row_number(),
        "test_len": t["test"].length(),
        "train_len": t["train"].length(),
    }

    t = (
        t.mutate(
            file_id=t["filename"].re_extract(r"(\w{8})\.json", 0).replace(".json", "")
        )
        .mutate(**transforms)
        .relocate(transforms.keys())
        .relocate("task_num", "file_id")
    )

    return t


def transform(t, test=False):
    transforms = {
        "example_num": ibis.row_number().over(ibis.window(group_by="task_num")),
        "input_width": ibis._["input"].length(),
        "input_height": ibis._["input"][0].length(),
        "output_width": ibis._["output"].length(),
        "output_height": ibis._["output"][0].length(),
    }

    col_name = "test" if test else "train"

    res = (
        t.select("task_num", "file_id", t[col_name].unnest())
        .select(
            "task_num",
            "file_id",
            ibis._[col_name]["input"],
            ibis._[col_name]["output"],
        )
        .mutate(**transforms)
        .relocate(transforms.keys())
        .relocate("file_id", "task_num", "example_num")
        .order_by("task_num", "example_num")
    )

    res = (
        res.join(
            res.select(
                "task_num",
                "example_num",
                res["input"].unnest(),
                res["output"].unnest(),
            )
            .group_by(
                "task_num",
                "example_num",
            )
            .agg(
                input_colors=ibis._["input"].collect().flatten().unique().sort(),
                output_colors=ibis._["output"].collect().flatten().unique().sort(),
            ),
            ["task_num", "example_num"],
        )
        .relocate(res.columns[:3], "input_colors", "output_colors")
        .drop(s.contains("_right"))
        .order_by("task_num", "example_num")
    )

    return res
