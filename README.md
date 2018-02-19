## cf
Command line tool for using collaborative filtering.
By specifing the table name, "Train" and "predict" of collaborative filtering can be done.

## Setup
### 1. Clone repository

```
$ git clone git@github.com:south37/cf.git path/to/workdir && cd path/to/workdir
```

### 2. Instll necessary packages

```
$ pip install -r requirements.txt
```

### 3. Create .env

```
$ cp .env{.sample,}
```

### 4 Create cf_features table
`cf_features` table is used for storing feature vectors.

```
$ python src/setup.py
Running create table query...

CREATE TABLE cf_features (
    id         integer PRIMARY KEY,
    key        text    NOT NULL,
    y_list     text    NOT NULL,
    y_features text    NOT NULL,
    x_list     text    NOT NULL,
    x_features text    NOT NULL
);
CREATE INDEX index_cf_features_on_key ON cf_features (key);

Finish creation of cf_features table!
```


## Usage

### train

```
$ bin/train --src user_company_applications --x user_id --y company_id --n 10
```

### predict

```
$ bin/predict --src user_company_applications --cmd get_similar_y_list --args '{"y":"1"}'
```

## bin/train
Perform training.

Input is a table which has three columns "column corresponding to `x`", "column corresponding to `y`", and "column corresponding to `v`", and the input table name is specified as the` src` parameter.
Note that `v` can be omitted, in which case `score` treats `1.0` for all `x`, `y` combinations.

The result is output to the `cf_features` table. The output is contained in one record, the value contained in `x`, `y` of `src` is outputted to the `x_list`, `y_list` column as csv. The `feature vector` corresponding to the element is output to` x_features`, `y_features` as csv.

By passing `n` as an option, you can specify the dimension of the feature vector. The default is `10`.

```
$ bin/train --src user_company_applications --x user_id --y company_id --n 10
```

### train example

```
$ bin/train --src user_company_applications --x user_id --y company_id --n 10
Start fetching matrix from 'user_company_applications'...
Running query...

SELECT
    company_id,  -- y
    user_id   -- x
FROM
    user_company_applications   -- src

Finish query
Finish fetching matrix from 'user_company_applications'
Start matrix facterization of 'user_company_applications' with n_components = 10...
Finish matrix facterization!
Train result: reconstruction_err_: 278.15579552829183, n_iter_: 307
Start saving the features with key = 'user_company_applications'...
Finish saving the features!
```

## bin/predict
Perform predict.

As `src`, specify the table name passed in when training and pass the operation you want to do to `cmd`. Specify the parameter in JSON format to `args`, but note that `args` does not allow spaces in it.

Following are supported as operations.

- `get_y_feature`: Return the feature vector of `y` (parameter: `{"y":y}`).
- `get_x_feature`: Return the feature vector of `x` (parameter: `{"x":x}`).
- `get_similar_y_list`: Return a list of `y` with a score (the smaller the better) similar to passed `y` (parameter: `{"y":y}`).
- `get_similar_x_list`: Return a list of `x` with a score (the smaller the better) similar to passed `x` (parameter: `{"x":x}`).

```
$ bin/predict --src user_company_applications --cmd get_similar_y_list --args '{"y":"1"}'
```

### predict example

```
$ bin/predict --src user_company_applications --cmd get_similar_y_list --args '{"y":"1"}'
Start loading the features with key = 'user_company_applications'...
Finish loading the features with key = 'user_company_applications'
Start predict...
get_similar_y_list result is below:
[('319768', 0.002005959182745598), ('244218', 0.0071734535927241438), ('253963', 0.017882362219602488), ('160599', 0.018516475884152284), ('78', 0.055577606194376017), ('153318', 0.070644829256075625), ('16520', 0.081771456965424427), ('26', 0.12736032704778832), ('18829', 0.12942517812058818), ('167', 0.13339359123428551)]
Finish predict
```
