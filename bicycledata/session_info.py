import json
import os

import yaml


class SessionInfo:
  """Read and write session info stored in a markdown file whose frontmatter
  is YAML or JSON.

  1) YAML-style frontmatter using --- delimiters
  2) JSON-style frontmatter using a code block labeled ```json immediately at the top of the file

  The rest of the file after the frontmatter is treated as markdown body.
  """

  def __init__(self, path: str):
    self.path = path

  def read(self):
    if not os.path.exists(self.path):
      raise FileNotFoundError(self.path)

    with open(self.path, 'r', encoding='utf-8') as f:
      content = f.read()

    # Try YAML-style frontmatter starting with ---
    if content.startswith('---'):
      parts = content.split('\n')
      # find the closing '---'
      try:
        end_idx = parts.index('---', 1)
        front_lines = parts[1:end_idx]
        rest_lines = parts[end_idx+1:]
        front = '\n'.join(front_lines).strip()
        body = '\n'.join(rest_lines)

        try:
          metadata = yaml.safe_load(front) or {}
          if not isinstance(metadata, dict):
            raise ValueError('Frontmatter did not parse to a mapping')
        except Exception as e:
          raise ValueError(f'Invalid YAML frontmatter: {e}')
        return metadata, body
      except ValueError:
        pass

    # Try json-style frontmatter starting with ```json
    if content.startswith('```json'):
      parts = content.split('\n')
      # find the closing ```
      try:
        end_idx = parts.index('```', 1)
        front_lines = parts[1:end_idx]
        rest_lines = parts[end_idx+1:]
        front = '\n'.join(front_lines).strip()
        body = '\n'.join(rest_lines)

        try:
          metadata = json.loads(front)
        except Exception as e:
          raise ValueError('Invalid JSON in fenced code block frontmatter')
        return metadata, body
      except ValueError:
        pass

    # No frontmatter found
    return {}, content

  def write(self, metadata, body = None) -> None:
    front = json.dumps(metadata, indent=2, ensure_ascii=False)
    if body is None:
      body = ''

    content = '```json\n' + front + '\n```\n\n' + body

    dirpath = os.path.dirname(self.path)
    if dirpath and not os.path.exists(dirpath):
      os.makedirs(dirpath, exist_ok=True)

    with open(self.path, 'w', encoding='utf-8') as f:
      f.write(content)

  @staticmethod
  def read_from(path: str):
    return SessionInfo(path).read()

  @staticmethod
  def write_to(path: str, metadata, body = None) -> None:
    SessionInfo(path).write(metadata, body)
