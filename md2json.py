#!/usr/bin/env python

import re
import json


def get_category(idx):
    # 1: 1-426
    yield 1
    # 2: 1-38,    47-98,    100-374,    387-426
    if 1 <= idx <= 38 or 47 <= idx <= 98 or 100 <= idx <= 374 or 387 <= idx <= 426:
        yield 2
    # 3: 1-34,  47-98,  100-135,  150-226,  387-391,  409-422
    if 1 <= idx <= 34 or 47 <= idx <= 98 or 100 <= idx <= 135 or 150 <= idx <= 226 or \
       387 <= idx <= 391 or 409 <= idx <= 422:
        yield 3
    # 4: 1-17,   47-98,   100-135,   150-226,   387-391,   409-422
    if 1 <= idx <= 17 or 47 <= idx <= 98 or 100 <= idx <= 135 or 150 <= idx <= 226 or \
       387 <= idx <= 391 or 409 <= idx <= 422:
        yield 4


def get_questions():
    r_line = re.compile(r'\[(\d+)\] ([abcd])')
    r_q = re.compile(r'^Вопрос №(\d+)')

    with open('answers.txt') as f:
        answers = {k: v for k, v in sum((r_line.findall(line) for line in f), [])}

    ql = {}
    with open('ham.md') as f:
        question = {}
        current_tag = current_idx = None
        for line in f:
            if line.startswith("# "):
                current_tag = line.lstrip("# ").strip()
            elif line.startswith("## Вопрос"):
                if question:
                    ql[current_idx] = question
                current_idx = r_q.match(line.lstrip("# ").strip()).group(1)
                current_answer = {'a': 1, 'b': 2, 'c': 3, 'd': 4}[answers[current_idx]]
                question = {
                    'choices': [],
                    'body': '',
                    'tags': [current_tag, ],
                    'answer': current_answer
                }
                question['tags'].extend("{0} категория".format(cat) for cat in
                                        get_category(int(current_idx)))
            elif line.startswith("- "):
                question['choices'].append(line.lstrip("- ").rstrip())
            elif line.startswith('![img'):
                question['image'] = line.strip()
            elif line.strip():
                question['body'] += line.strip()
    return ql


if __name__ == "__main__":
    data = get_questions()
    print(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
