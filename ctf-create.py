import os
import yaml

# Load the ctf.yml file
with open('ctf.yml', 'r') as f:
    ctf_config = yaml.safe_load(f)

teams = ctf_config['ctf']['teams']
services = ctf_config['ctf']['services']

# Create Dockerfile.ctf-admin
with open('Dockerfile.ctf-admin', 'w') as f:
    f.write('FROM ubuntu:20.04\n')
    f.write('ENV DEBIAN_FRONTEND=noninteractive\n')
    f.write('RUN apt-get update && apt-get install -y \\\n')
    f.write('    openssh-client sshpass ansible sudo vim make python3-venv python3-pip \\\n')
    f.write('    && apt-get clean\n')
    f.write('RUN useradd -m -d /home/ctf-admin -s /bin/bash ctf-admin && echo "ctf-admin:123" | chpasswd\n')
    f.write('RUN echo "ctf-admin ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers\n')
    f.write('RUN pip3 install requests')
    f.write('WORKDIR /home/ctf-admin\n')
    f.write('CMD tail -f /dev/null\n') # Use a simple command for Docker Compose v1.17.1

# Create Dockerfile.ctf
with open('Dockerfile.ctf', 'w') as f:
    f.write('FROM ubuntu:20.04\n')
    f.write('ENV DEBIAN_FRONTEND=noninteractive\n')
    f.write('RUN apt-get update && apt-get install -y \\\n')
    f.write('    openssh-server sudo vim python3-venv python3-pip \\\n')
    f.write('    && apt-get clean\n')
    f.write('RUN useradd -m -d /home/ctf -s /bin/bash ctf && echo "ctf:123" | chpasswd\n')
    f.write('RUN echo "ctf ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers\n')
    f.write('WORKDIR /home/ctf\n')
    f.write('CMD /usr/sbin/sshd -D\n') # Use a simple command for Docker Compose v1.17.1

# Create docker-compose.yml (compatible with v1.17.1)
    teams = ['red-team', 'fuchsia-team']
services = ['ssh', 'web', 'app']  # adjust as needed

with open('docker-compose.yml', 'w') as f:
    f.write('version: "3"\n')
    f.write('services:\n')

    # Admin service
    f.write('  ctf-admin:\n')
    f.write('    build:\n')
    f.write('      context: .\n')
    f.write('      dockerfile: Dockerfile.ctf-admin\n')
    f.write('    container_name: ctf-admin\n')
    f.write('    volumes:\n')
    f.write('      - ./ansible-playbooks:/ansible-playbooks\n')
    f.write('      - ./test.sh:/home/ctf-admin/test.sh\n')
    f.write('    networks:\n')
    f.write('      - ctf-network\n')
    f.write('    command: ["tail", "-f", "/dev/null"]\n\n')

    # Team containers
    for idx, team in enumerate(teams):
        base_port = 6000 + idx * 10
        f.write(f'  {team}:\n')
        f.write('    build:\n')
        f.write('      context: .\n')
        f.write('      dockerfile: Dockerfile.ctf\n')
        f.write(f'    container_name: {team}\n')
        f.write('    networks:\n')
        f.write('      - ctf-network\n')
        f.write('    ports:\n')
        f.write(f'      - "{base_port}:22"\n')           # SSH
        f.write(f'      - "{base_port + 1}:5000"\n')    # Web
        f.write(f'      - "{base_port + 2}:5001"\n')    # App
        f.write('\n')

    # Network declaration
    f.write('networks:\n')
    f.write('  ctf-network:\n')

# Create Ansible Playbooks (start.yml, stop.yml, inventory.ini)
os.makedirs('ansible-playbooks', exist_ok=True)

# Generate inventory.ini file
with open('ansible-playbooks/inventory.ini', 'w') as f:
    f.write('[ctf_servers]\n')
    for team in teams:
        f.write(f'{team} ansible_host={team}\n')
    f.write('\n[ctf_servers:vars]\n')
    f.write('ansible_port=22\n')
    f.write('ansible_user=ctf\n')
    f.write('ansible_ssh_pass=123\n')
    f.write('ansible_ssh_common_args=-o StrictHostKeyChecking=no\n')

# Generate start.yml playbook
with open('ansible-playbooks/start.yml', 'w') as f:
    f.write('- name: Set up servers\n')
    f.write('  hosts: ctf_servers\n')
    f.write('  tasks:\n')
    for service in services:
        f.write(f'    - name: Run start.sh in services/{service}\n')
        f.write('      ansible.builtin.shell: |\n')
        f.write(f'        cd /home/ctf/services/{service} && bash -x start.sh\n')
        f.write('      args:\n')
        f.write('        chdir: /home/ctf\n')

# Generate stop.yml playbook
with open('ansible-playbooks/stop.yml', 'w') as f:
    f.write('- name: Stop services\n')
    f.write('  hosts: ctf_servers\n')
    f.write('  tasks:\n')
    for service in services:
        f.write(f'    - name: Run stop.sh in services/{service}\n')
        f.write('      ansible.builtin.shell: |\n')
        f.write(f'        cd /home/ctf/services/{service} && ./stop.sh\n')
        f.write('      args:\n')
        f.write('        chdir: /home/ctf\n')

# Generate start.sh and stop.sh for each service
os.makedirs('services', exist_ok=True)

for service in services:
    service_dir = f'services/service-{service}'

    # Create the service directory if it doesn't exist
    if not os.path.exists(service_dir):
        os.makedirs(service_dir)

    # Create start.sh for each service
    start_script_path = os.path.join(service_dir, 'start.sh')
    with open(start_script_path, 'w') as f:
        f.write(f"""#!/bin/bash
echo "Starting service {service}..."
cd /home/ctf/services/service-{service}
FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
""")

    # Create stop.sh for each service
    stop_script_path = os.path.join(service_dir, 'stop.sh')
    with open(stop_script_path, 'w') as f:
        f.write(f"""#!/bin/bash
echo "Stopping service {service}..."
pkill -f "flask run"
""")

    # Make the scripts executable
    os.chmod(start_script_path, 0o755)
    os.chmod(stop_script_path, 0o755)

