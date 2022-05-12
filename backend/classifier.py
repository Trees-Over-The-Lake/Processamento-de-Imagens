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

from PIL import Image, ImageFilter, ImageEnhance


class ImageClassifier:
    # Modelo para previsões
    __model: svm.SVC()
    
    # Kernel do modelo
    __model_kernel: str

    ## Arrays com os conjuntos de treino e teste, bem como as respostas
    __images_train:  np.empty(0, dtype=np.float64)
    __images_test:   np.empty(0, dtype=np.float64)
    __predictions:   np.empty(0, dtype=np.float64)
    __answers_train: np.empty(0, dtype=np.int32)
    __answers_test:  np.empty(0, dtype=np.int32)
    
    # Diretorio onde estão as pastas de classes BIRADS
    __images_dir: str

    # Tipos de arquivos
    __supported_img_extensions: list

    # Porcentagem de dados para treino. É balanceado igualmente entre
    # as classses BIRADS
    __percentage_train: int

    # Numero de cores
    __n_colors: float
    
    # Raio da matriz de suavização gaussiana. 0 desabilita
    __gaussian_radius: int
    
    # Em quanto cada um desses elementos será realçado
    # no pré-processamento. 1 os mantém igual, valores de 0 a 1
    # os reduzem e valores maiores que 1 aumentam
    __sharpness_boost_strength:  float
    __contrast_boost_strength :  float
    __brightness_boost_strength: float
    __color_boost_strength:      float

    # Distancias na matriz de co-ocorrencia
    __distances_glcm: np.empty(0, dtype=np.int32)

    # Angulos para calcular matriz de co-ocorrencia
    __angles_glcm: np.empty(0, dtype=np.float64)


    def __init__(self):
        self.__model_kernel = "linear"
        self.__model = svm.SVC(kernel=self.__model_kernel, C=1.15)
        
        self.__images_train  = np.empty(0, dtype=np.float64)
        self.__images_test   = np.empty(0, dtype=np.float64)
        self.__predictions   = np.empty(0, dtype=np.float64)
        self.__answers_train = np.empty(0, dtype=np.int32)
        self.__answers_test  = np.empty(0, dtype=np.int32)
        
        self.__supported_img_extensions = ['.jpg', '.jpeg', '.png']

        # Valores default. Outros valores podem ser escolhidos pela interface e pelo metodo set :)
        self.__n_colors = 32
        self.__gaussian_radius = 0.15
        self.__sharpness_boost_strength  = 1
        self.__contrast_boost_strength   = 1
        self.__brightness_boost_strength = 1
        self.__color_boost_strength      = 1
        self.__percentage_train = 75

        self.__distances_glcm = np.array([
            1, 
            2, 
            4, 
            8, 
            16
        ])

        self.__angles_glcm = np.array([
            0, 
            np.pi/8, 
            np.pi/4, 
            3*np.pi/8, 
            np.pi/2, 
            5*np.pi/8, 
            3*np.pi/4, 
            7*np.pi/8
        ])


    # Gets e Sets :)
    def set_model_kernel(self, k: str):
        self.__model_kernel = k
    
    def get_model_kernel(self):
        return self.__model_kernel

    def set_n_colors(self, n_colors: int):
        self.__n_colors = n_colors
    
    def get_n_colors(self):
        return self.__n_colors

    def set_gaussian_radius(self, strength: int):
        self.__gaussian_radius = strength
    
    def get_gaussian_radius(self):
        return self.__gaussian_radius
    
    def set_sharpness_boost_strength(self, strength: float):
        self.__sharpness_boost_strength = strength
    
    def get_sharpness_boost_strength(self):
        return self.__sharpness_boost_strength

    def set_contrast_boost_strength(self, strength: float):
        self.__contrast_boost_strength = strength
    
    def get_contrast_boost_strength(self):
        return self.__contrast_boost_strength

    def set_brightness_boost_strength(self, strength: float):
        self.__brightness_boost_strength = strength
    
    def get_brightness_boost_strength(self):
        return self.__brightness_boost_strength

    def set_color_boost_strength(self, strength: float):
        self.__color_boost_strength = strength
    
    def get_color_boost_strength(self):
        return self.__color_boost_strength

    def set_percentage_train(self, percentage: int):
        self.__percentage_train = percentage
    
    def get_percentage_train(self):
        return self.__percentage_train

    def set_images_dir(self, dir: str):
        self.__images_dir = dir

    def get_images_dir(self):
        return self.__images_dir

    def get_supported_img_extensions(self):
        return self.__supported_img_extensions

    def get_images_train(self):
        return self.__images_train

    def get_answers_train(self):
        return self.__answers_train

    def get_images_test(self):
        return self.__images_test

    def get_answers_test(self):
        return self.__answers_test

    def get_predictions(self):
        return self.__predictions

    '''
    Essa função separa as imagens encontradas nas pastas de acordo com self.__percentage_train, com 
    balanceamento equilibrado entre as 4 classes.
    '''
    def split_train_test(self):
        
        '''
        Infelizmente não há como saber quantos elementos os arrays vão ocupar de antemão,
        e isso impossibilita usar arrays numpy para armazenar diretamente os dados resultados.
        Os conjuntos de teste e treino são armazenados aqui temporariamente e no fim da execução
        são convertidos para arrays numpy de volta.
        '''
        tmp_train_set = []
        tmp_test_set  = []

        density_classes = ["1", "2", "3", "4"]
        for density_class in density_classes:
            path_images = [f for f in os.listdir(f"{self.get_images_dir()}/{density_class}") if f.endswith(tuple(self.get_supported_img_extensions()))]
            
            tmp_train, tmp_test = train_test_split(path_images, train_size=self.get_percentage_train(), shuffle=True)

            # Para cada imagem no conjunto de treino, extrair os descritores de textura abaixo e concatená-los
            # ao conjunto de treino
            for i in tmp_train:
                image =  Image.open(f"{self.get_images_dir()}/{density_class}/{i}")

                # Pré-processamento com suavização gaussiana e filtros para alterar sharpness,
                # contraste, cor e brilho
                image = image.filter(ImageFilter.GaussianBlur(radius=self.get_gaussian_radius()))

                enhancer_sharpness = ImageEnhance.Sharpness(image)
                image = enhancer_sharpness.enhance(self.get_sharpness_boost_strength())

                enhancer_contrast = ImageEnhance.Contrast(image)
                image = enhancer_contrast.enhance(self.get_contrast_boost_strength())

                enhancer_color = ImageEnhance.Color(image)
                image= enhancer_color.enhance(self.get_color_boost_strength())

                enhancer_brightness = ImageEnhance.Brightness(image)
                image= enhancer_brightness.enhance(self.get_brightness_boost_strength())

                # Reamostragem dos tons de cinza
                image = image.quantize(self.get_n_colors())

                # Gerando matriz de co-ocorrência
                glcm          =  graycomatrix(image, self.__distances_glcm, self.__angles_glcm, levels=self.get_n_colors())
                
                # Extraindo descritores de textura
                energy        =  graycoprops(glcm, 'energy')
                homogeneity   =  graycoprops(glcm, 'homogeneity')
                asm           =  graycoprops(glcm, 'ASM')
                dissimilarity =  graycoprops(glcm, 'dissimilarity')
                correlation   =  graycoprops(glcm, 'correlation')
                contrast      =  graycoprops(glcm, 'contrast')
                entropy       =  shannon_entropy(glcm, base=2)
                
                # Ajuntando todos em um array só
                descriptors = np.concatenate((energy, homogeneity, entropy, asm, dissimilarity, correlation, contrast), axis=None)
                
                tmp_train_set.append(descriptors)
                self.__answers_train = np.append(self.__answers_train, [density_class], axis=0)

            
            # Mesma coisa que antes, só que concatenar ao conjunto de teste
            for i in tmp_test:
                image         =  np.asarray(Image.open(f"{self.get_images_dir()}/{density_class}/{i}").quantize(self.get_n_colors()))

                glcm          =  graycomatrix(image, self.__distances_glcm, self.__angles_glcm, levels=self.get_n_colors())
                energy        =  graycoprops(glcm, 'energy')
                homogeneity   =  graycoprops(glcm, 'homogeneity')
                asm           =  graycoprops(glcm, 'ASM')
                dissimilarity =  graycoprops(glcm, 'dissimilarity')
                correlation   =  graycoprops(glcm, 'correlation')
                contrast      =  graycoprops(glcm, 'contrast')
                entropy       =  shannon_entropy(glcm, base=2)
                
                descriptors = np.concatenate((energy, homogeneity, entropy, asm, dissimilarity, correlation, contrast), axis=None)

                tmp_test_set.append(descriptors)
                self.__answers_test = np.append(self.__answers_test, [density_class], axis=0)
                
        # Transformando de volta para um array numpy
        self.__images_train = np.asarray(tmp_train_set)
        self.__images_test  = np.asarray(tmp_test_set)


    def train_model(self):
        self.__model.fit(self.get_images_train(), self.get_answers_train())


    def predict_with_test_imgs(self):
        self.__predictions = self.__model.predict(self.get_images_test())