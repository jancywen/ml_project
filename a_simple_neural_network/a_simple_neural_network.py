# -*- coding: utf-8 -*-
"""
    用numpy构建一个简单的神经网络

"""

import numpy as np

# 层级结构
nn_architecture = [
    {'input_dim': 2, 'output_dim': 4, 'activation': 'relu'},
    {'input_dim': 4, 'output_dim': 6, 'activation': 'relu'},
    {'input_dim': 6, 'output_dim': 6, 'activation': 'relu'},
    {'input_dim': 6, 'output_dim': 4, 'activation': 'relu'},
    {'input_dim': 4, 'output_dim': 1, 'activation': 'relu'},
]


# 初始化层
def init_layers(nn_architecture, seed = 42):
    np.random.seed(seed)

    number_of_layers = len(nn_architecture)
    params_values = {}

    for idx, layer in enumerate(nn_architecture):
       layer_idx = idx + 1
       layer_input_size = layer['input_dim']
       layer_output_size = layer['output_dim']

       params_values['W' + str(layer_idx)] = np.random.randn(layer_output_size, layer_input_size) * 0.1
       params_values['b' + str(layer_idx)] = np.random.randn(layer_output_size) * 0.1

    return params_values


# 激活函数
def sigmoid(z):
    return 1/(1+np.exp(-z))


def relu(z):
    return np.maximum(0, z)


def sigmoid_backward(dA, z):
    sig = sigmoid(z)
    return dA * sig * (1 - sig)


def relu_backward(dA, z):
    dz = np.array(dA, copy=True)
    dz[z <= 0] = 0
    return dz


# 前向传播
# 单层前向传播
def single_layer_forward_propagation(A_prev, w_curr, b_curr, activation='relu'):
    z_curr = np.dot(w_curr, A_prev) + b_curr

    if activation == 'relu':
        activation_func = relu
    elif activation == 'sigmoid':
        activation_func = sigmoid
    else:
        raise Exception('Non-sport activation function')
    return activation_func(z_curr), z_curr


# 全层前向传播
def full_layer_forward_propagation(X, params_values, nn_architecture):

    memory = {}
    A_curr = X

    for idx, layer in enumerate(nn_architecture):
        layer_idx = idx + 1
        A_prev = A_curr

        activation = layer['activation']
        w_curr = params_values['W' + str(layer_idx)]
        b_curr = params_values['b' + str(layer_idx)]

        A_curr, z_curr = single_layer_forward_propagation(A_prev, w_curr, b_curr, activation)

        memory['A' + str(idx)] = A_prev
        memory['z' + str(idx)] = z_curr

    return A_curr, memory


# 损失函数  交叉熵
def get_cost_value(Y_hat, Y):
    m = Y_hat.shape[1]
    cost = -1/m * (np.dot(Y, np.log(Y_hat).T) + np.dot(1-Y, np.log(1-Y_hat).T))
    return np.squeeze(cost)

#
def convert_prob_into_class(probs):
    probs_ = np.copy(probs)
    probs_[probs_ > 0.5] = 1
    probs_[probs_ <= 0.5] = 0
    return probs_

# 准确率
def get_accuracy_value(Y_hat, Y):
    Y_hat_ = convert_prob_into_class(Y_hat)
    return  (Y_hat_ == Y).all(axis=0).mean()


# 反向传播
def single_layer_backward_propagation(dA_ccurr, W_curr, b_curr, z_curr, A_prev, activation='relu'):
    m = A_prev.shape[1]
    if activation is 'relu':
        backward_activation_func = relu_backward
    elif activation is'sigmoid':
        backward_activation_func = sigmoid_backward
    else:
        raise Exception('Non-supported activation function')

    dz_curr = backward_activation_func(dA_ccurr, z_curr)
    dW_curr = np.dot(dz_curr, A_prev.T) / m
    db_curr = np.sum(dz_curr, axis=1, keepdims=True) / m
    dA_prev = np.dot(W_curr.T, dz_curr)

    return dA_prev, dW_curr, db_curr


def full_backward_propagation(Y_hat, Y, memory, params_values, nn_architecture):
    gards_values = {}
    m = Y.shape[1]
    Y = Y.reshape(Y_hat.shape)
    dA_prev = - (np.divide((Y, Y_hat) - np.divide(1 - Y, 1 - Y_hat)))

    for layer_idx_prev, layer in reversed(list(enumerate(nn_architecture))):
        layer_idx_curr = layer_idx_prev + 1
        activ_function_curr = layer['activation']

        dA_curr = dA_prev

        A_prev = memory['A' + str(layer_idx_prev)]
        z_curr = memory['z' + str(layer_idx_curr)]
        W_curr = params_values['W' + str(layer_idx_curr)]
        b_curr = params_values['b' + str(layer_idx_curr)]

        dA_prev, dW_curr, db_curr = single_layer_backward_propagation(dA_curr, W_curr, b_curr, z_curr, A_prev, activ_function_curr)

        gards_values['dW' + str(layer_idx_curr)] = dW_curr
        gards_values['db' + str(layer_idx_curr)] = db_curr

    return gards_values


# 更新参数
def update(params_value, grads_values, nn_architecture, learning_rate):

    for idx, layer in enumerate(nn_architecture):
        layer_idx = idx + 1
        params_value['W' + str(layer_idx)] -= learning_rate * grads_values['dW' + str(layer_idx)]
        params_value['b' + str(layer_idx)] -= learning_rate * grads_values['db' + str(layer_idx)]

    return params_value


# 训练

def train(X, Y, nn_architecture, epochs, learning_rate):
    params_values = init_layers(nn_architecture, 2)

    cost_history = []
    accuracy_history = []

    for i in range(epochs):
        Y_hat, cashe = full_layer_forward_propagation(X, params_values, nn_architecture)
        cost = get_cost_value(Y_hat, Y)
        cost_history.append(cost)
        accuracy = get_accuracy_value(Y_hat, Y)
        accuracy_history.append(accuracy)

        grads_values = full_backward_propagation(Y_hat, Y, cashe, params_values, nn_architecture)
        params_values = update(params_values, grads_values, nn_architecture, learning_rate)

        return params_values, cost_history, accuracy_history