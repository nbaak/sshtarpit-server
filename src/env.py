

def load(file_path:str) -> dict[str, str]:
    env_vars = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()

            # Ignore empty lines and comments
            if not line or line.startswith("#"):
                continue

            key, value = line.split('=', 1)
            
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            env_vars[key] = value

    return env_vars


def test():
    env_vars = load(".env")
    print(env_vars.get("test", "NOPE!"))

    
if __name__ == "__main__":
    test()
