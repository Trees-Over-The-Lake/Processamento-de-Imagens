import os
import string
import numpy as np

import sklearn.metrics
from skimage.feature import graycomatrix, graycoprops
from skimage import io
from sklearn import svm
from skimage.measure import shannon_entropy
from sklearn.model_selection import train_test_split

from matplotlib import pyplot as plt

from PIL import Image

'''
Returns two sets containing the training and testing sets, respectively
@param train_size: an int from 1 to 99 indicating how much of the available
data will be used for training
'''
def split_train_test(train_size: int, image_dir: string, grey_colors: int):
    train = []
    test  = []
    train_answers = []
    test_answers  = []

    supported_extensions = ['.jpg', '.jpeg', '.png']

    density_classes = ["1", "2", "3", "4"]
    for density_class in density_classes:
        path_images = [file for file in os.listdir(f"{image_dir}/{density_class}") if file.endswith(tuple(supported_extensions))]
        tmp_train, tmp_test = train_test_split(path_images, train_size=train_size, shuffle=True)

        for i in tmp_train:

            image       =  np.asarray(Image.open(f"{image_dir}/{density_class}/{i}").quantize(grey_colors))
            
            glcm        =  graycomatrix(image, [1, 2, 4, 8, 16], [0, np.pi/8, np.pi/4, 3*np.pi/8, np.pi/2, 5*np.pi/8, 3*np.pi/4, 7*np.pi/8])
            energy      =  graycoprops(glcm, 'energy')
            homogeneity =  graycoprops(glcm, 'homogeneity')
            asm         =  graycoprops(glcm, 'ASM')
            entropy     =  shannon_entropy(glcm, base=2)

            tmp = np.concatenate((energy, homogeneity, entropy), axis=None)

            train.append(tmp)
            train_answers.append(f"{density_class}")
        
        for i in tmp_test:
            image       =  np.asarray(Image.open(f"{image_dir}/{density_class}/{i}").quantize(grey_colors))

            glcm        =  graycomatrix(image, [1, 2, 4, 8, 16], [0, np.pi/8, np.pi/4, 3*np.pi/8, np.pi/2, 5*np.pi/8, 3*np.pi/4, 7*np.pi/8])
            energy      =  graycoprops(glcm, 'energy')
            homogeneity =  graycoprops(glcm, 'homogeneity')
            asm         =  graycoprops(glcm, 'ASM')
            entropy     =  shannon_entropy(glcm, base=2)
            
            tmp = np.concatenate((energy, homogeneity, entropy), axis=None)

            test.append(tmp)
            test_answers.append(f"{density_class}")

    return train, test, train_answers, test_answers

def runPrediction(train_size: int, image_dir: string, grey_colors: int):
    train, test, train_answers, test_answers = split_train_test(train_size, image_dir, grey_colors)

    clf = svm.SVC(kernel="linear")
    clf.fit(train, train_answers)

    prediction = clf.predict(test)
    
    accuracy = sklearn.metrics.accuracy_score(test_answers, prediction)
    confusion_matrix = sklearn.metrics.confusion_matrix(test_answers, prediction)

    especificidade = 0

    print(f"Accuracy = {accuracy}")
    print(f"Matriz de confusão = {confusion_matrix}")

    plt.matshow(confusion_matrix, fignum="int")

    for (i, j), z in np.ndenumerate(confusion_matrix):
        plt.text(j, i, '{:0.1f}'.format(z), ha='center', va='center',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'))

    plt.savefig(f"./metricas.png")
    return accuracy, especificidade

def runPredictionOneImage(train_size: int, images_path: string, grey_colors: int):
    image       =  np.asarray(Image.open(f"{image_dir}/{density_class}/{i}").quantize(grey_colors))

    glcm        =  graycomatrix(image, [1, 2, 4, 8, 16], [0, np.pi/8, np.pi/4, 3*np.pi/8, np.pi/2, 5*np.pi/8, 3*np.pi/4, 7*np.pi/8])
    energy      =  graycoprops(glcm, 'energy')
    homogeneity =  graycoprops(glcm, 'homogeneity')
    asm         =  graycoprops(glcm, 'ASM')
    entropy     =  shannon_entropy(glcm, base=2)
    
    tmp = np.concatenate((energy, homogeneity, entropy), axis=None)