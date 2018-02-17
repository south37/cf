import json
from sklearn.decomposition import NMF
import scipy.spatial.distance as dis

class Predictor:
    def __init__(self, y_list, y_features, x_list, x_features):
        self.y_features = zip(y_list, y_features)
        self.x_features = zip(x_list, x_features)

        # NOTE: used to get feature quickly
        self.y_dict = dict(zip(y_list, y_features))
        self.x_dict = dict(zip(x_list, x_features))

    def do_command(self, cmd, args):
        if args:
            a = json.loads(args)
        else:
            a = {}
        if cmd == "get_y_feature":
            return self.get_y_feature(a)
        if cmd == "get_x_feature":
            return self.get_x_feature(a)
        if cmd == "get_y_features":
            return self.get_y_features(a)
        if cmd == "get_x_features":
            return self.get_x_features(a)
        if cmd == "get_similar_y_list":
            return self.get_similar_y_list(a)
        if cmd == "get_similar_x_list":
            return self.get_similar_x_list(a)

        # NOTE: must not reache here
        raise Exception("invalid cmd: {}".format(cmd))

    def get_y_feature(self, args):
        y = args["y"]
        return self.get_feature(v_dict=self.y_dict, v=y, v_s="y")

    def get_x_feature(self, args):
        x = args["x"]
        return self.get_feature(v_dict=self.x_dict, v=x, v_s="x")

    def get_y_features(self, args):
        num = self.num_from(args)
        return list(self.y_features)[:num]

    def get_x_features(self, args):
        num = self.num_from(args)
        return list(self.x_features)[:num]

    def get_similar_y_list(self, args):
        y   = args["y"]
        num = self.num_from(args)
        return self.get_similar_list(
                v_dict=self.y_dict,
                v_features=self.y_features,
                v=y,
                v_s="y",
                num=num)

    def get_similar_x_list(self, args):
        x   = args["x"]
        num = self.num_from(args)
        return self.get_similar_list(
                v_dict=self.x_dict,
                v_features=self.x_features,
                v=x,
                v_s="x",
                num=num)

    # NOTE: 10 is just default value
    def num_from(self, args):
        if "num" in args:
            return int(args["num"])
        else:
            return 10

    def get_feature(self, v_dict, v, v_s):
        if v not in v_dict:
            raise Exception("{}_list is not including {}: {}".format(v_s, v_s, v))
        return v_dict[v]

    def get_similar_list(self, v_dict, v_features, v, v_s, num):
        feature = self.get_feature(v_dict=v_dict, v=v, v_s=v_s)
        distances = [(e[0], self.similarity(e[1], feature)) for e in v_features]
        distances.sort(key=lambda d: d[1])
        return distances[1:num + 1]

    def similarity(self, v1, v2):
        return dis.cosine(v1, v2)
