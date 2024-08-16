import numpy as np
import pytest
from malo import sigmoid, sigmoid_derivative, xavier_init, train_model

def test_sigmoid():
    assert np.isclose(sigmoid(0), 0.5)
    assert np.isclose(sigmoid(100), 1.0)
    assert np.isclose(sigmoid(-100), 0.0)

def test_sigmoid_derivative():
    x = np.array([0.5])
    assert np.isclose(sigmoid_derivative(x), 0.25)

def test_xavier_init():
    n_inputs, n_outputs = 10, 5
    weights = xavier_init(n_inputs, n_outputs)
    assert weights.shape == (n_inputs, n_outputs)
    assert -0.5 < np.mean(weights) < 0.5  # Check if mean is close to 0
    assert 0 < np.std(weights) < 1  # Check if std dev is reasonable

def test_train_model():
    hidden1_weights, hidden1_bias, hidden2_weights, hidden2_bias, output_weights, output_bias, output_layer, error = train_model(epochs=1000, lr=0.1, hidden_neurons=4, momentum=0.9)
    
    # Check shapes
    assert hidden1_weights.shape == (2, 4)
    assert hidden1_bias.shape == (1, 4)
    assert hidden2_weights.shape == (4, 4)
    assert hidden2_bias.shape == (1, 4)
    assert output_weights.shape == (4, 1)
    assert output_bias.shape == (1, 1)
    assert output_layer.shape == (4, 1)
    assert error.shape == (4, 1)

    # Check if error is decreasing
    assert np.mean(np.abs(error)) < 0.5

def test_model_accuracy():
    _, _, _, _, _, _, output_layer, _ = train_model(epochs=10000, lr=0.1, hidden_neurons=8, momentum=0.9)
    expected_output = np.array([[0], [1], [1], [0]])
    predictions = (output_layer > 0.5).astype(int)
    accuracy = np.mean(predictions == expected_output)
    assert accuracy > 0.75  # At least 75% accuracy

if __name__ == "__main__":
    pytest.main()