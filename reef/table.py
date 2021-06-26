from typing import Any, AnyStr, List, Optional
import re


def write_row(rows: List[List[Any]], chars, q, centered: bool = False, label=False):
    row_data = ""
    if not label:
        for row in range(len(rows)):
            c = 0
            for item in map(str, rows[row]):
                if centered:
                    row_data += chars[0] + " " + item.center((q[c])) + " "
                else:
                    row_data += chars[0] + " " + item + " " * ((q[c]) - len(item)) + " "
                c += 1
            row_data += chars[0] + "\n"
    else:
        c = 0
        for item in rows:
            item = str(item)
            if centered:
                row_data += chars[0] + " " + item.center((q[c])) + " "
            else:
                row_data += chars[0] + " " + item + " " * ((q[c]) - len(item)) + " "
            c += 1
        row_data += chars[0] + "\n"

    return row_data


def make_table(
    rows: List[List[Any]], labels: Optional[List[Any]] = None, centered: bool = False
) -> str:

    chars = "│ ─ ┌ ┬ ┐ ├ ┼ ┤ └ ┴ ┘".split()
    q = {}
    max_col = len(rows[0])

    for i in range(max_col):
        # We need to get the maximum item lengths for each column for later use.
        temp = []
        for z in range(len(rows)):
            temp.append(rows[z][i])
        q[i] = len(max(map(str, temp), key=len))

    if labels:
        # If labels exist, we need to pad the cells by them if label_length > max_col_item_width
        label_lengths = [len(str(i)) for i in labels]
        for i in range(len(label_lengths)):
            if label_lengths[i] > q[i]:
                q[i] = label_lengths[i]

    res = write_row(rows=rows, chars=chars, q=q, centered=centered)

    test = res.split("\n")[0]  # Use the first row to find the occurences of │
    idx = [
        match.start() for match in re.finditer(chars[0], test[1:])
    ]  # find indices for │

    d = ""
    t_max = len(test)  # A border will be created, so the maximum row length is needed
    for i in range(t_max - 2):
        # subtract by two to account for the two border chars on each end side
        if i in idx:
            if labels is None:
                d += chars[3]
            else:
                d += chars[6]
        else:
            d += chars[1]

    header_item = ""
    if labels:
        header = chars[2] + d.replace(chars[6], chars[3]) + chars[4] + "\n"
        header_item = write_row(
            rows=labels, chars=chars, q=q, centered=centered, label=True
        )
        mid = chars[5] + d + chars[7] + "\n"
    else:
        header = ""
        mid = chars[2] + d + chars[4] + "\n"

    new_result = (
        header
        + header_item
        + mid
        + res
        + chars[8]
        + d.replace(chars[3], chars[9]).replace(chars[6], chars[9])
        + chars[10]
    )
    return new_result
