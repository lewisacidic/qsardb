qsardb
======

Package for handling QSAR data.

Setting up the database
-----------------------

A dump of the database is available from GitHub Large File Storage.  To get it,
install `git-lfs` from [packagecloud.io](https://packagecloud.io/install/repositories/github/git-lfs/).


Create a postgresql database called `qsardb` (this will require being run as a
superuser.  By default, the postgres user):

```bash
createuser qsar
createdb qsardb --owner qsar
```

Migrate:

```bash
alembic upgrade head
```

Load chembl data
----------------

Set up a [ChEMBL postresql database](ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/).  
Then grant SELECT privileges for the qsar user:

```bash
psql chembl_{version} -c'GRANT SELECT ON ALL TABLES IN SCHEMA public TO qsar;'
```

Finally, use the ChEMBL loader script:

```bash
python -m qsardb.data.chembl
```
