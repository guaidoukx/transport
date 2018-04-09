import sklearnimport pandas as pdimport numpy as npfrom sklearn.svm import SVRfrom sklearn.metrics import mean_squared_error, r2_scorefrom sklearn.cross_validation import KFoldoverall = 2171def read_data(split):    data = pd.DataFrame(pd.read_csv('IO/one.csv'))    Y = data['A']    X = data.drop(['A'], axis=1)        index = np.arange(0, len(Y))    np.random.shuffle(index)    Y = Y.values[index]    X = X.values[index]    L=[]    kf = KFold(overall, n_folds=split, shuffle=True)    for train_index, test_index in kf:        # print("TRAIN:", train_index, "TEST:", test_index)        train_ = [X[train_index], Y[train_index]]        test_ = [X[test_index], Y[test_index]]        L.append([train_,test_])    #     print(train_[0][1], test_[0][1])    #     print(L[0][0][0][1],L[0][1][0][1])    # print(len(L[0][0][0]))    return L, kf    # return train_, test_    def MAD(target, predictions):    absolute_deviation = np.abs(target - predictions)    return np.mean(absolute_deviation)def main(tran_test_split_):    print('start!')    D, kf = read_data(tran_test_split_)    print('read finish!')    L = []    for t,pred in enumerate(kf):        # print(t)        model_svr = SVR(kernel='poly', degree=4, gamma=1.8,)        model_svr.fit(D[t][0][0], D[t][0][1])        print('---------%d iteration SVR Training Finish & result----------' %(t+1))        svr_train_pred = model_svr.predict(D[t][0][0])        svr_test_pred = model_svr.predict(D[t][1][0])        for i, pred in enumerate([            [svr_train_pred, svr_test_pred]        ]):            print("-Train-")            trainRMSE = np.sqrt(mean_squared_error(D[t][0][1], pred[0]))            trainR2 = r2_score(D[t][0][1], pred[0])            trainMAD = MAD(D[t][0][1],pred[0])            print("Root Mean Squared Error: %.3f"  % trainRMSE)            print('R2 score: %.3f'  % trainR2)            print("Mean Absolute Deviation: %.3f" % trainMAD)                        print("-Test-")            testRMSE = np.sqrt(mean_squared_error(D[t][1][1], pred[1]))            testR2 = r2_score(D[t][1][1], pred[1])            testMAD = MAD(D[t][1][1], pred[1])            print("Root Mean Squared Error: %.3f" %testRMSE )            print('R2 score: %.3f'  % testR2)            print("Mean Absolute Deviation: %.3f" % testMAD)            print('\r')  # ----------------------------------------------            L.append([trainRMSE,trainR2,trainMAD,testRMSE,testR2,testMAD])    print("-----====final result===-----")    FT = []    for i in list(range(len(L[0]))):        sum_ = 0        for j, red in enumerate(kf):            sum_ = sum_ + L[j][i]        FT.append(sum_/tran_test_split_)        print('--final train--')    print("final train Root Mean Squared Error: %.3f"  % FT[0])    print("final train R2 score: %.3f"  % FT[1])    print("final train Mean Absolute Deviation: %.3f"  % FT[2])    print('--final test--')    print("final test Root Mean Squared Error: %.3f"  % FT[3])    print("final test R2 score: %.3f"  % FT[4])    print("final test Mean Absolute Deviation: %.3f"  % FT[5])    if __name__ == '__main__':    main(10)    # read_data(5)