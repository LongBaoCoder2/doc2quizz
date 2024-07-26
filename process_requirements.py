import re

def parse_and_write_requirements(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Use regex to capture package name and version
            match = re.match(r'(\S+)\s+(\S+)', line.strip())
            if match:
                package_name, version = match.groups()
                outfile.write(f'{package_name}=={version}\n')

if __name__ == "__main__":
    input_file = 'requirement.txt'  # Input file with provided text list of packages
    output_file = 'requirements.txt'  # Output file in proper requirements.txt format

    parse_and_write_requirements(input_file, output_file)
