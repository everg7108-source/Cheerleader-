import random
import uuid
from typing import List, Dict


# ======================================================
# Global Memory
# ======================================================

class GlobalMemory:

    def __init__(self):
        self.entries = []

    def add(self, data):
        data["id"] = str(uuid.uuid4())
        self.entries.append(data)

    def query(self, keyword):
        return [e for e in self.entries if keyword in str(e)]

    def summary(self):
        return len(self.entries)


# ======================================================
# Base Agent
# ======================================================

class Agent:

    def __init__(self, name, memory):
        self.name = name
        self.memory = memory

    def act(self):
        pass


# ======================================================
# Research Agent
# ======================================================

class ResearchAgent(Agent):

    def act(self):

        topic = random.choice([
            "memory systems",
            "reasoning models",
            "multi agent cooperation",
            "world simulation",
        ])

        discovery = {
            "type": "research",
            "topic": topic,
            "insight": f"Possible improvement in {topic}"
        }

        self.memory.add(discovery)

        return discovery


# ======================================================
# Hypothesis Agent
# ======================================================

class HypothesisAgent(Agent):

    def act(self):

        research = random.choice(self.memory.entries)

        hypothesis = {
            "type": "hypothesis",
            "idea": f"If implemented, {research.get('topic','idea')} may improve capability"
        }

        self.memory.add(hypothesis)

        return hypothesis


# ======================================================
# Experiment Agent
# ======================================================

class ExperimentAgent(Agent):

    def act(self):

        hypothesis = random.choice(self.memory.entries)

        score = random.random()

        experiment = {
            "type": "experiment",
            "hypothesis": hypothesis,
            "score": score
        }

        self.memory.add(experiment)

        return experiment


# ======================================================
# Critic Agent
# ======================================================

class CriticAgent(Agent):

    def act(self):

        experiments = [e for e in self.memory.entries if e["type"] == "experiment"]

        if not experiments:
            return None

        best = max(experiments, key=lambda x: x["score"])

        evaluation = {
            "type": "evaluation",
            "best_score": best["score"]
        }

        self.memory.add(evaluation)

        return evaluation


# ======================================================
# Evolution Agent
# ======================================================

class EvolutionAgent(Agent):

    def __init__(self, name, memory, ecosystem):
        super().__init__(name, memory)
        self.ecosystem = ecosystem

    def act(self):

        if random.random() < 0.3:

            new_agent = ExperimentAgent(
                f"experiment_agent_{uuid.uuid4().hex[:4]}",
                self.memory
            )

            self.ecosystem.add_agent(new_agent)

            return {"spawned": new_agent.name}


# ======================================================
# Ecosystem Coordinator
# ======================================================

class Ecosystem:

    def __init__(self):

        self.memory = GlobalMemory()

        self.agents: List[Agent] = []

    def add_agent(self, agent):

        self.agents.append(agent)

    def cycle(self):

        for agent in self.agents:

            result = agent.act()

            if result:
                print(agent.name, "→", result)

    def run(self, steps=10):

        for i in range(steps):

            print("\n--- Ecosystem Cycle", i + 1, "---")

            self.cycle()

        print("\nMemory size:", self.memory.summary())


# ======================================================
# Bootstrapping the Proto-AGI Ecosystem
# ======================================================

if __name__ == "__main__":

    eco = Ecosystem()

    eco.add_agent(ResearchAgent("research_1", eco.memory))
    eco.add_agent(HypothesisAgent("hypothesis_1", eco.memory))
    eco.add_agent(ExperimentAgent("experiment_1", eco.memory))
    eco.add_agent(CriticAgent("critic_1", eco.memory))
    eco.add_agent(EvolutionAgent("evolution_1", eco.memory, eco))

    eco.run(20)
