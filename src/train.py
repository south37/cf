import argparse
from src_storage import SrcStorage
from feature_storage import FeatureStorage
from trainer import Trainer

parser = argparse.ArgumentParser(description='Do training of collaborative filtering')
parser.add_argument('--src', help='table name used for creating matrix', required=True)
parser.add_argument('--x', default='x', help='colun name used as x of matrix')
parser.add_argument('--y', default='y', help='colun name used as y of matrix')
parser.add_argument('--v', help='colun name used as v of matrix')
parser.add_argument('--n', type=int, default=10, help='length of feature vector')
args = parser.parse_args()
src = args.src

print("Start fetching matrix from '{}'...".format(src))
matrix, y_list, x_list = SrcStorage().fetch_matrix(src=src, x=args.x, y=args.y, v=args.v)
print("Finish fetching matrix from '{}'".format(src))

print("Start matrix facterization of '{}' with n_components = {}...".format(src, args.n))
trainer = Trainer(matrix=matrix, n_components=args.n)
y_features, x_features = trainer.fit()
print("Finish matrix facterization!")
print("Train result: reconstruction_err_: {}, n_iter_: {}".format(trainer.reconstruction_err_, trainer.n_iter_))

print("Start saving the features with key = '{}'...".format(src))
FeatureStorage().save(
        key=src,
        y_list=y_list,
        y_features=y_features,
        x_list=x_list,
        x_features=x_features)
print("Finish saving the features!")
