class Flight():
	counter = 1

	##specail methods in python called "init"
	def __init__(self,origin,destination,duration):

		#keep track of id number
		self.id=Flight.counter

		Flight.counter += 1
 
		#Keep track of list of passenger 
		self.passengers = []



		self.origin=origin
		self.destination=destination
		self.duration=duration

	def print_info(self):
		print(f"Flight Origin: {self.origin}")
		print(f"Flight destination: {self.destination}")
		print(f"Flight duration: {self.duration}")


		print()

		print("Passenger: ")
		for passenger in self.passengers:
			print(f"{passenger.name}")

	def delay(self,amount):
		self.duration += amount 


	def add_passenger(self, p):
		self.passengers.append(p)
		p.flight_id = self.id
 
class Passenger():

	def __init__(self,name):
		self.name=name

	



def main():

	f= Flight(origin="Kual Lumpur",destination="Mindat",duration=750)


	alice = Passenger(name="Alice")
	bob = Passenger(name="Bob")

	#add passenger
	f.add_passenger(alice)
	f.add_passenger(bob)



	f.print_info()


if __name__ == '__main__':
	main()