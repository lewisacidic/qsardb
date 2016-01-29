from sqlalchemy import func, and_, desc
import pandas as pd
import skchem

from ..models import Session, Compound, Target, Activity
from ..utils import config

class Dataset(object):
    def __init__(self, activity_filter=True, target_filter=True, compound_filter=True):
        self.session = Session()
        query = (self.session.query(func.max(Compound.smiles).label('structure'),
                 Target.external_id.label('target_id'),
                 func.avg(Activity.value).label('value'))
                 .join(Activity, Target)
                 .filter(activity_filter, target_filter, compound_filter)
                 .group_by(Compound.external_id, Target.external_id))
        self.data = pd.read_sql_query(query.statement, config['alembic']['sqlalchemy.url'])
