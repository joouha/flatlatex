
from .. import data
from .. import parser

import ast


def test_known_fracts():
    assert type(data.known_fracts) is dict
    for k, v in data.known_fracts.items():
        assert type(k) is tuple
        assert len(k) == 2
        assert all([type(x) is str for x in k])
        assert type(v) is str


def test_transliteration_consistancy():
    for d in (
            data.subscript,
            data.superscript,
            data.bb,
            data.bf,
            data.cal,
            data.frak,
            data.it,
            data.mono,
            ):
        assert type(d) is dict
        for k, v in d.items():
            assert type(k) is str
            assert type(v) is str


def test_symbols_consistancy():
    assert type(data.symbols) is dict
    for k, v in data.symbols.items():
        assert type(k) is str
        out = parser.parse(k)
        assert len(out) == 1
        assert out[0][0] == 'cmd'
        assert type(v) is str


def test_combining_consistancy():
    assert type(data.combinings) is dict
    for k, v in data.combinings.items():
        assert type(k) is str
        out = parser.parse(k)
        assert len(out) == 1
        assert out[0][0] == 'cmd'
        assert type(v) is tuple
        assert len(v) == 2
        assert all([type(x) is str for x in v])


def test_newcommands_consistancy():
    assert type(data.newcommands) is tuple
    for k in data.newcommands:
        parsed = parser.parse(k)
        assert len(parsed) in (3, 6)
        assert parsed[0][0] == 'cmd'
        assert parsed[0][1] in (r'\newcommand', r'\renewcommand', r'\def')
        if len(parsed) == 6:
            assert parsed[2] == ('char', '[')
            assert parsed[4] == ('char', ']')
            assert type(parsed[3][0]) is str
            a = int(parsed[3][1])
            assert a >= 0


def test_replicated_command():
    datasets = [
            data.symbols.keys(),
            data.combinings.keys(),
            data.transliterators.keys(),
    ]
    datasets.append([parser.parse(nc)[1][1] for nc in data.newcommands])
    for i in range(len(datasets)):
        for j in range(i + 1, len(datasets)):
            s1 = set(datasets[i])
            s2 = set(datasets[j])
            assert len(s1.intersection(s2)) == 0


def test_replicated_in_the_same_dict():
    with open(data.__file__, encoding='utf8') as f:
        data_ast = ast.parse(f.read())

    def toobj(x):
        if type(x) is ast.Tuple:
            return tuple(toobj(v) for v in x.elts)
        return x.s

    for seg in data_ast.body:
        if type(seg) is ast.Assign:
            if type(seg.value) is ast.Dict:
                keys = [toobj(k) for k in seg.value.keys]
                count = {}
                for k in keys:
                    count[k] = count[k] + 1 if k in count else 1
                for k, c in count.items():
                    assert c == 1, "duplicated key in dict: %s" % k
