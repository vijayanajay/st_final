import yaml

def load_config(file_path: str) -> dict:
  """
  Loads a YAML configuration file and returns its content as a dictionary.

  Args:
    file_path: The path to the YAML configuration file.

  Returns:
    A dictionary containing the parsed YAML content.

  Raises:
    FileNotFoundError: If the specified file does not exist.
    yaml.YAMLError: If the file content is not valid YAML.
  """
  try:
    with open(file_path, 'r') as f:
      config = yaml.safe_load(f)
    return config
  except FileNotFoundError:
    raise
  except yaml.YAMLError:
    raise
