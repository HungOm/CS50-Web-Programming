class Flight():

	##specail methods in python called "init"
	def __init__(self,origin,destination,duration):
		self.origin=origin
		self.destination=destination
		self.duration=duration

	def print_info(self):
		print(f"Flight Origin: {self.origin}")
		print(f"Flight destination: {self.destination}")
		print(f"Flight duration: {self.duration}")

	def delay(self,amount):
		self.duration += amount 



def main():

	m= Flight(origin="Paris",destination="London",duration=540)
	m.delay(10)
	m.print_info()

	print('=================================')

	f= Flight(origin="Kual Lumpur",destination="Mindat",duration=750)
	f.delay(150)
	f.print_info()


if __name__ == '__main__':
	main()