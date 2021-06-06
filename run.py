import os
import time
i=0
cwd=os.path.join(os.getcwd(),"main.py")
while True:
        try:
                os.system('{} {}'.format('python3',cwd))
                print('loop',i)
                i+=1
                time.sleep(800)
        except:
                pass
