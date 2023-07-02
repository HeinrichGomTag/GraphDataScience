import random  # Import the random module for generating random numbers


class Fish:
    def __init__(self, x, y):  # Constructor for the Fish class
        self.x = x  # Set the initial x-coordinate of the fish
        self.y = y  # Set the initial y-coordinate of the fish

    def swim(self):  # Method to simulate the swimming of the fish
        self.x += random.uniform(
            -1, 1
        )  # Add a random value to the current x-coordinate
        self.y += random.uniform(
            -1, 1
        )  # Add a random value to the current y-coordinate


class Aquarium:
    def __init__(self, width, height, num_fish):  # Constructor for the Aquarium class
        self.width = width  # Set the width of the aquarium
        self.height = height  # Set the height of the aquarium
        self.fish = []  # Initialize an empty list to store the fish
        for _ in range(num_fish):
            x = random.uniform(
                0, width
            )  # Generate a random x-coordinate within the aquarium width
            y = random.uniform(
                0, height
            )  # Generate a random y-coordinate within the aquarium height
            fish = Fish(x, y)  # Create a new Fish object with the generated coordinates
            self.fish.append(fish)  # Add the fish to the list

    def simulate(self, num_steps):  # Method to simulate the movement of the fish
        steps = 1
        for _ in range(
            num_steps
        ):  # Iterate for the specified number of simulation steps
            for fish in self.fish:  # Iterate over each fish in the aquarium
                fish.swim()  # Call the swim method of the fish to simulate its movement
                # Additional logic or rules can be applied here
            self.print_state(steps)  # Print the current state of the aquarium
            if steps <= num_steps:
                steps += 1

    def print_state(
        self, num_steps
    ):  # Method to print the current state of the aquarium
        for fish in self.fish:  # Iterate over each fish in the aquarium
            print(
                f"Fish {self.fish.index(fish) + 1} at ({fish.x}, {fish.y}) after { num_steps} steps"
            )  # Print the current position of the fish
        print("------")  # Print a separator line between each simulation step


# Create an aquarium with 5 fish
acuario = Aquarium(10, 10, 5)

# Simulate the movement of the fish for 10 time steps
acuario.simulate(10)
