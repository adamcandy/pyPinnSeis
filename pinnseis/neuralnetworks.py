#!/usr/bin/env python3

from .log import debug, report, error
import numpy as np
import tensorflow as tf
from .parameters import *

#### Neural nets
def xavier_init(size):
    in_dim = size[0]
    out_dim = size[1]        
    xavier_stddev = np.sqrt(2.0 / (in_dim + out_dim))
    return tf.Variable(
        tf.random.truncated_normal(
            [in_dim, out_dim],
            stddev=xavier_stddev,
            dtype=tf.float64
            ),
        dtype=tf.float64)


# Neural Network 1
def neural_net(X, weights, biases):
    num_layers = len(weights) + 1    
    ub = np.array([ax/Lx,az/Lz,(t_m-t_st)]).reshape(-1,1).T# normalization of the input to the NN
    # normalization map to [-1 1]
    H = 2 * ( X / ub ) - 1

    for l in range(0,num_layers-2): 
        W = weights[l]
        b = biases[l]
        H = tf.nn.tanh(tf.add(tf.matmul(H, W), b))

    W = weights[-1]
    b = biases[-1]
    Y = tf.add(tf.matmul(H, W), b)
    return Y

# Neural Network 2
def neural_net0(X, weights, biases):
    num_layers = len(weights) + 1    
    ub0 = np.array([ax/Lx,az/Lz]).reshape(-1,1).T#same for the inverse NN estimating the wave_speed 
    H = 2 * ( X / ub0 ) - 1

    for l in range(0,num_layers-2): 
        W = weights[l]
        b = biases[l]
        H = tf.nn.tanh(tf.add(tf.matmul(H, W), b))


    W = weights[-1] 
    b = biases[-1]
    Y = tf.add(tf.matmul(H, W), b)
    return Y


