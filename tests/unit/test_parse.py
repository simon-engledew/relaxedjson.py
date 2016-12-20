import unittest
import parsec
import relaxedjson

# 2007-10-05
JSONDOCS = [
    # http://json.org/JSON_checker/test/fail1.json
    '"A JSON payload should be an object or array, not a string."',
    # http://json.org/JSON_checker/test/fail2.json
    '["Unclosed array"',
    # http://json.org/JSON_checker/test/fail3.json
    # '{unquoted_key: "keys must be quoted"}',
    # http://json.org/JSON_checker/test/fail4.json
    # '["extra comma",]',
    # http://json.org/JSON_checker/test/fail5.json
    '["double extra comma",,]',
    # http://json.org/JSON_checker/test/fail6.json
    '[   , "<-- missing value"]',
    # http://json.org/JSON_checker/test/fail7.json
    '["Comma after the close"],',
    # http://json.org/JSON_checker/test/fail8.json
    '["Extra close"]]',
    # http://json.org/JSON_checker/test/fail9.json
    # '{"Extra comma": true,}',
    # http://json.org/JSON_checker/test/fail10.json
    '{"Extra value after close": true} "misplaced quoted value"',
    # http://json.org/JSON_checker/test/fail11.json
    '{"Illegal expression": 1 + 2}',
    # http://json.org/JSON_checker/test/fail12.json
    '{"Illegal invocation": alert()}',
    # http://json.org/JSON_checker/test/fail13.json
    '{"Numbers cannot have leading zeroes": 013}',
    # http://json.org/JSON_checker/test/fail14.json
    '{"Numbers cannot be hex": 0x14}',
    # http://json.org/JSON_checker/test/fail15.json
    '["Illegal backslash escape: \\x15"]',
    # http://json.org/JSON_checker/test/fail16.json
    '[\\naked]',
    # http://json.org/JSON_checker/test/fail17.json
    '["Illegal backslash escape: \\017"]',
    # http://json.org/JSON_checker/test/fail18.json
    # '[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]',
    # http://json.org/JSON_checker/test/fail19.json
    '{"Missing colon" null}',
    # http://json.org/JSON_checker/test/fail20.json
    '{"Double colon":: null}',
    # http://json.org/JSON_checker/test/fail21.json
    '{"Comma instead of colon", null}',
    # http://json.org/JSON_checker/test/fail22.json
    '["Colon instead of comma": false]',
    # http://json.org/JSON_checker/test/fail23.json
    '["Bad value", truth]',
    # http://json.org/JSON_checker/test/fail24.json
    # "['single quote']",
    # http://json.org/JSON_checker/test/fail25.json
    # '["\ttab\tcharacter\tin\tstring\t"]',
    # http://json.org/JSON_checker/test/fail26.json
    '["tab\\   character\\   in\\  string\\  "]',
    # http://json.org/JSON_checker/test/fail27.json
    # '["line\nbreak"]',
    # http://json.org/JSON_checker/test/fail28.json
    '["line\\\nbreak"]',
    # http://json.org/JSON_checker/test/fail29.json
    '[0e]',
    # http://json.org/JSON_checker/test/fail30.json
    '[0e+]',
    # http://json.org/JSON_checker/test/fail31.json
    '[0e+-1]',
    # http://json.org/JSON_checker/test/fail32.json
    '{"Comma instead if closing brace": true,',
    # http://json.org/JSON_checker/test/fail33.json
    '["mismatch"}',
    '["mismatched_quotes\']',
    # http://code.google.com/p/simplejson/issues/detail?id=3
    # '["A\u001FZ control characters in string"]',
]

PASS_1 = r'''
[
    "JSON Test Pattern pass1",
    {"object with 1 member":["array with 1 element"]},
    {},
    [],
    -42,
    true,
    false,
    null,
    {
        "integer": 1234567890,
        "real": -9876.543210,
        "e": 0.123456789e-12,
        "E": 1.234567890E+34,
        "":  23456789012E66,
        "zero": 0,
        "one": 1,
        "space": " ",
        "quote": "\"",
        "backslash": "\\",
        "controls": "\b\f\n\r\t",
        "slash": "/ & \/",
        "alpha": "abcdefghijklmnopqrstuvwyz",
        "ALPHA": "ABCDEFGHIJKLMNOPQRSTUVWYZ",
        "digit": "0123456789",
        "0123456789": "digit",
        "special": "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
        "hex": "\u0123\u4567\u89AB\uCDEF\uabcd\uef4A",
        "true": true,
        "false": false,
        "null": null,
        "array":[  ],
        "object":{  },
        "address": "50 St. James Street",
        "url": "http://www.JSON.org/",
        "comment": "// /* <!-- --",
        "# -- --> */": " ",
        " s p a c e d " :[1,2 , 3
,
4 , 5        ,          6           ,7        ],"compact":[1,2,3,4,5,6,7],
        "jsontext": "{\"object with 1 member\":[\"array with 1 element\"]}",
        "quotes": "&#34; \u0022 %22 0x22 034 &#x22;",
        "\/\\\"\uCAFE\uBABE\uAB98\uFCDE\ubcda\uef4A\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"
: "A key can be any string"
    },
    0.5 ,98.6
,
99.44
,
1066,
1e1,
0.1e1,
1e-1,
1e00,2e+00,2e-00
,"rosebud"]
'''

PASS_3 = r'''
{
    "JSON Test Pattern pass3": {
        "The outermost value": "must be an object or array.",
        "In this test": "It is an object."
    }
}
'''

import os

class TestParse(unittest.TestCase):
    def loads(self, text):
        return relaxedjson.parse(text)

    @property
    def JSONDecodeError(self):
        return parsec.ParseError

    def test_unquoted_key(self):
        self.assertEqual(self.loads('{moose: "goose"}'), {'moose': 'goose'})
        self.assertEqual(self.loads('{ moose : "goose"}'), {'moose': 'goose'})
        self.assertEqual(self.loads('{moose_key: "goose"}'), {'moose_key': 'goose'})
        self.assertEqual(self.loads('{moose-key: "goose"}'), {'moose-key': 'goose'})
        self.assertEqual(self.loads('{moose-key10: "goose"}'), {'moose-key10': 'goose'})

    def test_multiline(self):
        self.assertEqual(self.loads("""{key:
"value"}"""), {'key': 'value'})
        self.assertEqual(self.loads("""{
key:
"value"
}"""), {'key': 'value'})

    def test_comments(self):
        self.assertEqual(self.loads('{/* moose */}'), {})
        self.assertEqual(self.loads('{/** moose */}'), {})
        self.assertEqual(self.loads('[/** moose **/]'), [])
        self.assertEqual(self.loads("""{/** moose */key:"value"}"""), {'key': 'value'})
        self.assertEqual(self.loads("""{key:"value"/** moose */}"""), {'key': 'value'})
        self.assertEqual(self.loads("""{key:"value"}"""), {'key': 'value'})
        self.assertEqual(self.loads("""{key:/** moose */"value"}"""), {'key': 'value'})
        self.assertEqual(self.loads("""{key:
/** moose */
"value"}"""), {'key': 'value'})

    def test_empty_objects(self):
        self.assertEqual(self.loads('{}'), {})
        self.assertEqual(self.loads('[]'), [])

    def test_pass1(self):
        self.loads(PASS_1)

    def test_pass3(self):
        self.loads(PASS_3)

    def test_failures(self):
        for idx, doc in enumerate(JSONDOCS):
            try:
                self.loads(doc)
            except self.JSONDecodeError:
                pass
            else:
                self.fail("Expected failure for fail{0}.json: {1!r}".format(idx, doc))


    def test_truncated_input(self):
        test_cases = [
            ('', 'Expecting value', 0),
            ('[', 'Expecting value', 1),
            ('[42', "Expecting ',' delimiter", 3),
            ('[42,', 'Expecting value', 4),
            ('["', 'Unterminated string starting at', 1),
            ('["spam', 'Unterminated string starting at', 1),
            ('["spam"', "Expecting ',' delimiter", 7),
            ('["spam",', 'Expecting value', 8),
            ('{', 'Expecting property name enclosed in double quotes', 1),
            ('{"', 'Unterminated string starting at', 1),
            ('{"spam', 'Unterminated string starting at', 1),
            ('{"spam"', "Expecting ':' delimiter", 7),
            ('{"spam":', 'Expecting value', 8),
            ('{"spam":42', "Expecting ',' delimiter", 10),
            ('{"spam":42,', 'Expecting property name enclosed in double quotes', 11),
        ]
        test_cases += [
            ('"', 'Unterminated string starting at', 0),
            ('"spam', 'Unterminated string starting at', 0),
        ]
        for data, msg, idx in test_cases:
            with self.assertRaises(self.JSONDecodeError) as cm:
                self.loads(data)

    def test_unexpected_data(self):
        test_cases = [
            ('[,', 'Expecting value', 1),
            ('{"spam":[}', 'Expecting value', 9),
            ('[42:', "Expecting ',' delimiter", 3),
            ('[42 "spam"', "Expecting ',' delimiter", 4),
            # ('[42,]', 'Expecting value', 4),
            ('{"spam":[42}', "Expecting ',' delimiter", 11),
            ('["]', 'Unterminated string starting at', 1),
            ('["spam":', "Expecting ',' delimiter", 7),
            # ('["spam",]', 'Expecting value', 8),
            ('{:', 'Expecting property name enclosed in double quotes', 1),
            ('{,', 'Expecting property name enclosed in double quotes', 1),
            ('{42', 'Expecting property name enclosed in double quotes', 1),
            ('[{]', 'Expecting property name enclosed in double quotes', 2),
            ('{"spam",', "Expecting ':' delimiter", 7),
            ('{"spam"}', "Expecting ':' delimiter", 7),
            ('[{"spam"]', "Expecting ':' delimiter", 8),
            ('{"spam":}', 'Expecting value', 8),
            ('[{"spam":]', 'Expecting value', 9),
            ('{"spam":42 "ham"', "Expecting ',' delimiter", 11),
            ('[{"spam":42]', "Expecting ',' delimiter", 11),
            # ('{"spam":42,}', 'Expecting property name enclosed in double quotes', 11),
        ]
        for data, msg, idx in test_cases:
            with self.assertRaises(self.JSONDecodeError) as cm:
                self.loads(data)

    def test_extra_data(self):
        test_cases = [
            ('[]]', 'Extra data', 2),
            ('{}}', 'Extra data', 2),
            ('[],[]', 'Extra data', 2),
            ('{},{}', 'Extra data', 2),
        ]
        test_cases += [
            ('42,"spam"', 'Extra data', 2),
            ('"spam",42', 'Extra data', 6),
        ]
        for data, msg, idx in test_cases:
            with self.assertRaises(self.JSONDecodeError) as cm:
                self.loads(data)

    def test_linecol(self):
        test_cases = [
            ('!', 1, 1, 0),
            (' !', 1, 2, 1),
            ('\n!', 2, 1, 1),
            ('\n  \n\n     !', 4, 6, 10),
        ]
        for data, line, col, idx in test_cases:
            with self.assertRaises(self.JSONDecodeError) as cm:
                self.loads(data)
