import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(x))

def sigmoid_derivative(x):
    return x * (1 - x)

def xavier_init(n_inputs, n_outputs):
    limit = np.sqrt(6 / (n_inputs + n_outputs))
    return np.random.uniform(-limit, limit, (n_inputs, n_outputs))

def train_model(epochs=100000, lr=0.01, hidden_neurons=8, momentum=0.9):
    # Input dataset
    inputs = np.array([[0, 0], [0, 1], [1, 0], [0, 1]])
    expected_output = np.array([[0], [1], [0]])

    inputLayerNeurons, hiddenLayer1Neurons, hiddenLayer2Neurons, outputLayerNeurons = 2, hidden_neurons, hidden_neurons, 1

    # Xavier initialization
    hidden1_weights = xavier_init(inputLayerNeurons, hiddenLayer1Neurons)
    hidden1_bias = np.zeros((1, hiddenLayer1Neurons))
    hidden2_weights = xavier_init(hiddenLayer1Neurons, hiddenLayer2Neurons)
    hidden2_bias = np.zeros((1, hiddenLayer2Neurons))
    output_weights = xavier_init(hiddenLayer2Neurons, outputLayerNeurons)
    output_bias = np.zeros((1, outputLayerNeurons))

    # Initialize momentum
    v_hidden1_weights, v_hidden1_bias = np.zeros_like(hidden1_weights), np.zeros_like(hidden1_bias)
    v_hidden2_weights, v_hidden2_bias = np.zeros_like(hidden2_weights), np.zeros_like(hidden2_bias)
    v_output_weights, v_output_bias = np.zeros_like(output_weights), np.zeros_like(output_bias)

    best_error = float('inf')
    patience = 1000
    patience_counter = 0

    for _ in range(epochs):
        # Forward Propagation
        hidden_layer1 = sigmoid(np.dot(inputs, hidden1_weights) + hidden1_bias)
        hidden_layer2 = sigmoid(np.dot(hidden_layer1, hidden2_weights) + hidden2_bias)
        output_layer = sigmoid(np.dot(hidden_layer2, output_weights) + output_bias)

        # Backpropagation
        error = expected_output - output_layer
        d_output = error * sigmoid_derivative(output_layer)
        
        error_hidden_layer2 = d_output.dot(output_weights.T)
        d_hidden_layer2 = error_hidden_layer2 * sigmoid_derivative(hidden_layer2)

        error_hidden_layer1 = d_hidden_layer2.dot(hidden2_weights.T)
        d_hidden_layer1 = error_hidden_layer1 * sigmoid_derivative(hidden_layer1)

        # Updating Weights and Biases with momentum
        v_output_weights = momentum * v_output_weights + lr * hidden_layer2.T.dot(d_output)
        v_output_bias = momentum * v_output_bias + lr * np.sum(d_output, axis=0, keepdims=True)
        v_hidden2_weights = momentum * v_hidden2_weights + lr * hidden_layer1.T.dot(d_hidden_layer2)
        v_hidden2_bias = momentum * v_hidden2_bias + lr * np.sum(d_hidden_layer2, axis=0, keepdims=True)
        v_hidden1_weights = momentum * v_hidden1_weights + lr * inputs.T.dot(d_hidden_layer1)
        v_hidden1_bias = momentum * v_hidden1_bias + lr * np.sum(d_hidden_layer1, axis=0, keepdims=True)

        output_weights += v_output_weights
        output_bias += v_output_bias
        hidden2_weights += v_hidden2_weights
        hidden2_bias += v_hidden2_bias
        hidden1_weights += v_hidden1_weights
        hidden1_bias += v_hidden1_bias

        # Early stopping
        current_error = np.mean(np.abs(error))
        if current_error < best_error:
            best_error = current_error
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= patience:
                break

    return hidden1_weights, hidden1_bias, hidden2_weights, hidden2_bias, output_weights, output_bias, output_layer, error

def test_train_model():
    # Run the model training with new parameters
    hidden1_weights, hidden1_bias, hidden2_weights, hidden2_bias, output_weights, output_bias, output_layer, error = train_model(epochs=100000, lr=0.01, hidden_neurons=8, momentum=0.9)