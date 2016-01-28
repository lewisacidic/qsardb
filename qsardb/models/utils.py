
class ModelMixin(object):

    def __repr__(self):
        props = [(prop, self.__dict__.get(prop)) for prop in self.__repr_props__]
        props = ['{k}=\'{v}\''.format(k=k, v=v) for k, v in props]
        klass = self.__class__.__name__
        props = ', '.join(props)
        return '<{k}({ps})>'.format(k=klass, ps=props)
