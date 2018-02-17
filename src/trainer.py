from sklearn.decomposition import NMF

class Trainer:
    def __init__(self, matrix, n_components):
        self.matrix       = matrix
        self.n_components = n_components
        self.model        = NMF(n_components=self.n_components, init='random', max_iter=1000)

        # NOTE: updated by fit
        self.y_features          = None
        self.x_features          = None
        self.reconstruction_err_ = None
        self.n_iter_             = None

    def fit(self):
        self.y_features          = self.model.fit_transform(self.matrix)
        self.x_features          = self.model.components_.T
        self.reconstruction_err_ = self.model.reconstruction_err_
        self.n_iter_             = self.model.n_iter_
        return self.y_features, self.x_features
