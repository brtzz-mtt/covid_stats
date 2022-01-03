Covid Stats
===========

[![Netlify Status](https://api.netlify.com/api/v1/badges/79cc5eac-276e-495e-98bd-15ed48347e64/deploy-status)](https://csml.netlify.app) a static export of this project can be found at URL [https://csml.netlify.app/](https://csml.netlify.app)

TBDs
----

- fix temperature labels and legend
- incrementale generation of data/data_[DATUM] csv file
- add remaining vip countries with more statistics
- additional illness statistics & vaccination rate data
- auto-documentation generator

BASH scripts
------------

Bundled pytests can be run and resulting code-coverage reports saved under ./htmlcov as follows:
```
./toolbox.sh checkup
```

A static html structure of application can be esported under ./build as follows (includes checkup):
```
./toolbox.sh build
```

Additionaly, local dev branch (with appropriate privileges) can be merged in master like this:
```
./toolbox.sh push
```

---

Copyright © 2021 Bertozzi Matteo