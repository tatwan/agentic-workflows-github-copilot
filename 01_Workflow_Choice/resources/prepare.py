"""Copy only the task input and fixed script into the project."""
from pathlib import Path
import shutil

resources = Path(__file__).resolve().parent
project = resources.parent.parent / 'orders-analytics'
if not (project / 'pyproject.toml').is_file():
    raise SystemExit('FAIL run from a complete repository copy')
work = project / 'work' / 'lab01'
work.mkdir(parents=True, exist_ok=True)
shutil.copyfile(resources / 'orders.csv', work / 'input.csv')
shutil.copyfile(resources / 'summarize.py', work / 'summarize.py')
agents = project / '.github' / 'agents'
agents.mkdir(parents=True, exist_ok=True)
shutil.copyfile(resources / 'supplied-context.agent.md', agents / 'lab01-supplied-context.agent.md')
print('Prepared work/lab01/input.csv, work/lab01/summarize.py and the supplied-context profile')
print('Existing reports were kept; save them before repeating a run.')
