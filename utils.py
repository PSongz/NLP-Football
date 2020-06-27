#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
def save(obj, name, path ):
    with open(path+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load(name ,path):
    with open(path + name + '.pkl', 'rb') as f:
        return pickle.load(f)

