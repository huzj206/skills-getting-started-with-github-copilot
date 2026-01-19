import subprocess
import datetime
import os

# Set PYTHONPATH
os.environ['PYTHONPATH'] = 'src'

# Run pytest
result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v'], capture_output=True, text=True)

# Get timestamp
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'tests/test_log_{timestamp}.txt'

# Write to file
with open(filename, 'w') as f:
    f.write(result.stdout)
    if result.stderr:
        f.write('\nSTDERR:\n')
        f.write(result.stderr)

print(f'Log saved to {filename}')
print('STDOUT:')
print(result.stdout)
print('STDERR:')
print(result.stderr)