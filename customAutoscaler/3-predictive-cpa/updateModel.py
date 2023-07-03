from pandas import read_csv, DataFrame
import time
import joblib
import os
from helpers import get_helper

def data_read(filename):
    return read_csv(filename, header=None).values.astype("float32")

def series_to_supervised(data, n_in=1, n_out=1):
    agg = []
    for i in range(data.shape[0] - n_in - n_out + 1):
        agg.append(list(data[i: i+n_in+n_out, :].flatten()))
    agg = DataFrame(agg)
    return agg.values

def formulate(data, n_feature):
    data_x, data_y = data[:, :n_feature], data[:, n_feature:]
    return data_x.reshape(data_x.shape[0], 1, data_x.shape[1]), data_y


def train_model(model, train_set, val_set, epoch=1, batch_size=30):
    train_x, train_y = train_set
    model.fit(train_x, train_y, epochs=epoch, batch_size=batch_size,
              validation_data=val_set, verbose=2, shuffle=False)

def update_model(helper):
    n_feature = 5
    data = data_read('/metrics_log.csv')
    if (len(data) < 20):
        raise Exception("No enough data") 
    train_samples = int(0.75 * (data.shape[0]))
    train = data[0:train_samples, :]
    test = data[train_samples:, :]

    scaler = joblib.load('/model_dir/scaler')
    model = helper.load_model('/model_dir/model')

    train = series_to_supervised(scaler.transform(train))
    test = series_to_supervised(scaler.transform(test))

    train_x, train_y = formulate(train, n_feature)
    test_x, test_y = formulate(test, n_feature)

    helper.update_model(model, (train_x, train_y), (test_x, test_y))
    helper.save_model(model, '/model_dir/model')
    os.remove('/metrics_log.csv')

while True:
    helper = get_helper(os.environ['ModelType'])
    try:
        update_model(helper)
        message = 'model updated\n'
    except Exception as e:
        message = str(e) + '\n'
    with open('/modelUpdate.log', 'a+') as f:
        f.write(message)
    time.sleep(60*20)
