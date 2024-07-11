import json

from g_helpers import data, masechet_to_dapim
import os


curr_dir = os.path.dirname(__file__)
riddles = os.path.join('../', curr_dir)

masechet = input("מכסת?").replace(" ", "_")
assert masechet in data
daf = input('דף?')
assert daf in masechet_to_dapim[masechet]

print("%s %s" % (masechet, daf))
q = input('שאלה:')
a1 = input("תשובה 1")
a2 = input("תשובה 2")
a3 = input("תשובה 3")
a4 = input("תשובה 4")


def int_input(s):
    while 1:
        d = input(s).strip()
        try:
            d = int(d)
            assert 1 <= d <= 4, 'צריך מספר בין 1 ל4'
            return d
        except Exception as e:
            print(str(e))


right_ans = int_input('מספר התשובה הנכונה')

file_path = os.path.join(riddles, '%s_%s.json' % (masechet, daf))
print(file_path)

if os.path.exists(file_path):
    with open(file_path) as f:
        data = json.loads(file_path)
else:
    data = {'questions': []}

data['questions'].append(
    {
        'q': q,
        'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4,
        'right_ans': right_ans
    }
)
with open(file_path, 'w') as f:
    f.write(json.dumps(data, indent=4))

print('done')