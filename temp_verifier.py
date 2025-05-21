import sys
# Add src directory to Python path to allow importing config_parser
sys.path.append('./src')

try:
    from config_parser import load_config
    config = load_config("configs/sma_cross.yaml")
    if config:
        print("Successfully loaded config")
        # Optionally print the loaded config to verify content
        # import json
        # print(json.dumps(config, indent=2))
    else:
        print("Failed to load config: No content or empty file.")
except Exception as e:
    print(f"Failed to load config: {e}")
