
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
import pickle
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def ML_LogisticRegression_train(data, labelcolname, size=0.25, penalty='l2', showcoef=False, showmatch=False,
                                savefilename='lg.pickle', **kwargs):
    X = data[[x for x in data.columns if x != labelcolname]]
    y = data[labelcolname]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size)

    # 标准化处理
    std = StandardScaler()
    X_train = std.fit_transform(X_train)
    X_test = std.transform(X_test)

    # 模型训练
    # 创建一个逻辑回归估计器
    lg = LogisticRegression(penalty=penalty, C=1.0)
    # 训练模型，进行机器学习
    lg.fit(X_train, y_train)
    # 得到模型，打印模型回归系数，即权重值

    with open(savefilename, 'wb') as fw:
        pickle.dump(lg, fw)

    if showcoef is True:
        print("logist回归系数为:\n", lg.coef_)
    else:
        pass
    # return estimator
    # 模型评估
    y_predict = lg.predict(X_test)
    y_proba = lg.predict_proba(X_test)
    y_proba = y_proba.max(axis=1)
    # print(y_proba.max(axis = 1))

    if showmatch is True:
        print("预测值为:\n", y_predict)
        print("真实值与预测值比对:\n", y_predict == y_test)
    else:
        pass
    rate = lg.score(X_test, y_test)
    print("直接计算准确率为:\n", rate)

    # 打印精确率、召回率、F1 系数以及该类占样本数
    labelsclass = list(set(y.tolist()))
    print(labelsclass)
    print("精确率与召回率为:\n", classification_report(y_test, y_predict, labels=labelsclass))

    # ###模型评估
    # #ROC曲线与AUC值
    print("AUCpredict值:\n", roc_auc_score(y_test, y_predict))
    print("AUCproba值:\n", roc_auc_score(y_test, y_proba))


def ML_predict(modelfile, dataset):
    with open(modelfile, 'rb') as fr:
        new_lg = pickle.load(fr)
        print(new_lg.predict([dataset]))


def ML_SVM_train(data,labelcolname,size= 0.25,savefilename='svm.pickle'):
    X = data[[x for x in data.columns if x != labelcolname]]
    y = data[labelcolname]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size)

    # 标准化处理
    std = StandardScaler()
    X_train = std.fit_transform(X_train)
    X_test = std.transform(X_test)



    from sklearn import svm
    predictor = svm.SVC(gamma='auto', C=1.0, decision_function_shape='ovr', kernel='rbf')
    predictor.fit(X_train, y_train)
    with open(savefilename, 'wb') as fw:
        pickle.dump(predictor, fw)
    # # 预测结果
    result = predictor.predict(X_test)
    # # 进行评估
    from sklearn.metrics import f1_score
    print("F-score: {0:.2f}".format(f1_score(result, y_test, average='micro')))

