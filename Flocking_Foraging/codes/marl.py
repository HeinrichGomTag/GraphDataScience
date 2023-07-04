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
        separation_radius = 2  # Radius within which the agent avoids other agents
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

    @staticmethod
    def select_action():
        # Randomly select between "forage" and "flock" actions
        return random.choice(["forage", "flock"])


class Simulation:
    def __init__(self, width, height, num_agents, num_food_sources):
        self.width = width  # Width of the simulation area
        self.height = height  # Height of the simulation area
        self.agents = []  # List to store the agents
        self.initial_positions = []  # List to store the initial positions of agents
        self.final_positions = []  # List to store the final positions of agents
        self.food_sources = []  # List to store the food sources
        self.q_tables = {}  # Dictionary to store Q-tables of agents

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
            self.q_tables[agent] = {}  # Create an empty Q-table for the agent

        for _ in range(num_food_sources):
            x = random.uniform(
                0, width
            )  # Random x-coordinate within the simulation area
            y = random.uniform(
                0, height
            )  # Random y-coordinate within the simulation area
            self.food_sources.append((x, y))

    def calculate_reward(self, agent):
        # Calculate the reward for the agent based on the current state and action
        food_radius = 2  # Radius within which the agent is considered to have reached the food
        food_reward = 1  # Reward for reaching the food
        movement_reward = -0.1  # Penalty for movement
        proximity_reward = 0.2  # Reward for being close to food
        flocking_reward = 0.5  # Reward for being close to other agents

        for food in self.food_sources:
            dx = food[0] - agent.x  # Horizontal distance between the agent and the food
            dy = food[1] - agent.y  # Vertical distance between the agent and the food
            distance = math.sqrt(dx ** 2 + dy ** 2)  # Euclidean distance between the agent and the food

            if distance < food_radius:
                return food_reward

            if distance < 2 * food_radius:
                return proximity_reward

        # Check if the agent is close to other agents
        num_neighbors = 0
        for other_agent in self.agents:
            if other_agent != agent:
                dx = other_agent.x - agent.x  # Horizontal distance between the agent and its neighbor
                dy = other_agent.y - agent.y  # Vertical distance between the agent and its neighbor
                distance = math.sqrt(dx ** 2 + dy ** 2)  # Euclidean distance between the agent and its neighbor

                if distance < food_radius:
                    num_neighbors += 1

        if num_neighbors > 0:
            return flocking_reward

        return movement_reward

    def update_q_table(self, agent, state, action, reward, next_state):
        # Update the Q-table based on the agent's experience
        learning_rate = 0.1  # Learning rate
        discount_factor = 0.9  # Discount factor

        q_table = self.q_tables[agent]

        # Initialize the Q-value for the (state, action) pair if it doesn't exist
        if state not in q_table:
            q_table[state] = {action: 0}

        # Retrieve the Q-value for the (state, action) pair
        q_value = q_table[state].get(action, 0)

        # Calculate the maximum Q-value for the next state
        max_q_value = max(q_table.get(next_state, {}).values(), default=0)

        # Update the Q-value using the Q-learning formula
        new_q_value = (1 - learning_rate) * q_value + learning_rate * (
                reward + discount_factor * max_q_value
        )

        # Update the Q-value in the Q-table
        q_table[state][action] = new_q_value

    '''
    def print_q_tables(self):
        print("Q-tables for all agents:")
        for agent in self.agents:
            print(f"Agent: {agent}")
            q_table = self.q_tables[agent]
            for state in q_table:
                print(f"    State: {state}")
                for action in q_table[state]:
                    print(f"        Action: {action}, Q-value: {q_table[state][action]}")
    '''

    def print_last_actions_and_states(self):
        print("Q-summary for agents:")
        for agent in self.agents:
            print(f"Agent: {agent}")
            q_table = self.q_tables[agent]
            last_state = None
            last_action = None
            last_q_value = None
            for state in q_table:
                last_state = state
                for action in q_table[state]:
                    last_action = action
                    last_q_value = q_table[state][action]
            print(f"    Last State: {last_state}")
            print(f"    Last Action: {last_action}")
            print(f"    Last Q-value: {last_q_value}")

    @staticmethod
    def get_state(agent):
        # Retrieve the state of the agent
        return agent.x, agent.y, agent.orientation, agent.speed

    def get_action(self, agent, state):
        # Select an action for the agent based on the current state
        epsilon = 0.1  # Exploration rate

        if random.uniform(0, 1) < epsilon:
            # Explore: select a random action
            return random.choice(["forage", "flock"])
        else:
            # Exploit: select the action with the highest Q-value
            q_values = self.q_tables[agent].get(state, {})
            if q_values:
                max_q_value = max(q_values.values())
                actions_with_max_q_value = [
                    action for action, q_value in q_values.items() if q_value == max_q_value
                ]
                return random.choice(actions_with_max_q_value)
            else:
                return random.choice(["forage", "flock"])

    def run(self, num_iterations):
        for _ in range(num_iterations):
            for agent in self.agents:
                state = self.get_state(agent)  # Get current state of the agent
                action = self.get_action(agent, state)  # Get action for the agent
                reward = 0  # Initialize reward for the agent

                if action == "forage":
                    agent.forage(self.food_sources)
                    reward = self.calculate_reward(agent)
                elif action == "flock":
                    agent.flock(self.agents)
                    reward = self.calculate_reward(agent)

                next_state = self.get_state(agent)  # Get next state of the agent
                self.update_q_table(agent, state, action, reward, next_state)

        self.visualize()  # Visualize the simulation at each iteration

    def visualize(self):
        # Visualize the simulation
        plt.figure(figsize=(10, 10))
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)

        # Plot food sources
        food_x = [food[0] for food in self.food_sources]
        food_y = [food[1] for food in self.food_sources]
        plt.scatter(food_x, food_y, color="green", marker="o", label="Food")

        # Plot agents
        agent_x = [agent.x for agent in self.agents]
        agent_y = [agent.y for agent in self.agents]
        plt.scatter(
            agent_x,
            agent_y,
            color="red",
            marker="o",
            label="Final Positions",
        )

        # Plot initial positions of agents
        initial_x = [pos[0] for pos in self.initial_positions]
        initial_y = [pos[1] for pos in self.initial_positions]
        plt.scatter(
            initial_x,
            initial_y,
            color="blue",
            marker="o",
            label="Initial Positions",
        )

        plt.legend()
        plt.show()


# Create a simulation with a width of 200, height of 200, 50 agents, and 30 food sources
simulation = Simulation(200, 200, 50, 30)

# Run the simulation for 300 iterations
simulation.run(300)

# Print the Q-table
# simulation.print_q_tables()
simulation.print_last_actions_and_states()
