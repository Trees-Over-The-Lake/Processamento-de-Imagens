from classifier import ImageClassifier
import sklearn.metrics
a = ImageClassifier()
a.set_images_dir("../Imagens")
a.split_train_test()
a.train_model()
a.predict_with_test_imgs()
print(sklearn.metrics.accuracy_score(a.get_answers_test(), a.get_predictions()))


'''
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
'''