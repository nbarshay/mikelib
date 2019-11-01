from obvious import *

__all__ = ['Dataframe']


class Dataframe(object):
    def __init__(self, cols=None, n=None):
        object.__setattr__(self, '_df_n', n)
        object.__setattr__(self, '_df_cols', OrderedDict())
        if cols is not None:
            for k,v in cols.iteritems():
                self._addCol(k, v)

    @classmethod
    def fromRows(cls, rows):
        cols = [(k, np.array([x[k] for x in rows])) for k in funnel(x.keys() for x in rows)]
        return cls(dCreate(cols, t=OrderedDict), n=len(rows))

    ##################

    def __setattr__(self, k, v): self._addCol(k, v)
    def __getattr__(self, k): return self._getCol(k)
    def __setitem__(self, k, v): self._addCol(k,v)
    def __getitem__(self, k):
        if isinstance(k, (slice, np.ndarray)):
            return Dataframe(OrderedDict((a, b[k]) for a,b in self.items()))
        else:
            return self._getCol(k)

    def __delitem__(self, k):
        del self._df_cols[k]

    def __len__(self):
        assert self._df_n is not None
        return self._df_n

    def keys(self): return self._df_cols.keys()
    def values(self): return self._df_cols.values()
    def items(self): return self._df_cols.items()

    def __iter__(self): return self.keys()
    def contains(self, k): return k in self.keys()

    def __copy__(self):
        return Dataframe(OrderedDict(self.items()))
    def __deepcopy__(self, _memo):
        return Dataframe(OrderedDict((k, v.copy()) for k,v in self.items()))

    #########################
    def _addCol(self, k, v):
        assert isinstance(k, basestring)
        assert isinstance(v, np.ndarray) and (v.ndim == 1)
        if self._df_n is not None:
            assert v.size == self._df_n
        else:
            object.__setattr__(self, '_df_n', v.size)
        self._df_cols[k] = v

    def _getCol(self, k):
        return self._df_cols[k]

    def filter(self, mask):
        mask = np.array(mask)
        new_cols = {}
        for k,v in self.items():
            new_cols[k] = v[mask]
        return Dataframe(new_cols)
        
    #####################
    @classmethod
    def concat(cls, xs):
        res = cls()
        xs = list(xs)
        if xs:
            cols = funnel(x.keys() for x in xs)
            for col in cols:
                temp = [x[col] for x in xs]
                funnel(x.dtype for x in temp)
                res[col] = np.concatenate(temp)
        return res

    ###############
    def safeHdf5(self, path):
        with h5py.File(path, 'w') as f:
            for k,v in self.items():
                data = v.astype(np.string_) if v.dtype == np.object_ or v.dtype.type is np.unicode_ else v
                f.create_dataset(k, data=data)

    @staticmethod
    def loadHdf5(path):
        with h5py.File(path, 'r') as f:
            cols = OrderedDict([(k, v[:]) for k,v in f.iteritems()])
            n = funnel([v.shape[0] for v in f.itervalues()]) if len(f) else 0
            return Dataframe(cols, n)

    @staticmethod
    def loadNpz(path):
        raw = np.load(path)
        return Dataframe(dict(raw))
