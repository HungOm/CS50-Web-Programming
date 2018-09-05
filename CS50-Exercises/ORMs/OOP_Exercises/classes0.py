class Flight():

	##specail methods in python called "init"
	def __init__(self,origin,destination,duration):
		self.origin=origin
		self.destination=destination
		self.duration=duration



def main():

	f= Flight(origin="Paris",destination="London",duration=540)

	#change the value of variable
	f.duration += 10
	
	print(f.origin)
	print(f.destination)
	print(f.duration)

	# Paris
	# London
	# 550

if __name__ == '__main__':
	main()