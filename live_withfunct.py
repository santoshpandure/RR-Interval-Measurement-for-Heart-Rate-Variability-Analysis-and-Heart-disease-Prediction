import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import serial
import time
import readline
import re, sys
import csv
from sklearn import preprocessing, cross_validation, neighbors, svm
from scipy.signal import butter, lfilter

def readdata():
    global files
    global data_list
    ser = serial.Serial('/dev/ttyACM0',9600)
    timeout_start = time.time()
    # timeout variable can be omitted, if you use specific value in the while condition
    timeout = 60*1# [seconds]
    data_list = []         
    while time.time() < timeout_start + timeout:
        data = ser.readline()
        #data = data.split('\r\n')[0]
        data = re.sub('[^0-9]','',data)
        #print (data)
        data_list.append(data)
        #time.sleep(0.1)
        #print data_list
    
       
    files = pd.DataFrame(data_list)
    time.sleep(1)
    missing_value = 0
    files.fillna(missing_value)
    files.to_csv("/home/pi/Desktop/new GUI1/data.csv", index = False)
    #time.sleep(0.50)   
    #print ("please waite......data is processed....")
    #time.sleep(0.50)

##    graph = open('graph.txt', 'w')
##    index = 0
##
##    for val in data_list:
##        if len(val) == 3:
##            graph.write("%d,%s \n"%(index, val))
##            index += 1
##
##    graph.close()



    

def datacleaning():
    try :
        global files
        u_cols = ['heart']
        files = pd.read_csv("/home/pi/Desktop/demo15.csv", names = u_cols)
        files[files>1000] = 0
        cal_mean = int (files["heart"].mean())
        files[files<=100] = cal_mean
        print cal_mean
        files = files.fillna(cal_mean)
        files.to_csv("/home/pi/Desktop/demo12.csv")
        print files

    except IOError:
        print "file not found"
        sys.exit()


def moving_average():
    global measures
    global mov_avg
    global peaklist
    global ybeat
    global frequency_sam
    measures = {}
    heart_rate_window =0.75 #One-sided window size, as proportion of the sampling frequency
    frequency_sam = 100 #The example dataset was recorded at 100Hz
    #w = int(hrw*fs)
    #print w
    mov_avg = pd.rolling_mean(files.heart, window=(heart_rate_window*frequency_sam )) #Calculate moving average
    #mov_avg = pd.Series.rolling(dataset.hart, window=75,center=False).mean()
    #Impute where moving average function returns NaN, which is the beginning of the signal where x hrw
    avg_hr = (np.mean(files.heart))
    mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
    mov_avg = [x*1.2 for x in mov_avg] #For now we raise the average by 20% to prevent the secondary heart contraction from interfering,will do this dynamically
    files['heart_rollingmean'] = mov_avg #Append the moving average to the dataframe
    print mov_avg
    try:
        #Mark regions of interest
        window = []
        peaklist = []
        listpos = 0 #We use a counter to move over the different data columns
        for datapoint in files.heart:
            rollingmean = files.heart_rollingmean[listpos] #Get local mean
            if (datapoint < rollingmean) and (len(window) < 1): #If no detectable R-complex activity -> do nothing
                listpos += 1
            elif (datapoint > rollingmean): #If signal comes above local mean, mark ROI
                window.append(datapoint)
                listpos += 1
            else: #If signal drops below local mean -> determine highest point
                maximum = max(window)
                beatposition = listpos - len(window) + (window.index(max(window))) #Notate the position of the point on the X-axis
                peaklist.append(beatposition) #Add detected peak to list
                window = [] #Clear marked ROI
                listpos += 1
        measures['peaklist'] = peaklist
        measures['ybeat'] = [files.heart[x] for x in peaklist]
        ybeat = [files.heart[x] for x in peaklist] #Get the y-value of all peaks for plotting purposes
    except IOError:
        print "Please dont move hand....data acquzation is not done."
        sys.exit()

def rr_interval():
    global measures
    global RR_list
    peaklist = measures['peaklist']
    RR_list = []
    cnt = 0
    while (cnt < (len(peaklist)-1)):
        RR_interval = (peaklist[cnt+1] - peaklist[cnt]) #Calculate distance between beats in  samples
        #print RR_interval
        ms_dist = ((RR_interval / frequency_sam) * 1000.0) #Convert sample distances to ms distances
        RR_list.append(ms_dist) #Append to list
        cnt += 1
        measures['RR_list'] = RR_list
    print ("rr_list", RR_list)
    
    bpm = 60000 / np.mean(RR_list) #60000 ms (1 minute) / average R-R interval of signal
    print "Average Heart Beat is: %.01f" %bpm #Round off to 1 decimal and print
    print bpm


    
def plot():
    plt.xlim(0,1000)
    plt.plot(files.heart, alpha=0.5, color='blue', label="raw signal") #Plot semi-transparent HR
    plt.plot(mov_avg, color ='green', label="moving average")
    plt.scatter(peaklist, ybeat, color='red') # Plot detected peaks
    plt.legend(loc=4, framealpha=0.6)
    plt.show() 
    
    
  
def features():
    global features
    RR_diff = []
    RR_sqdiff = []
    RR_list = measures['RR_list']
    cnt = 1 #Use counter to iterate over RR_list
    while (cnt < (len(RR_list)-1)): #Keep going as long as there are R-R intervals
        RR_diff.append(abs(RR_list[cnt] - RR_list[cnt+1])) #Calculate absolute difference between successive R-R interval
        RR_sqdiff.append(math.pow(RR_list[cnt] - RR_list[cnt+1], 2)) #Calculate squared difference
        cnt += 1
    print RR_diff, RR_sqdiff
    # calculate featurs from RR interval
    features = []
    ibi = np.mean(RR_list) #Take the mean of RR_list to get the mean Inter Beat Interval
    print "IBI:", ibi
    sdnn = np.std(RR_list) #Take standard deviation of all R-R intervals
    print "SDNN:", sdnn
    sdsd = np.std(RR_diff) #Take standard deviation of the differences between all subsequent R-R intervals
    print "SDSD:", sdsd
    rmssd = np.sqrt(np.mean(RR_sqdiff)) #Take root of the mean of the list of squared differences
    print "RMSSD:", rmssd
    RR_list = pd.DataFrame({'RR_interval':RR_list})
    print RR_list


    features.append(ibi)
    features.append(sdnn)
    features.append(sdsd)
    features.append(rmssd)
    print features
    features = pd.DataFrame({'features':features})
    print features
    features.to_csv('/home/pi/Desktop/new GUI/features.csv', index = False)

def classificationkkn():
    try:
        df = pd.read_csv('/home/pi/Desktop/classification/knn1.csv')
        X = np.array(df.drop(['class'], 1))
        y = np.array(df['class'])
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.2)
        clf = neighbors.KNeighborsClassifier()
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_test, y_test)
        print ('Accuracy of classification: ', accuracy*100)
        #features = [0,0, 0, 0]
        example_measures = np.array(features)
        example_measures = example_measures.reshape(1, -1)
        prediction = clf.predict(example_measures)
        print ('prediction :', prediction)

    except IOError:
        print('file is not found or features are not found')

def classificationsvm():
    try:
        df = pd.read_csv('/home/pi/Desktop/classification/knn1.csv')
        X = np.array(df.drop(['class'], 1))
        y = np.array(df['class'])
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.2)
        clf = svm.SVC(kernel = 'linear', C = 1.0)
        clf.fit(X_train, y_train)
        #clf.fit(X, y)
        accuracy = clf.score(X_test, y_test)
        print (accuracy)*100
        #features = features
        example_measures = np.array(features)
        example_measures = example_measures.reshape(1, -1)
        prediction = clf.predict(example_measures)
        print(prediction)
        w = clf.coef_[0]
        print(w)
##        a= -w[0] / [1]
##        xx = np.linspace(0,71)
##        yy = a * xx - clf.intercept_[0] / w[1]
##        h0 = plt.plot(xx, yy, 'k-', label = 'non weighted')
##        plt.scatter(X[:, 0], X[:, 1], c = y)
##        plt.legend()
##        plt.show()
    except IOError:
         print('file is not found or features are not found')


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs #Nyquist frequeny is half the sampling frequency
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

    
def butter_lowpass_filter(data, cutoff, fs, order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y
    
    


if __name__ == "__main__":
    readdata()

##    moving_average()
##    rr_interval()
##    plot()
##    features()
##    classificationkkn()
##    classificationsvm()
    butter_lowpass()
    butter_lowpass_filter()
    
    
   
    
    
    
