from flask import render_template, flash, url_for, redirect, request
from chartjs_dashboard import app, db, bcrypt
from flask_wtf import FlaskForm
from flask_login import login_user, current_user, logout_user, login_required
from wtforms import SelectField, IntegerField
from wtforms.validators import DataRequired
import pandas as pd

from chartjs_dashboard.models import User, Post
from chartjs_dashboard.formClasses import RegistrationForm, LoginForm, ActiveEHOForm, HighRiskSites, PersistentComplaints, LostTimeKPI

# user routes

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dash'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}. You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# charts

@app.route("/dash", methods=['GET', 'POST'])
@login_required
def dash():

    datasets = {}

    for csv in ['chartjs_dashboard/datasets/ActiveEHOConcernsYTDWWT.csv',
                'chartjs_dashboard/datasets/HighRiskSitesYTDWWT.csv',
                'chartjs_dashboard/datasets/PersistentComplaintsYTDWWT.csv',
                'chartjs_dashboard/datasets/SludgeStocksInCatchmentNL.csv',
                'chartjs_dashboard/datasets/SludgeStocksInCatchmentSL.csv',
                'chartjs_dashboard/datasets/SludgeStocksInCatchmentTV.csv',
                'chartjs_dashboard/datasets/SludgeStocksInCatchmentWWT.csv']:
        
        datasets[csv] = pd.read_csv(csv)

    activeEHOData = datasets['chartjs_dashboard/datasets/ActiveEHOConcernsYTDWWT.csv'] 
    activeEHOData = activeEHOData.fillna(0)
    x = list(activeEHOData.columns)
    y = list(activeEHOData.iloc[0].values)
    y = [int(i) for i in y]

    labels = x
    values = y

    highriskData = datasets['chartjs_dashboard/datasets/HighRiskSitesYTDWWT.csv']
    highriskData = highriskData.fillna(0)
    x1 = list(highriskData.columns)
    y1 = list(highriskData.iloc[0].values)

    labels1 = x1
    values1 = y1

    persistentComplaintsData = pd.read_csv('chartjs_dashboard/datasets/PersistentComplaintsYTDWWT.csv')
    persistentComplaintsData = persistentComplaintsData.fillna(0)
    x2 = list(persistentComplaintsData.columns)
    y2 = list(persistentComplaintsData.iloc[0].values)

    labels2 = x2
    values2 = y2

    sludgeStocksNLData = pd.read_csv('chartjs_dashboard/datasets/SludgeStocksInCatchmentNL.csv')
    sludgeStocksNLData = sludgeStocksNLData.fillna(0)
    x3 = list(sludgeStocksNLData.columns)
    y3 = list(sludgeStocksNLData.iloc[0].values)

    labels3 = x3
    values3 = y3

    sludgeStocksSLData = pd.read_csv('chartjs_dashboard/datasets/SludgeStocksInCatchmentSL.csv')
    sludgeStocksSLData = sludgeStocksSLData.fillna(0)
    x4 = list(sludgeStocksSLData.columns)
    y4 = list(sludgeStocksSLData.iloc[0].values)
    
    labels4 = x4
    values4 = y4

    sludgeStocksTVData = pd.read_csv('chartjs_dashboard/datasets/SludgeStocksInCatchmentTV.csv')
    sludgeStocksTVData = sludgeStocksTVData.fillna(0)
    x5 = list(sludgeStocksTVData.columns)
    y5 = list(sludgeStocksTVData.iloc[0].values)

    labels5= x5
    values5 = y5

    sludgeStocksWWTData = pd.read_csv('chartjs_dashboard/datasets/SludgeStocksInCatchmentWWT.csv')
    sludgeStocksWWTData = sludgeStocksWWTData.fillna(0)
    x6 = list(sludgeStocksWWTData.columns)
    y6 = list(sludgeStocksWWTData.iloc[0].values)

    labels6 = x6
    values6 = y6

    kpiDashData = pd.read_csv('chartjs_dashboard/datasets/kpidash.csv')
    kpiDashData = kpiDashData.fillna('')    
    tableColumns = list(kpiDashData.columns)
    lostTimeRow = list(kpiDashData.iloc[0, :])
    assetAvailRow = list(kpiDashData.iloc[1, :])
    energyConsumedRow = list(kpiDashData.iloc[2, :])
    energyGeneratedRow = list(kpiDashData.iloc[3, :]) 

    return render_template('dashtest.html', values=values, 
            labels=labels, labels1=labels1, values1=values1, 
            labels2=labels2, values2=values2, labels3=labels3, 
            values3=values3, labels4=labels4, values4=values4,
            labels5=labels5, values5=values5, values6=values6,
            tableColumns=tableColumns, lostTimeRow=lostTimeRow, 
            assetAvailRow=assetAvailRow, energyConsumedRow=energyConsumedRow, 
            energyGeneratedRow=energyGeneratedRow) 
  

@app.route("/activeehoconcerns", methods=['GET', 'POST'])
@login_required
def activeEHOConcernsYTDWWT():
    activeEHOData = pd.read_csv('chartjs_dashboard/datasets/ActiveEHOConcernsYTDWWT.csv')
    activeEHOData = activeEHOData.fillna(0)
    x = list(activeEHOData.columns)
    y = list(activeEHOData.iloc[0].values)
    data_tuples = dict(zip(x, y))
    y = [int(i) for i in y]

    legend = 'Active EHO Concerns Dataset'
    labels = x
    values = y

    form = ActiveEHOForm()
    form.date.choices = [i for i in data_tuples]

    if request.method == 'POST':
        dateVar = request.form['date']
        valVar = request.form['val']
        try:
            valVar = int(valVar)
        except ValueError:
            return render_template('activeehoconcerns.html', values=values, 
                    labels=labels, legend=legend, form=form)
        activeEHOData.loc[0, dateVar] = valVar
        activeEHOData.to_csv('chartjs_dashboard/datasets/ActiveEHOConcernsYTDWWT.csv', index=False)
        activeEHOData = pd.read_csv('chartjs_dashboard/datasets/ActiveEHOConcernsYTDWWT.csv')
        activeEHOData = activeEHOData.fillna(0)
        x = list(activeEHOData.columns)
        y = list(activeEHOData.iloc[0].values)
        data_tuples = dict(zip(x, y))
        y = [int(i) for i in y]
        legend = 'Active EHO Concerns Dataset'
        labels = x
        values = y
        return render_template('activeehoconcerns.html', values=values, 
                labels=labels, legend=legend, form=form)

    legend = 'Active EHO Concerns Dataset'
    labels = x
    values = y

    return render_template('activeehoconcerns.html', values=values, 
            labels=labels, legend=legend, form=form)

@app.route("/highrisksites", methods=['GET', 'POST'])
@login_required
def highRiskSites():
    highriskData = pd.read_csv('chartjs_dashboard/datasets/HighRiskSitesYTDWWT.csv')
    highriskData = highriskData.fillna(0)
    x = list(highriskData.columns)
    y = list(highriskData.iloc[0].values)
    data_tuples = dict(zip(x, y))
    y = [int(i) for i in y]

    legend = 'High Risk Sites Dataset'
    labels = x
    values = y

    form = HighRiskSites()
    form.date.choices = [i for i in data_tuples]

    if request.method == 'POST':
        dateVar = request.form['date']
        valVar = request.form['val']
        try:
            valVar = int(valVar)
        except ValueError:
            return render_template('highrisksites.html', values=values, 
                    labels=labels, legend=legend, form=form)
        highriskData.loc[0, dateVar] = valVar
        highriskData.to_csv('chartjs_dashboard/datasets/HighRiskSitesYTDWWT.csv', index=False)
        highriskData = pd.read_csv('chartjs_dashboard/datasets/HighRiskSitesYTDWWT.csv')
        highriskData = highriskData.fillna(0)
        x = list(highriskData.columns)
        y = list(highriskData.iloc[0].values)
        data_tuples = dict(zip(x, y))
        y = [int(i) for i in y]
        labels = x
        values = y

        return render_template('highrisksites.html', values=values, 
                labels=labels, legend=legend, form=form)

    legend = 'High Risk Sites Dataset'
    labels = x
    values = y

    return render_template('highrisksites.html', values=values, 
            labels=labels, legend=legend, form=form)


@app.route("/persistentcomplaints", methods=['GET', 'POST'])
@login_required
def persistentComplaints():
    persistentComplaintsData = pd.read_csv('chartjs_dashboard/datasets/PersistentComplaintsYTDWWT.csv')
    persistentComplaintsData = persistentComplaintsData.fillna(0)
    x = list(persistentComplaintsData.columns)
    y = list(persistentComplaintsData.iloc[0].values)
    data_tuples = dict(zip(x, y))
    y = [int(i) for i in y]

    legend = 'Persistent Complaints Dataset'
    labels = x
    values = y

    form = PersistentComplaints()
    form.date.choices = [i for i in data_tuples]

    if request.method == 'POST':
        dateVar = request.form['date']
        valVar = request.form['val']
        try:
            valVar = int(valVar)
        except ValueError:
            return render_template('persistentcomplaints.html', values=values,
                    labels=labels, legend=legend, form=form)
        persistentComplaintsData.loc[0, dateVar] = valVar
        persistentComplaintsData.to_csv(
            'chartjs_dashboard/datasets/PersistentComplaintsYTDWWT.csv', index=False)
        persistentComplaintsData = pd.read_csv(
            'chartjs_dashboard/datasets/PersistentComplaintsYTDWWT.csv')
        persistentComplaintsData = persistentComplaintsData.fillna(0)
        x = list(persistentComplaintsData.columns)
        y = list(persistentComplaintsData.iloc[0].values)
        data_tuples = dict(zip(x, y))
        y = [int(i) for i in y]
        labels = x
        values = y

        return render_template('persistentcomplaints.html', values=values, 
                labels=labels, legend=legend, form=form)

    legend = 'Persistent Complaints Dataset'
    labels = x
    values = y

    return render_template('persistentcomplaints.html', values=values, 
            labels=labels, legend=legend, form=form)


@app.route("/kpitable", methods=['GET', 'POST'])
@login_required
def kpitable():
    kpiDashData = pd.read_csv('chartjs_dashboard/datasets/kpidash.csv')
    kpiDashData = kpiDashData.fillna('')    
    tableColumns = list(kpiDashData.columns)
    lostTimeRow = list(kpiDashData.iloc[0, :])
    assetAvailRow = list(kpiDashData.iloc[1, :])
    energyConsumedRow = list(kpiDashData.iloc[2, :])
    energyGeneratedRow = list(kpiDashData.iloc[3, :]) 


    vals = list(kpiDashData.iloc[0].values)
 

    form = LostTimeKPI()
    if request.method == 'POST':
        modVar = request.form['modifier']
        valVar = request.form['val']
    return render_template("kpitable.html", form=form,
            tableColumns=tableColumns, lostTimeRow=lostTimeRow,
            assetAvailRow=assetAvailRow, energyConsumedRow=energyConsumedRow,
            energyGeneratedRow=energyGeneratedRow)
