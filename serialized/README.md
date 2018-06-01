# CHI-PG (Serialized Implementation)

#### Input file should be named "data.csv".

#### If the first column of the database file is the class label, set the global variable CLASS_LABEL_ON_FIRST_COLUMN to True on both "preprocess.py" and "chi-pg.py" files. Otherwise, it will be assumed that the class label is on the last column.

#### First, run "preprocess.py", in order to generate the "header.csv" file.

```
$ python3 preprocess.py
```

#### Then, run "chi-pg.py", in order to generate the "output.csv" file.

```
$ python3 chi-pg.py
```

#### Config parameters are set as global variables on "chi-pg.py" file.
