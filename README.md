Covid Stats
===========

[![Netlify Status](https://api.netlify.com/api/v1/badges/79cc5eac-276e-495e-98bd-15ed48347e64/deploy-status)](https://csml.netlify.app) -> static export of this project can be found at URL [https://csml.netlify.app/](https://csml.netlify.app)

TBDs
----

- auto-documentation generator
- additional illness statistics & vaccination rate data

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