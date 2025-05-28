#!/bin/bash
# Update and install Java
sudo yum update -y
sudo amazon-linux-extras install java-openjdk11 -y

# Jenkins install
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum install -y jenkins git
sudo systemctl enable jenkins
sudo systemctl start jenkins

# SonarQube install
sudo yum install -y unzip wget
cd /opt
sudo wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-10.4.1.88267.zip
sudo unzip sonarqube-10.4.1.88267.zip
sudo mv sonarqube-10.4.1.88267 sonarqube
sudo useradd sonar
sudo chown -R sonar:sonar /opt/sonarqube

# Tạo systemd service cho SonarQube
cat <<EOF | sudo tee /etc/systemd/system/sonarqube.service
[Unit]
Description=SonarQube service
After=network.target

[Service]
Type=forking
ExecStart=/opt/sonarqube/bin/linux-x86-64/sonar.sh start
ExecStop=/opt/sonarqube/bin/linux-x86-64/sonar.sh stop
User=sonar
Group=sonar
Restart=always
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl enable sonarqube
sudo systemctl start sonarqube
