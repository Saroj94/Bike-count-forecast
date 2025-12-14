## Deployment in the google cloud
1. Create a project in the google console (Project Name: <BikeRentalForecast>)
2. Open the <Cloud Run>, simultanously create a docker file in the working directory 
3. then find the <deploy container> 
4. option in the <Cloud Run service> section.

3. Select the Continously deploy from repo
    1. Cloud Build/Setup Cloud build
    2. Source Repository for access projects but first Authenticate with github repository by installing the Cloud Build
    3. Build Configuration 
        1. branch name: main
        2. Build Type : Dockerfile
        3. Create

# Alternative
## GCP deployment Via GitHub action
1. Enable artifact registry API
    1. Name of the repository
    2. Location and hit create button
2. Create .github/workflows/build.yml folder and file in the working directory with the help of these commands
    1. mkdir -p .github/workflows
    2. touch .github/workflows/build.yaml
3. github action secrets variables
    1. variable
    2. IAM service account id with arbitary name for repository email
    3. copy the arbitary email, go to artifact registry and repository
    4. inside repository, checked the box of repo and click on info panel to add the principals and role of it
    5. now we have permission we need to access the IAM service account , go to 