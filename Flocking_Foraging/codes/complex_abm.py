import random  # Import the random module for generating random numbers
import math  # Import the math module for mathematical operations

class Fish:
    def __init__(self, x, y, speed):
        self.x = x  # Initialize the x-coordinate of the fish
        self.y = y  # Initialize the y-coordinate of the fish
        self.speed = speed  # Initialize the speed of the fish

    def swim(self, other_fish):
        # Move towards a nearby fish
        if other_fish:  # Check if there are other fish present
            target_fish = random.choice(other_fish)  # Select a random target fish from the list
            dx = target_fish.x - self.x  # Calculate the difference in x coordinates between the target fish and the current fish
            dy = target_fish.y - self.y  # Calculate the difference in y coordinates between the target fish and the current fish
            distance = math.sqrt(dx**2 + dy**2)  # Calculate the distance between the two fish using the Euclidean distance formula
            if distance > 0:  # Check if the distance is greater than 0 to avoid division by zero
                self.x += (dx / distance) * self.speed  # Update the x-coordinate of the fish based on the distance and speed
                self.y += (dy / distance) * self.speed  # Update the y-coordinate of the fish based on the distance and speed

        # Move randomly
        angle = random.uniform(0, 2*math.pi)  # Generate a random angle between 0 and 2*pi
        self.x += math.cos(angle) * self.speed  # Update the x-coordinate of the fish based on the random angle and speed
        self.y += math.sin(angle) * self.speed  # Update the y-coordinate of the fish based on the random angle and speed

class Aquarium:
    def __init__(self, width, height, num_fish):
        self.width = width  # Initialize the width of the aquarium
        self.height = height  # Initialize the height of the aquarium
        self.fish = []  # Initialize an empty list to store the fish objects
        for _ in range(num_fish):
            x = random.uniform(0, width)  # Generate a random x-coordinate within the aquarium boundaries
            y = random.uniform(0, height)  # Generate a random y-coordinate within the aquarium boundaries
            speed = random.uniform(0.1, 1)  # Generate a random speed for the fish
            fish = Fish(x, y, speed)  # Create a new fish object with the generated coordinates and speed
            self.fish.append(fish)  # Add the fish object to the list of fish in the aquarium

    def simulate(self, num_steps):
        steps = 1
        for _ in range(num_steps):  # Iterate for the specified number of simulation steps
            for i, fish in enumerate(self.fish):  # Iterate over each fish in the aquarium
                other_fish = self.fish[:i] + self.fish[i+1:]  # Exclude the current fish from the list of other fish
                fish.swim(other_fish)  # Make the fish swim by calling the swim method and passing the other fish
                self.wrap_around(fish)  # Wrap the fish coordinates within the aquarium boundaries
            self.print_state(steps)  # Print the current state of the aquarium after each simulation step
            if steps <= num_steps:
                steps += 1

    def wrap_around(self, fish):
        # Wrap the fish coordinates within the aquarium
        if fish.x < 0:  # If the fish goes beyond the left boundary of the aquarium
            fish.x += self.width  # Wrap it around to the right boundary
        elif fish.x > self.width:  # If the fish goes beyond the right boundary of the aquarium
            fish.x -= self.width  # Wrap it around to the left boundary
        if fish.y < 0:  # If the fish goes beyond the top boundary of the aquarium
            fish.y += self.height  # Wrap it around to the bottom boundary
        elif fish.y > self.height:  # If the fish goes beyond the bottom boundary of the aquarium
            fish.y -= self.height  # Wrap it around to the top boundary

    def print_state(self, num_steps):
        for fish in self.fish:  # Iterate over each fish in the aquarium
            print(f"Fish {self.fish.index(fish) + 1} at ({fish.x}, {fish.y}) with speed {fish.speed}m/s after {num_steps} seconds")  # Print the current position and speed of the fish
        print("------")  # Print a line separator to separate each simulation step

# Create an aquarium with 10 fish
acuario = Aquarium(10, 10, 10)

# Simulate the movement of the fish for 20 time steps
acuario.simulate(20)
