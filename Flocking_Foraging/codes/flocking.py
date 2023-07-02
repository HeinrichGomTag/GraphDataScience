import random  # Import the random module for generating random numbers
import math  # Import the math module for mathematical operations
import matplotlib.pyplot as plt  # Import the matplotlib.pyplot module for plotting



class Agent:
    def __init__(self, x, y, speed, orientation):
        self.x = x  # Set the initial x-coordinate of the agent
        self.y = y  # Set the initial y-coordinate of the agent
        self.speed = speed  # Set the speed of the agent
        self.orientation = orientation  # Set the orientation (direction) of the agent

    def flock(self, agents):
        separation_radius = 2  # Radius for separation to avoid collisions
        cohesion_radius = 5  # Radius for cohesion for grouping
        alignment_radius = 5  # Radius for alignment for common direction

        separation_force = [0, 0]  # Separation force
        cohesion_force = [0, 0]  # Cohesion force
        alignment_force = [0, 0]  # Alignment force

        num_neighbors = 0  # Counter for the number of neighboring agents

        for agent in agents:
            if agent != self:  # Exclude self from the neighboring agents
                dx = agent.x - self.x  # Calculate the difference in x-coordinates
                dy = agent.y - self.y  # Calculate the difference in y-coordinates
                distance = math.sqrt(
                    dx**2 + dy**2
                )  # Calculate the distance between agents

                # Separation
                if (
                    distance < separation_radius
                ):  # If the agent is within the separation radius
                    separation_force[0] -= (
                        dx / distance
                    )  # Add separation force in the x-direction
                    separation_force[1] -= (
                        dy / distance
                    )  # Add separation force in the y-direction

                # Cohesion
                if (
                    distance < cohesion_radius
                ):  # If the agent is within the cohesion radius
                    cohesion_force[0] += dx  # Add cohesion force in the x-direction
                    cohesion_force[1] += dy  # Add cohesion force in the y-direction
                    num_neighbors += 1  # Increment the neighbor count

                # Alignment
                if (
                    distance < alignment_radius
                ):  # If the agent is within the alignment radius
                    alignment_force[0] += agent.speed * math.cos(
                        agent.orientation
                    )  # Add alignment force in the x-direction
                    alignment_force[1] += agent.speed * math.sin(
                        agent.orientation
                    )  # Add alignment force in the y-direction

        # Average cohesion and alignment forces
        if num_neighbors > 0:  # If there are neighboring agents
            cohesion_force[
                0
            ] /= (
                num_neighbors  # Calculate the average cohesion force in the x-direction
            )
            cohesion_force[
                1
            ] /= (
                num_neighbors  # Calculate the average cohesion force in the y-direction
            )
            alignment_force[
                0
            ] /= num_neighbors  # Calculate the average alignment force in the x-direction
            alignment_force[
                1
            ] /= num_neighbors  # Calculate the average alignment force in the y-direction

        # Update agent's position and velocity
        self.x += self.speed * math.cos(
            self.orientation
        )  # Update x-coordinate based on speed and orientation
        self.y += self.speed * math.sin(
            self.orientation
        )  # Update y-coordinate based on speed and orientation

        # Apply separation, cohesion, and alignment forces
        self.x += (
            separation_force[0] + cohesion_force[0] + alignment_force[0]
        )  # Update x-coordinate based on forces
        self.y += (
            separation_force[1] + cohesion_force[1] + alignment_force[1]
        )  # Update y-coordinate based on forces

    def update_orientation(self):
        self.orientation = math.atan2(
            math.sin(self.orientation), math.cos(self.orientation)
        )
        # Update the orientation to ensure it stays within the range of [0, 2 * pi)


class FlockSimulation:
    def __init__(self, width, height, num_agents):
        self.width = width  # Set the width of the simulation environment
        self.height = height  # Set the height of the simulation environment
        self.agents = []  # Initialize an empty list to store the agents
        self.initial_positions = []  # List to store initial positions
        self.final_positions = []  # List to store final positions
        for _ in range(num_agents):
            x = random.uniform(
                0, width
            )  # Generate a random x-coordinate within the environment width
            y = random.uniform(
                0, height
            )  # Generate a random y-coordinate within the environment height
            speed = random.uniform(0.1, 1)  # Generate a random speed for the agent
            orientation = random.uniform(
                0, 2 * math.pi
            )  # Generate a random orientation for the agent
            agent = Agent(
                x, y, speed, orientation
            )  # Create a new Agent object with the generated values
            self.agents.append(agent)  # Add the agent to the list
            self.initial_positions.append((x, y))  # Store initial position

    def simulate(self, num_steps):
        steps = 1
        for _ in range(num_steps):
            for agent in self.agents:
                agent.flock(self.agents)  # Make the agent flock with other agents
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
        for agent in self.agents:
            print(
                f"Agent at ({agent.x}, {agent.y}) with speed {agent.speed} and orientation {agent.orientation} at {num_steps} steps"
            )
        print("------")

    def plot_positions(self):
        initial_x = [pos[0] for pos in self.initial_positions]
        initial_y = [pos[1] for pos in self.initial_positions]
        final_x = [pos[0] for pos in self.final_positions]
        final_y = [pos[1] for pos in self.final_positions]

        plt.scatter(initial_x, initial_y, color="blue", label="Initial Position")
        plt.scatter(final_x, final_y, color="red", label="Final Position")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Flocking: Initial VS Final Positions of Fish")
        plt.legend()
        plt.show()


# Create a flock simulation with 10 agents
simulation = FlockSimulation(10, 10, 10)

# Simulate the flocking behavior for 20 time steps
simulation.simulate(20)

# Plot the initial and final positions of the agents
simulation.plot_positions()
