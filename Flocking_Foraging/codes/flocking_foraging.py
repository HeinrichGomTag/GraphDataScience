import random
import math
import matplotlib.pyplot as plt


class Agent:
    def __init__(self, x, y, speed, orientation):
        self.x = x  # Agent's x-coordinate
        self.y = y  # Agent's y-coordinate
        self.speed = speed  # Agent's speed
        self.orientation = orientation  # Agent's orientation

    def forage(self, food_sources):
        detection_radius = 5  # Radius within which the agent can detect food
        closest_food = None  # Variable to store the closest food source
        closest_distance = (
            math.inf
        )  # Variable to store the closest distance to a food source

        for food in food_sources:
            dx = (
                    food[0] - self.x
            )  # Horizontal distance between the agent and the food source
            dy = (
                    food[1] - self.y
            )  # Vertical distance between the agent and the food source
            distance = math.sqrt(
                dx ** 2 + dy ** 2
            )  # Euclidean distance between the agent and the food source

            if distance < detection_radius and distance < closest_distance:
                closest_food = food
                closest_distance = distance
        # If there is a closest food source, move towards it; otherwise, move in a random direction
        if closest_food is not None:
            dx = closest_food[0] - self.x
            dy = closest_food[1] - self.y
            angle = math.atan2(dy, dx)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        else:
            angle = random.uniform(0, 2 * math.pi)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)

    def flock(self, agents):
        separation_radius = 4  # Radius within which the agent avoids other agents
        cohesion_radius = 5  # Radius within which the agent aligns with other agents
        alignment_radius = (
            5  # Radius within which the agent aligns its orientation with other agents
        )

        separation_force = [0, 0]  # Force vector for separation
        cohesion_force = [0, 0]  # Force vector for cohesion
        alignment_force = [0, 0]  # Force vector for alignment

        num_neighbors = 0  # Counter for the number of neighboring agents

        for agent in agents:
            if agent != self:
                dx = (
                        agent.x - self.x
                )  # Horizontal distance between the agent and its neighbor
                dy = (
                        agent.y - self.y
                )  # Vertical distance between the agent and its neighbor
                distance = math.sqrt(
                    dx ** 2 + dy ** 2
                )  # Euclidean distance between the agent and its neighbor

                if distance < separation_radius:
                    separation_force[0] -= (
                            dx / distance
                    )  # Calculate separation force in the x-axis
                    separation_force[1] -= (
                            dy / distance
                    )  # Calculate separation force in the y-axis

                if distance < cohesion_radius:
                    cohesion_force[0] += dx  # Calculate cohesion force in the x-axis
                    cohesion_force[1] += dy  # Calculate cohesion force in the y-axis
                    num_neighbors += 1

                if distance < alignment_radius:
                    alignment_force[0] += agent.speed * math.cos(
                        agent.orientation
                    )  # Calculate alignment force in the x-axis
                    alignment_force[1] += agent.speed * math.sin(
                        agent.orientation
                    )  # Calculate alignment force in the y-axis

        if num_neighbors > 0:
            cohesion_force[0] /= num_neighbors  # Average cohesion force in the x-axis
            cohesion_force[1] /= num_neighbors  # Average cohesion force in the y-axis
            alignment_force[0] /= num_neighbors  # Average alignment force in the x-axis
            alignment_force[1] /= num_neighbors  # Average alignment force in the y-axis

        self.x += self.speed * math.cos(
            self.orientation
        )  # Update agent's x-coordinate based on its speed and orientation
        self.y += self.speed * math.sin(
            self.orientation
        )  # Update agent's y-coordinate based on its speed and orientation

        self.x += (
                separation_force[0] + cohesion_force[0] + alignment_force[0]
        )  # Update agent's x-coordinate based on separation, cohesion, and alignment forces
        self.y += (
                separation_force[1] + cohesion_force[1] + alignment_force[1]
        )  # Update agent's y-coordinate based on separation, cohesion, and alignment forces

    def update_orientation(self):
        self.orientation = math.atan2(
            math.sin(self.orientation), math.cos(self.orientation)
        )


class Simulation:
    def __init__(self, width, height, num_agents, num_food_sources):
        self.width = width  # Width of the simulation area
        self.height = height  # Height of the simulation area
        self.agents = []  # List to store the agents
        self.initial_positions = []  # List to store the initial positions of agents
        self.final_positions = []  # List to store the final positions of agents
        self.food_sources = []  # List to store the food sources

        for _ in range(num_agents):
            x = random.uniform(
                0, width
            )  # Random x-coordinate within the simulation area
            y = random.uniform(
                0, height
            )  # Random y-coordinate within the simulation area
            speed = random.uniform(0.1, 1)  # Random speed of the agent
            orientation = random.uniform(
                0, 2 * math.pi
            )  # Random orientation of the agent
            agent = Agent(
                x, y, speed, orientation
            )  # Create an agent with the specified attributes
            self.agents.append(agent)
            self.initial_positions.append((x, y))

        for _ in range(num_food_sources):
            x = random.uniform(
                0, width
            )  # Random x-coordinate within the simulation area
            y = random.uniform(
                0, height
            )  # Random y-coordinate within the simulation area
            self.food_sources.append((x, y))

    def simulate(self, num_steps):
        for step in range(num_steps):
            for agent in self.agents:
                agent.forage(self.food_sources)  # Agent forages for food
                agent.flock(self.agents)  # Agent aligns with and avoids other agents
                agent.update_orientation()  # Update agent's orientation

                # Wrap around the simulation area (toroidal boundary conditions)
                if agent.x < 0 or agent.x > self.width:
                    agent.x = agent.x % self.width

                if agent.y < 0 or agent.y > self.height:
                    agent.y = agent.y % self.height

            if step == num_steps - 1:
                for agent in self.agents:
                    self.final_positions.append((agent.x, agent.y))

    def print_state(self):
        for i, agent in enumerate(self.agents):
            print(
                f"Agent {i + 1}: position=({agent.x}, {agent.y}), speed={agent.speed:.2f}"
            )

    def plot_positions(self):
        plt.figure(figsize=(8, 6))  # Create a new figure with the specified size
        plt.scatter(
            *zip(*self.initial_positions), color="blue", label="Initial Position"
        )  # Plot the initial positions of the agents as blue dots
        plt.scatter(
            *zip(*self.final_positions), color="red", label="Final Position"
        )  # Plot the final positions of the agents as red dots
        plt.scatter(
            *zip(*self.food_sources), color="green", label="Food Sources"
        )  # Plot the food sources as green dots
        plt.xlim(0, self.width)  # Set the x-axis and y-axis limits
        plt.ylim(0, self.height)
        plt.xlabel("X")  # Set the x and y -axis label
        plt.ylabel("Y")
        plt.title("Foraging + Flocking")  # Set the title of the plot
        plt.legend()  # Display the legend
        plt.show()  # Show the plot


# Combined Foraging and Flocking Simulation
simulation = Simulation(
    20, 20, 10, 4
)  # Create a simulation with a width of 20, height of 20, 10 agents, and 4 food sources
simulation.simulate(150)  # Run the simulation for 150 steps
simulation.print_state()  # Print the final state of the agents
simulation.plot_positions()  # Plot the initial and final positions of the agents, along with the food sources
