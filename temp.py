import pickle
myData= {'1':'2'}
with open('data.pkl','wb') as f:
	pickle.dump(myData,f)
