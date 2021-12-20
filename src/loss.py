import keras.losses
import tensorflow as tf
import tensorflow_addons as tfa
from keras import backend as K


def pre_process_vectors(y_true, y_pred, logits=True):
    """
        Loss helper function for preprocessing vectors
        :param y_true True mask
        :param y_pred Predicted mask
        :param logits Flag for whether prediction is probability distribution or actual classes
    """
    y_true = tf.cast(y_true, tf.float32)
    if logits:
        y_pred = tf.argmax(y_pred, axis=-1)
    y_pred = tf.cast(y_pred, tf.float32)
    y_true = K.flatten(y_true)
    y_pred = K.flatten(y_pred)
    return y_true, y_pred


def dice_loss(y_true, y_pred, logits=True):
    """
        Dice loss
        :param y_true True mask
        :param y_pred Predicted mask
        :param logits Flag for whether prediction is probability distribution or actual classes
    """
    y_true, y_pred = pre_process_vectors(y_true, y_pred, logits)
    numerator = 2 * K.sum(y_true * y_pred)
    denominator = K.sum(y_true + y_pred)
    return 1 - numerator / denominator


def tversky_loss(y_true, y_pred, logits=True):
    """
        Tversky loss
        :param y_true True mask
        :param y_pred Predicted mask
        :param logits Flag for whether prediction is probability distribution or actual classes
    """
    y_true, y_pred = pre_process_vectors(y_true, y_pred, logits)
    # computed as the average ratio between the area of the fascicles and the area of the background
    beta = 0.154
    numerator = K.sum(y_true * y_pred)
    denominator = K.sum(y_true * y_pred + beta * (1 - y_true) * y_pred + (1 - beta) * y_true * (1 - y_pred))
    return 1 - numerator / denominator


def focal_tversky_loss(y_true, y_pred, logits=True):
    """
        Focal tversky loss
        :param y_true True mask
        :param y_pred Predicted mask
        :param logits Flag for whether prediction is probability distribution or actual classes
    """
    gamma = 4 / 3
    return tversky_loss(y_true, y_pred, logits) ** gamma


def diff_tversky_loss(y_true, y_pred):
    """
        Dice tversky loss
        :param y_true True mask
        :param y_pred Predicted mask
    """
    y_true = tf.cast(y_true, tf.float32)
    # y_pred = tf.cast(y_pred, tf.float32)
    # y_true = K.flatten(y_true)
    # y_pred = K.flatten(y_pred)
    beta = 0.154
    numerator = K.sum(y_true * y_pred)
    denominator = K.sum(y_true * y_pred + beta * (1 - y_true) * y_pred + (1 - beta) * y_true * (1 - y_pred))
    return 1 - numerator / denominator


def focal_loss(y_true, y_pred):
    """
        Focal loss
        :param y_true True mask
        :param y_pred Predicted mask
    """
    y_true = tf.cast(y_true, tf.float32)
    gamma = 1
    return -K.mean(K.pow(1 - y_pred, gamma) * K.log(y_pred + K.epsilon()) * y_true + K.pow(y_pred, gamma) * K.log(
        1 - y_pred + K.epsilon()) * (1 - y_true))


def custom_loss(y_true, y_pred):
    """
        Custom loss
        :param y_true True mask
        :param y_pred Predicted mask
    """
    bce = keras.losses.SparseCategoricalCrossentropy()
    fl = tfa.losses.SigmoidFocalCrossEntropy()
    return bce(y_true, y_pred) + fl(y_true, y_pred)


def nerve_segmentation_loss(y_true, y_pred, logits=True):
    """
        Nerve segmentation loss
        :param y_true True mask
        :param y_pred Predicted mask
        :param logits Flag for whether prediction is probability distribution or actual classes
    """
    y_true = tf.cast(y_true, tf.float32)
    sparse_cce = keras.losses.SparseCategoricalCrossentropy()
    o = sparse_cce(y_true, y_pred)
    return tf.reduce_mean(o)


def iou_score(y_true, y_pred, logits=True):
    """
        IOU score
        :param y_true True mask
        :param y_pred Predicted mask
        :param logits Flag for whether prediction is probability distribution or actual classes
    """
    y_true, y_pred = pre_process_vectors(y_true, y_pred, logits)
    intersection = K.sum(y_true * y_pred)
    union = K.sum(y_true) + K.sum(y_pred) - intersection
    return intersection / union
