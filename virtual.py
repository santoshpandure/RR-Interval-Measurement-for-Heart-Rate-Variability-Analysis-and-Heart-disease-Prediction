import subprocess


##def Focus():
##    p = subprocess.Popen(['florence show'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
##    if not "" == p.stderr.readline():
##        subprocess.Popen(['florence'], shell=True)
##



def Focus():
    p = subprocess.Popen(['matchbox-keyboard'])
    

if __name__ == "__main__":
    Focus()
    





        
