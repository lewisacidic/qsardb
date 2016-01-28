
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from . import Base
from .utils import ModelMixin

class Source(Base, ModelMixin):

    __tablename__ = 'source'
    __repr_props__ = ['id', 'name']

    # internal id
    id = Column(Integer, Sequence('source_id_seq'), primary_key=True, unique=True, nullable=False)

    # describe source
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(250))


class Species(Base, ModelMixin):

    __tablename__ = 'species'
    __repr_props__ = ['id', 'external_id', 'name']

    # internal id
    id = Column(Integer, Sequence('species_id_seq'), primary_key=True, unique=True, nullable=False)

    # record origin
    external_id = Column(Integer, unique=True, nullable=False, index=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
    source = relationship('Source')

    name = Column(String(150), unique=False, nullable=False)


class Compound(Base, ModelMixin):

    __tablename__ = 'compound'
    __repr_props__ = ['id', 'external_id']

    # internal id
    id = Column(Integer, Sequence('compound_id_seq'), primary_key=True, unique=True, nullable=False)

    # record origin
    external_id = Column(String, unique=True, nullable=False, index=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
    source = relationship('Source')

    smiles = Column(String(750), nullable=False)


class Target(Base, ModelMixin):

    __tablename__ = 'target'
    __repr_props__ = ['id', 'external_id']

    # internal id
    id = Column(Integer, Sequence('target_id_seq'), primary_key=True, unique=True, nullable=False)

    # record origin
    external_id = Column(String, unique=True, nullable=False, index=True)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
    source = relationship('Source')

    # define species
    species_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    species = relationship('Species', backref='targets')

    # define target sequence
    sequence = Column(String)


ASSAYS = Enum('ADMET', 'Binding', 'Functional', 'Property', 'Unassigned',
              name='assay_type')

ACTIVITIES = Enum('Kd', 'AC50', 'Potency', 'XC50', 'IC50', 'Ki', 'EC50',
                  name='activity_type')

RELATIONS = Enum('=', '>', '<', '<=', '>=', name='relation')

class Activity(Base, ModelMixin):

    __tablename__ = 'activity'
    __repr_props__ = ['id', 'compound', 'relation', 'value']

    # internal id
    id = Column(Integer, Sequence('activity_id_seq'), primary_key=True, unique=True, nullable=False)

    # record origin
    external_id = Column(String, nullable=False)
    source_id = Column(Integer, ForeignKey('source.id'), nullable=False)
    source = relationship('Source')  # many to one, no map back

    # define the activity
    relation = Column(RELATIONS, nullable=False)
    value = Column(Float, nullable=False)
    assay_type = Column(ASSAYS, nullable=False)
    activity_type = Column(ACTIVITIES, nullable=False)
    confidence_score = Column(Integer, index=True)

    #Link to target
    target_id = Column(Integer, ForeignKey('target.id'), nullable=False)
    target = relationship('Target', backref='activities')

    #Link to compound
    compound_id = Column(Integer, ForeignKey('compound.id'), nullable=False)
    compound = relationship('Compound', backref='activities')

    def __repr__(self):
        return '<Activity(id=\'{id}\' compound=\'{compound}\' '\
               'target=\'{target}\' relation=\'{relation}{value}\')>'\
                    .format(id=self.id,
                            relation=self.relation,
                            target=self.target.external_id,
                            compound=self.compound.external_id,
                            value=self.value)
