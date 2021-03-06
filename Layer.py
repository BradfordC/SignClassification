import numpy as np
import Functions

class Layer:
    def __init__(self, size, nextLayerSize, activationMode="Sigmoid"):
        self.Size = size
        self.NodeCount = size + 1

        self.Values = np.zeros(self.Size)
        self.Activations = np.zeros(self.NodeCount)
        self.Weights = np.zeros(shape=(nextLayerSize, self.NodeCount))

        self.Mode = activationMode

    def RandomizeWeights(self):
        for row in range(0, self.Weights.shape[0]):
            for column in range(0, self.Weights.shape[1]):
                self.Weights[row,column] = np.random.normal(0, .01)

    #def GetWeightsWithoutBias(self):

    def Feedforward(self, values):
        if(self.Values.size != values.size):
            print("Input size didn't match: {} vs {}".format(self.Values.size, values.size))
            return

        self.Values = values.copy()
        self.__Activate()
        Output = np.dot(self.Weights, self.Activations)
        return Output

    def MakeDeltas(self, nextLayerDeltas):
        weightsWithoutBias = self.Weights[:,:-1]
        temp = np.dot(nextLayerDeltas.transpose(),weightsWithoutBias)
        deltas = self.__GetDerivatives() * temp
        return deltas


    def __GetDerivatives(self):
        derivatives = np.zeros(self.Size)

        if self.Mode == "Linear":
            derivatives.fill(1)

        if self.Mode == "Sigmoid":
            for i in range(0, derivatives.size):
                derivatives[i] = self.Activations[i]*(1-self.Activations[i])

        if self.Mode == "ReLU":
            for i in range(0, derivatives.size):
                derivatives[i] = 0 if self.Activations[i] == 0 else 1

        return derivatives


    def __Activate(self):
        if self.Mode == "Linear":
            for i in range(0, self.Values.size):
                self.Activations[i] = self.Values[i]

        if self.Mode == "Sigmoid":
            for i in range(0, self.Values.size):
                self.Activations[i] = Functions.Sigmoid(self.Values[i])

        if self.Mode == "ReLU":
            for i in range(0, self.Values.size):
                self.Activations[i] = max(self.Values[i], 0)

        # Bias node
        self.Activations[-1] = 1