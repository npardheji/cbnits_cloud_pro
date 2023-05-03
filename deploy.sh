#!/bin/bash
docker stop custodian_policies
docker rm custodian_policies
docker login -u USER_DOCKER -p PASSWORD_DOCKER
docker pull devopscloudarmour/custodian_policies:VERSION
docker run --name custodian_policies -p 5000:5000 -d devopscloudarmour/custodian_policies:VERSION