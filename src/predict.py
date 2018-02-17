import argparse
from feature_storage import FeatureStorage
from predictor import Predictor

parser = argparse.ArgumentParser(description='Predict by using collaborative filtering')
parser.add_argument('--src', help='table name used for creating matrix', required=True)
parser.add_argument('--cmd', help='command name', required=True)
parser.add_argument('--args', help='arguments for command')
args = parser.parse_args()
src = args.src

print("Start loading the features with key = '{}'...".format(src))
y_list, y_features, x_list, x_features = FeatureStorage().load(src)
print("Finish loading the features with key = '{}'".format(src))

print("Start predict...")
predictor = Predictor(
        y_list=y_list,
        y_features=y_features,
        x_list=x_list,
        x_features=x_features
        )
print("{} result is below:".format(args.cmd))
result = predictor.do_command(cmd=args.cmd, args=args.args)
print(result)
print("Finish predict")
