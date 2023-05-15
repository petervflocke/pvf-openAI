# xpylint: disable=missing-module-docstring
# xpylint: disable=missing-class-docstring
# xpylint: disable=missing-function-docstring

# # Sample dictionary data
# data = {'name': 'John', 'age': 25, 'city': 'New York'}

# # Remove the 'age' key:value pair
# del data['age']

# # Print the updated dictionary
# print(data)


# data = {"name": "John", "age": 30, "job": "pp"}
# data = {"xname": "John", "age": 30, "job": "pp"}

# match data:
#     case {"name": name, "age": age, "job": "developer"} if age > 20:
#         print(f"{name} is a developer over 20 years old.")
#     case {"name": name, "age": age, "job": _}:
#         print(f"{name} works as something other than a developer.")
#     case _:
#         print("Data does not match any pattern.")

import threading
import time
import enum

# Define the states of your state machine using an Enum
class State(enum.Enum):
    START = 1
    MIDDLE = 2
    END = 3

# This class will represent your state machine
class Assistant:
    def __init__(self):
        self.state = State.START

    def update_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state

# These classes represent different threads that will interact with the state machine
class WorkerThread(threading.Thread):
    def __init__(self, assistant, new_state):
        threading.Thread.__init__(self)
        self.assistant = assistant
        self.new_state = new_state

    def run(self):
        print(f"Worker {self.name} is starting. Updating state to {self.new_state}")
        with threading.Lock():  # This ensures that only one thread updates the state at a time
            self.assistant.update_state(self.new_state)
        print(f"Worker {self.name} has finished. Current state: {self.assistant.get_state()}")


def main():
    assistant = Assistant()
    
    # Create and start two worker threads
    worker1 = WorkerThread(assistant, State.MIDDLE)
    worker2 = WorkerThread(assistant, State.END)

    worker1.start()
    time.sleep(1)  # Ensure worker1 has chance to complete before worker2 starts
    worker2.start()

    # Wait for both workers to finish
    worker1.join()
    worker2.join()

    print(f"Final state: {assistant.get_state()}")

if __name__ == "__main__":
    main()
