qsardb
======

Package for handling QSAR data.

Setting up the database
-----------------------

Create a postgresql database called `qsardb`:

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

Set up a chembl database.  Then grant select for qsar:

```bash
psql chembl_{version} -c'GRANT SELECT ON ALL TABLES IN SCHEMA public TO qsar;
```

Finally, use the chembl loader script.

```bash
python -m qsardb.data.chembl.__init__
```

