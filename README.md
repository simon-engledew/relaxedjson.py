[![Build Status](https://travis-ci.org/simon-engledew/sshim.svg?branch=master)](https://travis-ci.org/simon-engledew/sshim)

```
pip install relaxedjson
```

Parses JSON that is missing quotes around the keys.

```python
>>> import json
>>> json.loads('{moose: "goose"}')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File ".../python2.7/json/__init__.py", line 339, in loads
    return _default_decoder.decode(s)
  File ".../python2.7/json/decoder.py", line 364, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File ".../python2.7/json/decoder.py", line 380, in raw_decode
    obj, end = self.scan_once(s, idx)
ValueError: Expecting property name: line 1 column 2 (char 1)

>>> import relaxedjson
>>> relaxedjson.parse('{moose: "goose"}')
{'moose': 'goose'}
```

See http://pythonhosted.org/relaxedjson/