from keras import Modelfrom keras.initializers import RandomNormalfrom keras.layers import Input, Dense, LSTM, CuDNNLSTM, Bidirectional, ReLU, BatchNormalization, TimeDistributeddef get_model(name, **kwargs):    if name == 'deepspeech-ctc':        return _get_deepspeech_ctc(**kwargs)def _get_deepspeech_ctc(is_gpu, input_dim=26, fc_sizes=[64], rnn_sizes=[64, 128, 256, 512, 1024],                        output_dim=36, random_seed=123, stddev=0.05):    input_tensor = Input([None, input_dim], name='X')    random = RandomNormal(stddev=stddev, seed=random_seed)    x = input_tensor    for fc_size in fc_sizes:        linear = _get_fc_layer(units=fc_size,                               init=random,                               activation='linear')        x = linear(x)        x = BatchNormalization(axis=-1)(x)        x = ReLU(max_value=20)(x)    for rnn_size in rnn_sizes:        rnn = _get_rnn_layer(is_gpu, units=rnn_size)        x = rnn(x)    softmax = _get_fc_layer(units=output_dim,                            init=random,                            activation='softmax')    output_tensor = softmax(x)    model = Model(input_tensor, output_tensor, name='DeepSpeech')    return modeldef _get_fc_layer(init, **kwargs):    params = dict(kernel_initializer=init,                  bias_initializer=init,                  **kwargs)    return TimeDistributed(Dense(**params))def _get_rnn_layer(is_gpu, **kwargs):    params = dict(kernel_initializer='glorot_uniform',                  return_sequences=True,                  return_state=False,                  **kwargs)    if is_gpu:        return Bidirectional(CuDNNLSTM(**params), merge_mode='sum')    else:        return Bidirectional(LSTM(**params), merge_mode='sum')