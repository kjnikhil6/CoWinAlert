import pickle
mydata={'678000':'No Vaccination center is available for booking.'}
with open('data.pkl', 'wb') as f:
	pickle.dump(mydata, f)
count=0
with open('counter.pkl', 'wb') as f:
	pickle.dump(count, f)
