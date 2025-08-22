import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split

n = 1000 # Number of samples

# Create circles and split into train and test sets
X, y = make_circles(n, noise=0.03)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Reshape arrays for future convenience
X_train = X_train.T
X_test = X_test.T
y_train = y_train.reshape(1,-1)
y_test = y_test.reshape(1,-1)

def ReLU(X):
  """Defines the ReLU activation function"""
  return np.maximum(0,X)

def sigmoid(X):
  """Defines the sigmoid activation function"""
  return 1 / (1 + np.exp(-X))

def forward_pass(X, W1, b1, W2, b2):
  """Returns the prediction probabilities and the hidden layer units A1"""
  Z1 = W1 @ X + b1
  A1 = ReLU(Z1)
  Z2 = W2 @ A1 + b2
  A2 = sigmoid(Z2)
  return A1, A2

def BCEloss(pred, y):
  """Defines the binary cross entropy loss function"""
  return -np.mean(y * np.log(pred) + (1 - y) * np.log(1 - pred))

def accuracy_fn(pred_prob, y):
  """Returns the accuracy of predictions compared to true labels"""
  y = y.flatten()
  y_pred = np.round(pred_prob).flatten()
  correct = np.sum(np.equal(y_pred, y))
  acc = (correct/len(y))*100
  return acc

def backpropagation(A1, A2, W1, b1, W2, b2, X, y, n, lr):
  """Performs backpropagation and updates parameters accordingly"""
  # Calculate derivatives
  dZ2 = A2 - y
  dW2 = dZ2 @ A1.T / n
  db2 = np.sum(dZ2, axis=1, keepdims=True) / n

  dZ1 = (W2.T @ dZ2) * (A1 > 0)
  dW1 = dZ1 @ X.T / n
  db1 = np.sum(dZ1, axis=1, keepdims=True) / n

  # Update parameters through gradient descent
  W1 -= lr * dW1
  b1 -= lr * db1
  W2 -= lr * dW2
  b2 -= lr * db2

  return W1, b1, W2, b2

def initialize_parameters(input_shape, hidden_units, output_shape):
    """Initializes weights random values and biases with zeros"""
    W1 = np.random.randn(hidden_units, input_shape) * 0.1
    b1 = np.zeros((hidden_units, 1))
    W2 = np.random.randn(output_shape, hidden_units) * 0.1
    b2 = np.zeros((output_shape, 1))
    return W1, b1, W2, b2

def plot_decision_boundary(X, y, epoch, acc, test_acc, params):
    """Plots decision boundary of model for current epoch"""

    plt.cla()
    x_min, x_max = X[0, :].min() - 0.1, X[0, :].max() + 0.1
    y_min, y_max = X[1, :].min() - 0.1, X[1, :].max() + 0.1
    h = 0.01

    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    Z = np.round(forward_pass(np.c_[xx.ravel(), yy.ravel()].T, *params)[-1])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.scatter(X[0, :], X[1, :], c=y, cmap=plt.cm.Spectral, s=8)
    plt.ylabel('x2')
    plt.xlabel('x1')
    plt.suptitle(f'Decision Boundary Plot for NumPy Neural Network\nEpoch: {epoch} | Accuracy: {acc:.2f}% | Test Accuracy: {test_acc:.2f}%')
    plt.xlim(-1.1,1.1)
    plt.ylim(-1.1,1.1)
    plt.gca().set_aspect("equal")

def train(X, y, X_test, y_test, epochs, lr):
  """Trains the model on training data, calculates test/train loss and accuracy, and plots decision boundary"""
  W1, b1, W2, b2 = initialize_parameters(2, 16, 1)

  for epoch in range(epochs):
    A1, A2 = forward_pass(X, W1, b1, W2, b2)
    W1, b1, W2, b2 = backpropagation(A1, A2, W1, b1, W2, b2, X, y, n, lr)
    if epoch % 100 == 0:
      loss = BCEloss(A2, y)
      acc = accuracy_fn(A2, y)

      _, A2_test = forward_pass(X_test, W1, b1, W2, b2)
      test_loss = BCEloss(A2_test, y_test)
      test_acc = accuracy_fn(A2_test, y_test)

      print(f"Epoch: {epoch} | Loss: {loss:.5f}, Accuracy: {acc:.2f}% | Test Loss: {test_loss:.5f}, Test Accuracy: {test_acc:.2f}%")
      
      plot_decision_boundary(X, y, epoch, acc, test_acc, (W1, b1, W2, b2))
      plt.pause(0.1)

  return W1, b1, W2, b2

W1, b1, W2, b2 = train(X_train, y_train, X_test, y_test, epochs=10000, lr=0.1)
plt.show()
