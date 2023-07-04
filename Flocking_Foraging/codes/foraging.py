import random  # Import the random module for generating random numbers
import math  # Import the math module for mathematical operations
import matplotlib.pyplot as plt  # Import the matplotlib.pyplot module for plotting


class Agent:
    def __init__(self, x, y, speed, orientation):
        self.x = x  # Set the initial x-coordinate of the agent
        self.y = y  # Set the initial y-coordinate of the agent
        self.speed = speed  # Set the speed of the agent
        self.speed = speed
        self.orientation = orientation  # Set the orientation (direction) of the agent

    def forage(self, food_sources):
        detection_radius = 5  # Define the detection radius for food sources

        closest_food = (
            None  # Initialize the closest food source to None (no food source detected)
        )
        closest_distance = math.inf  # Initialize the closest distance to infinity

        # Find the closest food source
        for food in food_sources:
            dx = food[0] - self.x  # Calculate the difference in x-coordinates
            dy = food[1] - self.y  # Calculate the difference in y-coordinates
            distance = math.sqrt(
                dx ** 2 + dy ** 2
            )  # Calculate the distance between the agent and the food source

            if (
                    distance < detection_radius and distance < closest_distance
            ):  # If the food source is within the detection radius and closer than the previous closest food source
                closest_food = food  # Update the closest food source
                closest_distance = distance  # Update the closest distance

        if closest_food is not None:
            # Move towards the closest food source
            dx = closest_food[0] - self.x  # Calculate the difference in x-coordinates
            dy = closest_food[1] - self.y  # Calculate the difference in y-coordinates
            angle = math.atan2(
                dy, dx
            )  # Calculate the angle between the agent and the food source
            self.x += self.speed * math.cos(angle)  # Move the agent in the x-direction
            self.y += self.speed * math.sin(angle)  # Move the agent in the y-direction
        else:
            # Explore randomly if no nearby food source is detected
            angle = random.uniform(0, 2 * math.pi)  # Generate a random angle
            self.x += self.speed * math.cos(angle)  # Move the agent in the x-direction
            self.y += self.speed * math.sin(angle)  # Move the agent in the y-direction

    def update_orientation(self):
        self.orientation = math.atan2(
            math.sin(self.orientation), math.cos(self.orientation)
        )
        # Update the orientation to ensure it stays within the range of [0, 2 * pi)


class ForagingSimulation:
    def __init__(self, width, height, num_agents, num_food_sources):
        self.width = width  # Set the width of the simulation environment
        self.height = height  # Set the height of the simulation environment
        self.agents = []  # Initialize an empty list to store the agents
        self.initial_positions = []  # List to store initial positions
        self.final_positions = []  # List to store final positions
        self.food_sources = []

        # Create agents with random positions and speeds
        for _ in range(num_agents):
            x = random.uniform(0, width)  # Generate a random x-coordinate
            y = random.uniform(0, height)  # Generate a random y-coordinate
            speed = random.uniform(0.1, 1)  # Generate a random speed
            orientation = random.uniform(
                0, 2 * math.pi
            )  # Generate a random orientation
            agent = Agent(
                x, y, speed, orientation
            )  # Create an agent with the random position and speed
            self.agents.append(agent)  # Add the agent to the list of agents
            self.initial_positions.append((x, y))  # Store initial position

        # Create random food sources
        for _ in range(num_food_sources):
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            self.food_sources.append(
                (x, y)
            )  # Add the food source to the list of food sources

    def simulate(self, num_steps):
        steps = 1
        for _ in range(num_steps):
            for agent in self.agents:
                agent.forage(self.food_sources)  # Forage for food
                agent.update_orientation()  # Update the agent's orientation
                self.wrap_around(
                    agent
                )  # Wrap the agent's coordinates within the simulation environment
            self.print_state(num_steps)  # Print the current state of the simulation
            if steps <= num_steps:
                steps += 1
        for agent in self.agents:
            self.final_positions.append((agent.x, agent.y))  # Store final position

    def wrap_around(self, agent):
        if agent.x < 0:
            agent.x += (
                self.width
            )  # Wrap the x-coordinate if it goes beyond the left boundary
        elif agent.x > self.width:
            agent.x -= (
                self.width
            )  # Wrap the x-coordinate if it goes beyond the right boundary
        if agent.y < 0:
            agent.y += (
                self.height
            )  # Wrap the y-coordinate if it goes beyond the bottom boundary
        elif agent.y > self.height:
            agent.y -= (
                self.height
            )  # Wrap the y-coordinate if it goes beyond the top boundary

    def print_state(self, num_steps):
        for fish in self.agents:  # Iterate over each fish in the aquarium
            print(
                f"Fish {self.agents.index(fish) + 1} at ({fish.x}, {fish.y}) with speed {fish.speed}m/s after {num_steps} seconds"
            )  # Print the current position and speed of the fish
        print("------")  # Print a line separator to separate each simulation step

    def plot_positions(self):
        initial_x = [pos[0] for pos in self.initial_positions]
        initial_y = [pos[1] for pos in self.initial_positions]
        final_x = [pos[0] for pos in self.final_positions]
        final_y = [pos[1] for pos in self.final_positions]
        food_x = [pos[0] for pos in self.food_sources]
        food_y = [pos[1] for pos in self.food_sources]

        plt.scatter(initial_x, initial_y, color="blue", label="Initial Position")
        plt.scatter(final_x, final_y, color="red", label="Final Position")
        plt.scatter(food_x, food_y, color="green", label="Food Sources")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Foraging: Initial VS Final Positions of Fish while foraging")
        plt.legend()
        plt.show()


# Create a simulation with a width and height of 20, 5 agents, and 10 food sources
simulation = ForagingSimulation(20, 20, 5, 10)

# Simulate the behavior of agents for 20 steps
simulation.simulate(50)

# Plot the initial and final positions of the agents
simulation.plot_positions()
