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