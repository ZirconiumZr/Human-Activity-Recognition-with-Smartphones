from django.http import HttpResponse
from django.template import loader
from .models import Models
import pandas as pd
from django.shortcuts import redirect, render, get_object_or_404
from django.core.files.storage import FileSystemStorage
import joblib
from .forms import CsvUploadForm
import os


def login(request):
    context={}
    return render(request, template_name='login.html', context=context)

def upload(request):
    if request.method == 'POST':
        csvUploadForm = CsvUploadForm(request.POST, request.FILES)
        uploadFile = request.FILES['document']
        fs = FileSystemStorage()
        upload_filename = fs.save(uploadFile.name, uploadFile)
        upload_file_path = os.path.join('H:/Interview/SP/spproject/home/upload',upload_filename)
        testdf = pd.read_csv(upload_file_path)
        if 'subject' and 'Activity' in testdf.columns:
            X_test = testdf.drop(['subject', 'Activity'], axis=1)
        else:
            X_test = testdf
        xgselect=request.POST.get('xgselect')
        svcselect=request.POST.get('svcselect')
        rfselect=request.POST.get('rfselect')
        result = pd.DataFrame(columns=['XGBoost', 'SVC', 'RandomForest'])
        result.index.name = 'Index'
        # if 'XGBoost' in mylist:
        if 'XGBoost' == xgselect:
            result['XGBoost'] = xgboostPred(X_test)
        if 'SVC' == svcselect:
            result['SVC'] = svcPred(X_test)
        if 'RandomForest' == rfselect:
            result['RandomForest'] = randomForestPred(X_test)
        voteDf = result.filter(['XGBoost','SVC', 'RandomForest'], axis=1)
        voteDf['FinalResult'] = result.mode(axis=1)[0]
        result['FinalResult'] = voteDf['FinalResult']
        result.to_csv('./result/%s'%upload_filename,index=True)

    else:
        csvUploadForm = CsvUploadForm()
    context={'csvUploadForm':csvUploadForm}
    return render(request, template_name='upload.html', context=context)

def xgboostPred(X_test):
    loaded_model = joblib.load('./models/XGB_model.sav')
    y_pred= loaded_model.predict(X_test)
    return y_pred


def svcPred(X_test):
    loaded_model = joblib.load('./models/SVC_model.sav')
    y_pred= loaded_model.predict(X_test)
    return y_pred

def randomForestPred(X_test):
    loaded_model = joblib.load('./models/Ran_model.sav')
    y_pred= loaded_model.predict(X_test)
    return y_pred

def history(request):
    historyPath = 'H:/Interview/SP/spproject/result'
    if request.method == 'POST':
        ### Delete function
        if request.POST.get('modal_singleDelete'):
            audio_to_delete = request.POST.get('modal_singleDelete')
            if audio_to_delete != None:
                os.remove(os.path.join(historyPath,audio_to_delete))
    historyresult = os.listdir(historyPath)   
    return render(request, 'history.html', {'historyresult': historyresult})

def model(request):
  mymodels = Models.objects.all().values()
  template = loader.get_template('model.html')
  context = {
    'mymodels': mymodels,
  }
  return HttpResponse(template.render(context, request))

def detail(request, audio):
    path = './result'
    resultDf = pd.read_csv(os.path.join(path,audio)).dropna(axis=1, how='all')
    context = {
    'resultDf': resultDf,
    }
    return render(request, 'detail.html',context)
