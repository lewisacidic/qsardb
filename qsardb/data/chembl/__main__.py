import logging

from . import ChemblLoader
from ...models import Session

LOGGER = logging.getLogger(__file__)
LOGGER.setLevel(logging.INFO)

if len(LOGGER.handlers) == 0:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    LOGGER.addHandler(ch)


if __name__ == '__main__':
    session = Session()
    try:
        LOGGER.info('Initializing data loading...')
        ChemblLoader(20).load_all(session)
        LOGGER.info('Committing to database...')
        session.commit()
        LOGGER.info('Data loading successful.')
    except:
        LOGGER.error('Data loading failed.  Rolling back data entry.')
        session.rollback()
        raise
    finally:
        LOGGER.info('Closing connection.')
        session.close()
