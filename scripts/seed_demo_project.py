import os

def seed():
    os.makedirs("backend/data/projects", exist_ok=True)
    print("Demo project seeded.")

if __name__ == "__main__":
    seed()
