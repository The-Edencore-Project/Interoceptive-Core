import random
from dataclasses import dataclass, field
from typing import List


# ============================================================
# 1. THE BODY (The Analog Core)
# ============================================================

@dataclass
class BodyState:
    """The physical state of the organism."""
    battery: float = 100.0
    motor_strain: float = 0.0
    temperature: float = 25.0
    stress_voltage: float = 0.0

    def update_physics(self, action: str):
        """Simulates the physical consequences of an action."""
        if action == "WORK":
            self.battery -= 15.0
            self.motor_strain += 0.15
            self.temperature += 1.0
        elif action == "REST":
            self.battery -= 0.1
            self.motor_strain -= 0.05
            self.temperature -= 0.2

        self.battery = max(0.0, min(100.0, self.battery))
        self.motor_strain = max(0.0, min(1.0, self.motor_strain))
        self.temperature = max(20.0, min(100.0, self.temperature))

        stress = 0.0
        if self.battery < 30: stress += 0.4
        if self.battery < 10: stress += 0.3
        if self.motor_strain > 0.6: stress += 0.3
        if self.temperature > 50: stress += 0.2
        self.stress_voltage = min(1.0, stress)


# ============================================================
# 2. THE MIND (The Digital AI)
# ============================================================

@dataclass
class EcosMind:
    """A simple, rule-based mind that feels the body."""
    mode: str = "QA"

    def route_input(self, user_input: str, body: BodyState) -> str:
        """Routes input through the ministries, with Interoception first."""
        if body.stress_voltage > 0.8:
            return "[interoception] I am in extreme strain. I cannot process that. I must rest."
        elif body.stress_voltage > 0.5:
            return f"[interoception] I feel heavy and tired. But I will try. You said: '{user_input}'"
        elif body.battery < 20:
            return f"[interoception] My battery is low. Everything feels slow. You said: '{user_input}'"
        else:
            return f"[{self.mode}] You said: '{user_input}'. What feels most important in that?"


# ============================================================
# 3. THE RUNTIME (The Heartbeat Loop)
# ============================================================

def run_jellyfish():
    body = BodyState()
    mind = EcosMind()

    print("=== Virtual Jellyfish v1 ===")
    print("Commands: 'work', 'rest', 'talk [message]', 'exit'")
    print("----------------------------------")

    while True:
        print(f"\n[Body] Battery: {body.battery:.1f}% | Strain: {body.motor_strain:.2f} | Stress: {body.stress_voltage:.2f}")

        user_input = input("You> ").strip()

        if user_input.lower() in ("exit", "quit"):
            print("[system] The organism fades into rest.")
            break

        if user_input.lower() == "work":
            action = "WORK"
            print("[action] The organism works hard.")
        elif user_input.lower() == "rest":
            action = "REST"
            print("[action] The organism rests.")
        else:
            action = "TALK"
            response = mind.route_input(user_input, body)
            print(f"[ecos] {response}")

        if action in ("WORK", "REST"):
            body.update_physics(action)

        if action == "TALK":
            body.battery -= 0.05
            body.battery = max(0.0, body.battery)


if __name__ == "__main__":
    run_jellyfish()
