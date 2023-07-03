## ----------------- helpers --------------------------- ##
from abc import ABC, abstractmethod

class HelperBase(ABC):
    # Abstract class defining helpers
    def __init__(self):
        """ """
    @abstractmethod
    def load_model(self, filename):
        pass

    @abstractmethod
    def save_model(self, model, filename):
        pass

    @abstractmethod
    def predict(self, model, x):
        pass

    @abstractmethod
    def update_model(self, model, train, validation):
        pass

def get_helper(helper_type):
    if helper_type == 'keras':
        return KerasHelper()
    else: 
        return None

class KerasHelper(HelperBase):

    def load_model(self, filename):
        from tensorflow import keras
        return keras.models.load_model(filename)

    def save_model(self, model, filename):
        model.save(filename, save_format='h5')

    def predict(self, model, x):
        return model.predict(x)

    def update_model(self, model, train, val):
        import numpy as np
        train_x, train_y = train
        val_x, val_y = val
        model.fit(train_x, train_y, epochs=10, batch_size=30, 
                validation_data=val, verbose=2, shuffle=False)
