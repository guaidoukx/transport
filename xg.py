#----coding:utf-8-----import numpy as npimport xgboost as xgbimport pandas as pdfrom sklearn.cross_validation import train_test_split,KFoldfrom sklearn.metrics import mean_squared_error, r2_scorefrom transport31 import MAD, read_datadata = pd.DataFrame(pd.read_csv('IO/one_fill.csv'))overall = 2171def to_fold(n):    L = []    ta = np.array(data)    kf = KFold(overall, n_folds=n,shuffle=True)    for train_index, test_index in kf:        train_ = pd.DataFrame(ta[train_index])        test_ = pd.DataFrame(ta[test_index])        # print(train_[0])        L.append([train_,test_])    return L,kfD, kf = to_fold(5)# D, kf = read_data(5)parameters = {    'booster' : 'gbtree',    'objective' : 'reg:linear',    'eval_metric': 'rmse',    'gamma': 0.1,    'max_depth': 8,    'subsample':0.9,    'colsample_bytree': 0.9,    'eta': 0.06}num_rounds = 150y_true = []y_pred = []for t, m in enumerate(kf):    train_xy, val_ = train_test_split(D[t][0], test_size=0.2, random_state=20)    # train_y, val_y = train_test_split(D[t][1], test_size=0.2, random_state=20)    train_y = train_xy[0]    train_x = train_xy.drop([0], axis=1)    print('train_x', train_x.shape)    val_y = val_[0]    val_x = val_.drop([0], axis=1)    test_y = D[t][1][0]    test_x = xgb.DMatrix(D[t][1].drop([0], axis=1))# for t, m in enumerate(kf):#     train_xv = D[t][0]#     train_yv = D[t][1]#     test_x = xgb.DMatrix(D[t][2])#     test_y = D[t][3]#     train_x, val_x = train_test_split(train_xv,test_size=0.2,random_state=20)#     train_y, val_y = train_test_split(train_yv,test_size=0.2,random_state=20)    xgb_train = xgb.DMatrix(train_x, train_y)    xgb_val = xgb.DMatrix(val_x, val_y)        watchlist = [(xgb_train,'train'),(xgb_val, 'val')]    model = xgb.train(parameters, xgb_train, num_rounds, watchlist, early_stopping_rounds=100)    pred = model.predict(test_x)    print('\n-----%d iteration xgboost Training Finish & result-----' % (t + 1))    print("Root Mean Squared Error: %.10f" % np.sqrt(mean_squared_error(test_y, pred)))    print('R2 score: %.10f' % r2_score(test_y, pred))    print("Mean Absolute Deviation: %.3f" % MAD(test_y,pred))    y_true.append(pd.DataFrame(test_y))    y_pred.append(pd.DataFrame(pred))final_true_y = pd.concat(y_true)final_pred_y = pd.concat(y_pred)print("\n-----====final result===-----")print("final test Root Mean Squared Error: %.10f"  % np.sqrt(mean_squared_error(final_true_y, final_pred_y)))print('final test R2 score: %.10f' % r2_score(final_true_y, final_pred_y))print("final test Mean Absolute Deviation: %.3f"  % MAD(final_true_y,final_pred_y))