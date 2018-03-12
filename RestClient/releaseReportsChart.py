import pandas as pd
import matplotlib.pyplot as plt

def getReports(*file_paths):
    if len(file_paths)==0 or len(file_paths)>1:
        raise ValueError("Invalid file paths, expecting 2 got " + str(len(file_paths)))
    else:
        for f in file_paths:
            data=pd.read_csv(f)
        r_status=['Canceled','Succeeded','Failed','Active']
        color_code=['grey','green','red','c']
        r_count=[]
        for r in r_status:
            r_count.append(len(data[data.releaseStatus==r]))
        print(r_count)
        fig, ax =plt.subplots()
        ax.bar(r_status,r_count,color=color_code)
        plt.show()

        #plt.hist(r_count,r_status)


