import sys

import pathlib

import jinja2

DIR_PATH = pathlib.Path(__file__).parent

TYPES_LIST = [
    ("double", "double"),
    ("float", "float"),
]
for int_prefix_proto in [
    "int",
    "sint",
    "sfixed",
]:
    for size in [
        32,
        64,
    ]:
        TYPES_LIST.append((f"{int_prefix_proto}{size}", f"int{size}_t"))


def render_template(*, in_file, out_file, context):
    with open(in_file, "r") as in_f:
        template = jinja2.Template(in_f.read())

    with open(out_file, "w") as out_f:
        out_f.write(template.render(**context))


if __name__ == "__main__":
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    render_template(
        in_file=in_file,
        out_file=out_file,
        context=dict(data_types=TYPES_LIST),
    )
