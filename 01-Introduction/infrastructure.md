# Infrastructure Setup

Guide to using GCP service

## Prerequisite
1. Create a new Gmail account for $300 free credit on GCP
2. Create an account on GCP and setup a billing
---
## Step 1: Login into the GCP console and create a project

Name: `mlops-demo`

![Project Creation](/images/01.png)


## Step 2: Create an instance using Compute Engine

Configuration:
* Name: `demo-vm`
* Region: `us-east1`
* Zone: `us-east-b`
* Series: `N2`
* Machine Type: `n2-standard-2`
* Boot disk: 
    * Image: `Ubuntu 22.04 LTS`
* Firewall: Check both
    * Allow HTTP traffic
    * Allow HTTPS traffic

![Project Creation](/images/02.png)

![Project Creation](/images/03.png)

## Step 3: Assign static public ip

> View Network details > IP addresses > Reserve a static address

![Project Creation](/images/04.png)

![Project Creation](/images/05.png)

## Step 4: Enable SSH 

Generate a SSH key

```bash
ssh-keygen -t rsa -f ~/.ssh/mlops-demo -C mlops_zoomcamp
```

Copy the content of `mlops-demo.pub`
```bash
cat ~/.ssh/mlops-demo.pub
```

On GCP console, enter the copied public key
> Setting > Metadata > SSH Key 

![Project Creation](/images/06.png)

## Step 6: SSH into Instance

Replace your instance public IP address

```bash
ssh -i ~/.ssh/mlops-demo mlops_zoomcamp@35.196.19.116
```

Optional, Add host to hostname file for easy login 

Enter the following into `~/.ssh/config`
```bash
nano ~/.ssh/config
```
``` bash
Host gcp-mlops_demo
    HostName 35.196.19.116 # VM Public IP
    User mlops_zoomcamp # VM user
    IdentityFile ~/.ssh/mlops-demo # Private SSH key file
    StrictHostKeyChecking no
```

Further Use
```bash
ssh gcp-mlops_demo
```

## Step 7: Install the dependency

* Anaconda

```bash
cd ~
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
```

* Docker

```bash
sudo apt install docker.io
```

* Docker-Compose

```bash
sudo apt install docker-compose
```

* Add current user to docker group

```bash
sudo usermod -aG docker mlops_zoomcamp
```
* Verify Installation 

```bash
which python
# /home/mlops_zoomcamp/anaconda3/bin/python

which docker
# /usr/bin/docker

which docker-compose
# /usr/bin/docker-compose

docker run hello-world
```

* Run Jupyter Notebook
```bash
jupyter notebook
```
Copy the Password or Token


## Step 7: Connect to VS Code

* Install `Remote SSH` extension
* Enable port forwarding 8888 to localhost 8888

Refer instructor video for detailed steps


## Step 8: Start using Jupyter Notebook

Visit `localhost:8888` to start using jupyter
Past the copied Password or Token

![Project Creation](/images/07.png)

## All Set !
If you found this helpful, please star this repo. Thanks!

# Ends
