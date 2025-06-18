# Sonarqube

## Requirements
Start the sonarqube by running `podman-compose.yml`

⚠️ You might need to allow more memory to you podman machine.
```
podman machine stop
podman machine set --cpus 2 --memory 4 096
podman machine start
```

**Install SonarScanner CLI (Mac OS)**\
`brew install sonar-scanner`

**Install SonarScanner CLI (Other)**\
https://docs.sonarsource.com/sonarqube-server/10.8/analyzing-source-code/scanners/sonarscanner/

## First start
By default, sonarqube run with the account
```
username: admin
password: admin
```

When connecting with admin, you will be asked to update your password. We recommend to use:
```
username: admin
password: Ig2i-CI-son@rQube
```

In the top right corner, click your user icon and go to
"My Account" -> "Security".

Generate a new user token named `sonar_scan`.\
Create a `.env` file with the line:
```
SONAR_TOKEN=<your-token>
``` 