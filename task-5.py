import re

import pytest
import subprocess
import numpy as np


python_name = 'python3'
app_filename = './app.py'


def parse_list(src):
    p = '(\'.*?\')'
    match = re.findall(p, src)
    result = []
    for num in match:
        result.append(num[1:-1])
    return result


@pytest.mark.timeout(10)
def test_different_floats():
    floats = ['-.1', '0.1', '1.1', '+1.1', '5.0', '.1', '1234213.', '1.',
              '1233215.4213213', '+1233215.4213213', '0.124534123213',
              '-4123124.4213123']
    e_floats_bases = ['-.1', '0.1', '1.1', '5.0', '.1', '-1.234213', '1', '-1',
                      '+1.4213213', '0.124534123213',
                      '-4.4213123']
    np.random.seed(0)
    small_es = []
    big_es = []

    for fl in e_floats_bases:
        def get_power():
            pwr = np.random.randint(-100, 100)
            return str(pwr if pwr != 0 else 5)

        small_e = fl + 'e' + get_power()
        big_e = fl + 'E' + get_power()
        small_es.append(small_e)
        big_es.append(big_e)

    floats = floats + small_es + big_es

    pattern = 'x = %f'
    data = ''
    for fl in floats:
        line = pattern.replace('%f', fl)
        data += line + '\n'
    filename = './single_floats.txt'
    with open(filename, 'w') as f:
        f.write(data)

    run = subprocess.run([python_name, app_filename, filename, pattern], capture_output=True)
    out = run.stdout.decode()

    result = parse_list(out)

    # print(result)
    for fl in floats:
        assert fl in result, f"Valid number {fl} was not parsed properly"


@pytest.mark.timeout(10)
def test_different_ints():
    ints = ['1', '10', '124534131124354341', '4513', '45131', '123123123']
    pluses = []
    minuses = []

    for n in ints:
        pluses.append(f"+{n}")
        minuses.append(f"-{n}")

    ints = ints + pluses + minuses

    pattern = 'x = %d'
    data = ''
    for n in ints:
        line = pattern.replace('%d', n)
        data += line + '\n'

    filename = './single_ints.txt'
    with open(filename, 'w') as f:
        f.write(data)

    run = subprocess.run([python_name, app_filename, filename, pattern], capture_output=True)
    out = run.stdout.decode()

    result = parse_list(out)

    # print(result)
    for n in ints:
        assert n in result, f"Valid number {n} was not parsed properly"


@pytest.mark.timeout(10)
def test_different_strs():
    strs = ['asdasdad', 'f 3r1q21rfwqcwa awecdas dwacd', 'asda wf w fdadwad WAD QWD'
            'aws d-as d_AS_ da-sd2-1 qw-asd_ ', ' asd21 qwe- @1434Q@w e#Q RE$Q@ew']

    pattern = 'the string is %s and that is fine'
    data = ''
    for n in strs:
        line = pattern.replace('%s', n)
        data += line + '\n'

    filename = './single_strs.txt'
    with open(filename, 'w') as f:
        f.write(data)

    run = subprocess.run([python_name, app_filename, filename, pattern], capture_output=True)
    out = run.stdout.decode()

    result = parse_list(out)

    # print(result)
    for n in strs:
        assert n in result, f"Valid string {n} was not parsed properly"


@pytest.mark.timeout(10)
def test_phrase():
    strs = ['string11',
            'string12',
            'string13 with a space']
    ints = ['1',
            '10',
            '124534131124354341']
    floats = ['1.341',
              '1.2e5',
              '-0.7E15']
    strs2 = ['secondstring',
             'Some_underscores',
             'just a Hugasd  Medsssss  asdasdwa f']

    pattern = 'the string has string %s, int %d and a float %f, and also a string %s'

    data = ''
    for i in range(len(strs)):
        line = pattern.replace('%s', strs[i], 1)
        line = line.replace('%d', ints[i])
        line = line.replace('%f', floats[i])
        line = line.replace('%s', strs2[i])

        data += line + '\n'

    filename = './complex_phrase.txt'
    with open(filename, 'w') as f:
        f.write(data)

    run = subprocess.run([python_name, app_filename, filename, pattern], capture_output=True)
    out = run.stdout.decode()
    print(out)
    lists = out.split('\n')
    strs_result = parse_list(lists[0])
    floats_result = parse_list(lists[1])
    ints_result = parse_list(lists[2])
    strs2_result = parse_list(lists[3])

    assert strs_result == strs
    assert floats_result == floats
    assert ints_result == ints
    assert strs2_result == strs2


