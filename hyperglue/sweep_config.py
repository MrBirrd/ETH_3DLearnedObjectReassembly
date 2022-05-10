metric = {
    "name": 'total',
    "goal": 'minimize'
}

sweep_config = {'method': 'bayes'}

terminator = {
    "type": 'hyperband',
    "min_iter": 1000
}

param_dict = {
    'learning_rate': {
        'distribution': 'uniform',
        'min': 1e-4,
        'max': 1e-3
    },
    'optimizer': {
        'values': ["adam", "rmsprop"]
    },
    'sinkhorn_iterations': {
        'distribution': 'uniform',
        'min': 100,
        'max': 500
    },
    'num_heads': {
        'values': [4, 6, 9]},
    'sep_encoder': {
        'values': [True, False]},
    'use_sd_score': {
        'values': [False]},
    'match_threshold': {
        'distribution': 'uniform',
        'min': 0.2,
        'max': 0.4
    },
    'pillar': {
        'values': [True]},
    'match_inverted': {
        'values': [False]},
    'nll_balancing': {
        'distribution': 'uniform',
        'min': 0.9,
        'max': 0.99
    },

    'GNN_layers': {
        'values': [2, 3, 4]},
    'keypoint_encoder': {
        'values': [
            [8, 16, 32, 64],
            [8, 32, 64, 128],
        ]}
}

sweep_config['metric'] = metric
sweep_config['parameters'] = param_dict
sweep_config['early_terminate'] = terminator
