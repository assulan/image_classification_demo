import cPickle
import numpy
import theano
import theano.tensor as T

from trained_models.code.normalize import normalize
from models import LogisticRegression, LeNetConvPoolLayer, HiddenLayer

LOG_REG = 'logistic_regression'
CONV_MLP = 'convolutional_mlp'


def _logistic_regression(new_digit):
    """
    Classify new_digit using pretrained model
    """
    ###############
    # BUILD MODEL #
    ###############
    print '... building the model'
    # construct the logistic regression class
    # Each MNIST image has size 28*28
    new_digit = new_digit.reshape((1, new_digit.shape[0]))
    classifier = LogisticRegression(input=new_digit, n_in=28 * 28, n_out=10)
    predict = theano.function(inputs=[], outputs=classifier.y_pred)

    ###############
    # TRAIN MODEL #
    ###############
    print '... loading trained the model'
    f = file('trained_models/models/logistic_sgd.mnist.trained.W.pickle', 'rb')
    W = cPickle.load(f)
    f.close()
    f = file('trained_models/models/logistic_sgd.mnist.trained.b.pickle', 'rb')
    b = cPickle.load(f)
    f.close()
    # Set the values
    classifier.W.set_value(W)
    classifier.b.set_value(b)
    return predict()[0]


def _convolutional_mlp(new_digit, nkerns=[20, 50], batch_size=1):
    rng = numpy.random.RandomState(23455)

    # allocate symbolic variables for the data
    index = T.lscalar()  # index to a [mini]batch

    # start-snippet-1
    x = T.matrix('x')   # the data is presented as rasterized images
    y = T.ivector('y')  # the labels are presented as 1D vector of
                        # [int] labels

    ######################
    # BUILD ACTUAL MODEL #
    ######################
    print '... building the model'

    # Reshape matrix of rasterized images of shape (batch_size, 28 * 28)
    # to a 4D tensor, compatible with our LeNetConvPoolLayer
    # (28, 28) is the size of MNIST images.
    #layer0_input = x.reshape((batch_size, 1, 28, 28))
    layer0_input = new_digit.reshape((1, 1, 28, 28))

    # Construct the first convolutional pooling layer:
    # filtering reduces the image size to (28-5+1 , 28-5+1) = (24, 24)
    # maxpooling reduces this further to (24/2, 24/2) = (12, 12)
    # 4D output tensor is thus of shape (batch_size, nkerns[0], 12, 12)
    layer0 = LeNetConvPoolLayer(
        rng,
        input=layer0_input,
        image_shape=(batch_size, 1, 28, 28),
        filter_shape=(nkerns[0], 1, 5, 5),
        poolsize=(2, 2)
    )

    # Construct the second convolutional pooling layer
    # filtering reduces the image size to (12-5+1, 12-5+1) = (8, 8)
    # maxpooling reduces this further to (8/2, 8/2) = (4, 4)
    # 4D output tensor is thus of shape (batch_size, nkerns[1], 4, 4)
    layer1 = LeNetConvPoolLayer(
        rng,
        input=layer0.output,
        image_shape=(batch_size, nkerns[0], 12, 12),
        filter_shape=(nkerns[1], nkerns[0], 5, 5),
        poolsize=(2, 2)
    )

    # the HiddenLayer being fully-connected, it operates on 2D matrices of
    # shape (batch_size, num_pixels) (i.e matrix of rasterized images).
    # This will generate a matrix of shape (batch_size, nkerns[1] * 4 * 4),
    # or (500, 50 * 4 * 4) = (500, 800) with the default values.
    layer2_input = layer1.output.flatten(2)

    # construct a fully-connected sigmoidal layer
    layer2 = HiddenLayer(
        rng,
        input=layer2_input,
        n_in=nkerns[1] * 4 * 4,
        n_out=500,
        activation=T.tanh
    )

    # classify the values of the fully-connected sigmoidal layer
    layer3 = LogisticRegression(input=layer2.output, n_in=500, n_out=10)

    # the cost we minimize during training is the NLL of the model
    cost = layer3.negative_log_likelihood(y)

    predict = theano.function(inputs=[], outputs=layer3.y_pred)

    print 'Loading the model ...'
    f = file('trained_models/models/convolutional_mlp.mnist.trained.pickle', 'rb')
    # model_data = {layer0: {W: ..., b: ...}, layer1: ..., layer2: ..., layer3: ...}
    model_data = cPickle.load(f)
    f.close()
    print 'Loaded the model.'
    layers = [layer0, layer1, layer2, layer3]
    for i in range(4):
        layers[i].W.set_value(model_data['layer%s' % i]['W'])
        layers[i].b.set_value(model_data['layer%s' % i]['b'])
    print 'Restored model parameters.'
    print 'Predicting'
    return predict()[0]


def predict(new_img_path, model=LOG_REG):
    print 'Predicting ...'
    new_img = normalize(new_img_path)
    new_img = new_img.convert('1')
    new_img.save(new_img_path[:new_img_path.index('.png')] + '.processed.png')
    img_data = numpy.asarray(new_img.getdata())
    if model == LOG_REG:
        return _logistic_regression(img_data)
    elif model == CONV_MLP:
        img_data = numpy.asarray(new_img.getdata(), dtype='float32')
        new_digit = img_data.reshape((1, img_data.shape[0]))
        return _convolutional_mlp(new_digit)


if __name__ == '__main__':
    img_path = '/home/aseke/research/theano/classification_demo/uploads/six.png'
    print predict(img_path)


