#-*- coding:utf-8 -*-
import tensorflow as tf
from tensorflow.contrib import predictor
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import pdb
import traceback
import pickle
import logging
import multiprocessing
from functools import partial
import os,sys
ROOT_PATH = '/'.join(os.path.abspath(__file__).split('/')[:-2])
sys.path.append(ROOT_PATH)

from embedding import embedding
from encoder import encoder
from utils.data_utils import *
from tests.test import Test


class TestTranslation(Test):
    def __init__(self, conf, **kwargs):
        super(TestNER, self).__init__(conf, **kwargs)
        conf.update({
            "keep_prob": 1,
            "is_training": False
        })
        self.encoder = encoder[conf['encoder_type']](**conf)
        self.mp_label = pickle.load(open(self.label_path, 'rb'))

    def test_file(self, text):
        raise ValueError('no implemented')

    def test(self, text_list):
        text_list_pred, x_query, x_query_length = self.text2id(text_list,
                                                               need_preprocess = True)

        input_dict = {'seq_encode': x_query, 
                      'seq_encode_length': x_query_length}
        input_dict.update(self.encoder.encoder_fun(**input_dict))
        predictions = self.predict_fn(input_dict)
        scores = [item for item in predictions['pred']]
        max_scores = np.max(scores, axis = -1)
        max_ids = np.argmax(scores, axis = -1)
        ret =  zip(max_ids, max_scores)
        return ret

    def test_file(self, file):
        with open(file) as f_in, open(file+'.out.txt','w') as f_out:
            lines = f_in.readlines()
            lines = [line.strip() for line in lines]
            res = self.test(lines)
            for idx,line in enumerate(lines):
                f_out.write(line + "\t" + ' '.join(res[idx])+'\n')

    def __call__(self, text):
        text_list  = [text]
        return self.test(text_list)[0]

