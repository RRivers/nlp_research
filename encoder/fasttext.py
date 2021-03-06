#-*- coding:utf-8 -*-
import tensorflow as tf
from encoder import EncoderBase
import pdb
import copy

class FastText(EncoderBase):
    def __init__(self, **kwargs):
        """
        :param config:
        """
        super(FastText, self).__init__(**kwargs)
        self.embedding_dim = kwargs['embedding_size']
        self.placeholder = {}

    def __call__(self, embed, name = 'encoder', features = None, reuse = tf.AUTO_REUSE, **kwargs):
        with tf.variable_scope("fast_text", reuse = reuse):
            #embed: [batch_size, self.maxlen, embedding_size]
            length = tf.placeholder(tf.int32, name=name + '_length',shape=[])
            if features != None:
                length = features[name + '_length']
            #pdb.set_trace()
            #mask:[batch_size, self.maxlen]
            mask = tf.sequence_mask(length, self.maxlen, tf.float32)
            mask = tf.expand_dims(mask, -1)
            embed = embed*mask
            mean_sentence = tf.reduce_mean(embed, axis=1)
            logits = tf.layers.dense(mean_sentence,
                                    self.num_output,
                                    kernel_regularizer=tf.contrib.layers.l2_regularizer(0.001),
                                    name='fc',
                                    reuse = reuse)
            return logits

    def get_features(self, name = 'encoder'):
        features = {}
        length_name = name+'_length'
        features[length_name] = tf.placeholder(tf.int32, name=name + '_length',shape=[])
        return features
