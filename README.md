Covid Stats
===========

[![Netlify Status](https://api.netlify.com/api/v1/badges/79cc5eac-276e-495e-98bd-15ed48347e64/deploy-status)](https://csml.netlify.app)

TBDs
----

- introduction for readme and indexes
- code-sniffing and static analysis (pylint, sniffer, code-sniffer) on checkup action
- auto-documentation generator
- 2022 prognosis generator + control group
- additional illness statistics

BASH scripts
------------

Bundled pytests can be run and resulting code-coverage reports saved under ./htmlcov as follows:
```
sh toolbox checkup
```

A static html structure of application can be esported under ./build as follows (includes checkup):
```
sh toolbox build
```

Additionaly, local dev branch (with appropriate privileges) can be merged in master like this:
```
sh toolbox push
```

---

Copyright © 2021 Bertozzi Matteo