# RR-Interval-Measurement-for-Heart-Rate-Variability-Analysis-and-Heart-disease-Prediction
Heart is the most important organ in the human body and the efforts were taken in order to understand the heart beats in precise manner. There were several mechanism were observed
and one of the most popular mechanism form representation of electrical activities tracing on paper is electrocardiogram (ECG). The Heart Rate Variability (HRV) is also well known
functionality devised for understanding functionality of heart its measure was derived manually, more prominently from the ECG. The electrical conduction through the heart follows
a set pathway under normal conditions. Disturbances in these pathways may leads in altering the pathway, the wave of depolarization must follow and change in timing of the electrical events were observed. Heart rate variability (HRV), the beat-to-beat variation in either heart rate or the duration of the R-R interval, has become a popular clinical and investigational tools. Although the exact contributions of the parasympathetic and the sympathetic divisions of the autonomic nervous system to this variability are controversial and remain the subject of active investigation and debate, a number of time and frequency domain techniques have been developed to provide insight into cardiac autonomic regulation in both health and disease. Heart rate variability (HRV) is the physiological phenomenon of variation in the time interval between heartbeats. It is measured by the variation in the beat-to-beat interval.


**Install essential Dependency **
1. import Tkinter as tk   # python
2. from Tkinter import *
3. import live_withfunct as lv
4. import ttk, time, datetime
5. import sqlite3
6. import tkMessageBox
7. import sys
8. import pandas as pd
9. import matplotlib.pyplot as plt
10. import numpy as np
11. import math
12. import serial
13. import time
14. import readline
15. import re, sys
16. import csv
17. from sklearn import preprocessing, cross_validation, neighbors, svm
18. import time
19. from scipy.signal import butter, lfilter
20. import requests
21. import tkFileDialog
22. from matplotlib import style
23. from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
24. from matplotlib.figure import Figure
25. import matplotlib.animation as animation
26. import subprocess
27. import os
28. import xlwt
29. import glob

# Experimental Work

The HRV was carried out by Time domain techniques, this feature was calculated for all the samples of the training set and testing set and store for recognition purposes. We applied classification of two different datasets i.e. Heart Beat sensor dataset and ECG Machine Dataset. The entire dataset of ECG machine and heartbeat sensor was divided into 70-30 ratio that is 70% for training and 30% for testing and pass for classification using K-Nearest Neighbor (KNN), Neural Network (NN) and Support Vector Machine (SVM) classifier. KNN is used as a classifier in this study. It is a Nonparametric and supervised learning classifier, KNN has a significant place among classifiers and is commonly prepared in various science and engineering applications. Total 1060 samples of analog and digital heartbeat sensor i.e. 530 of analog sensor and 530 of digital sensor and 530 ECG machine samples used in this experiment. Out of 530 samples of analog and digital sensors, 371 samples were used for training and 159 used for testing. So after applying KNN we achieved 98% accuracy from the analog sensor and 93% result from the digital sensor. Similarly, the ECG machine sample passes for recognition and it gives 95% accuracy.
