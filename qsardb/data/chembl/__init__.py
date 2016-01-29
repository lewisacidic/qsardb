import logging, sys, os

from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy_utils import database_exists, create_database

from tqdm import tqdm

# import skchem

from ...models import Session, Source, Species, Target, Compound, Activity


LOGGER = logging.getLogger(__file__)
LOGGER.setLevel(logging.INFO)

if len(LOGGER.handlers) == 0:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    LOGGER.addHandler(ch)

class ChemblLoader(object):

    def __init__(self, chembl_version=20):
        self.chembl_version = chembl_version

        if not database_exists(self.database_url):
            self.load_chembl()

        self.engine = create_engine(self.database_url)

    def load_chembl(self):
        raise NotImplementedError
        #create_database(self.database_url)

    @property
    def name(self):
        return 'chembl_{}'.format(self.chembl_version)

    @property
    def database_url(self):
        return 'postgresql://qsar:qsar@localhost/{}'.format(self.name)

    @property
    def description(self):
        return "Chembl {version} database, "
        "ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb"
        "/releases/chembl_{version}".format(version=self.chembl_version)

    @property
    def data_dir(self):
        return os.path.join(os.path.dirname(__file__), 'data', self.name)

    def query(self, name):
        with open(os.path.join(os.path.dirname(__file__), 'queries', name)) as f:
            q = f.read()
        LOGGER.info('Querying chembl with "{}"...'.format(name))
        res = self.engine.execute(q)
        return tqdm(res, total=res.rowcount)

    def load_source(self, session):
        try:
            source = session.query(Source).filter_by(name=self.name).one()
        except NoResultFound:
            source = Source(name=self.name, description=self.description)
            session.add(source)
            session.flush()
        return source

    def load_species(self, session):
        LOGGER.info('Loading species...')
        source = self.load_source(session)
        species = [Species(external_id=tax_id, name=name, source=source)
                   for tax_id, name in self.query('species.sql')]
        session.add_all(species)
        session.flush()

    def model_lookup(self, session, model):
        LOGGER.info('Building id lookup for {}...'.format(model.__name__))
        model_dict = session.query(model).all()
        return {s.external_id: s.id for s in model_dict}

    def load_targets(self, session):
        LOGGER.info('Loading targets...')
        lookup_species = self.model_lookup(session, Species)
        source = self.load_source(session)
        for accession, tax_id, sequence in self.query('targets.sql'):
            target = Target(source=source,
                            external_id=accession,
                            species_id=lookup_species[tax_id],
                            sequence=sequence)
            session.add(target)

    def load_compounds(self, session):
        LOGGER.info('Loading compounds...')
        source = self.load_source(session)
        for chembl_id, smiles in self.query('compounds.sql'):
            compound = Compound(external_id=chembl_id,
                                smiles=smiles,
                                source=source)
            session.add(compound)
    def load_activities(self, session):
        LOGGER.info('Loading activities...')

        source = self.load_source(session)

        lookup_target = self.model_lookup(session, Target)
        lookup_compound = self.model_lookup(session, Compound)

        assay_dict = {'B' : 'Binding',
                      'A' : 'ADMET',
                      'F' : 'Functional',
                      'P' : 'Property',
                      'U' : 'Unassigned'}

        for (activity_id, uniprot_accession, mol_chembl_id,
            standard_value, standard_relation, standard_type,
            assay_type, confidence_score) in self.query('activities.sql'):

            session.add(Activity(relation=standard_relation,
                              value=standard_value,
                              assay_type=assay_dict[assay_type],
                              activity_type=standard_type,
                              confidence_score=confidence_score,
                              external_id=activity_id,
                              target_id=lookup_target[uniprot_accession],
                              compound_id=lookup_compound[mol_chembl_id],
                              source=source))
    #
    # def remove_unparseable(self, session):
    #     for c in session.query(Compound).all():
    #         deleted = []
    #         try:
    #             skchem.Mol.from_smiles(c.smiles)
    #         except ValueError:
    #             deleted.append(c.id)
    #             session.delete(c)
    #     for a in session.query(Activity).join(Compound).filter(Compound.id.in_(deleted)).all():
    #         session.delete(a)

    def load_all(self, session):
        LOGGER.info('Loading all data...')
        self.load_source(session)
        self.load_species(session)
        self.load_targets(session)
        self.load_compounds(session)
        self.load_activities(session)
        # self.remove_unparseable(session)

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
