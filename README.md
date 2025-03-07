# CI/CD Pipeline for a Machine Learning Project - MLOps Assignment - 1 


## Team Members
- Member 1: Malaika Zafar (21I-1110)
- Member 2: M. Abdullah (21I-1215)


## Overview
This application aims to predict the demand-supply gap for ride requests in a city based on historical data. Uber divides a city into multiple non-overlapping square regions and a day into 144 time slots. 
For each region and time slot, the demand and supply are recorded. The demand-supply gap is calculated as the difference between these values. To accurately predict this gap, the application utilizes linear regression model trained on past data.
This repository follows a structured **Git workflow** with automated **code quality checks, feature testing, and deployment** using GitHub Actions, Jenkins, and Docker. 
##  Repository Setup & Branching Strategy
We implemented a **branching strategy** that includes:

- **Master Branch**: When a feature has been developed and tested thoroughly, it is pushed on to the master branch. This branch has the code for production.
- **Test Branch**: Every feature is validated on the test branch before it is moved to production. 
- **Dev Branch**: New features that have been developed are added to the dev branch.
- **Feature Branches**: Each new feature is developed or tested in a separate branch before merging with the respective branch.

- **Screenshot:**
![image](https://github.com/user-attachments/assets/d8b33d32-39ed-49ed-98a6-894cabf4e5ba)


### Pull Requests & Merging Process
1. **Feature Branch** → Pull Request (PR) to **Dev Branch** (This triggers the code quality check workflow).
2. Merge feature into **Dev Branch**.
3. **Dev Branch** → PR to **Test Branch** (This triggers the feature testing workflow).
4. Merge Dev into **Test Branch**.
5. Create a **new test branch** from the **Test Branch** for isolated feature testing.
6. After testing, PR from the feature testing branch to the **Test Branch**.
7. **Test Branch** → PR to **Master Branch** for final deployment.

- **Screenshot:**
![image](https://github.com/user-attachments/assets/741bda51-8a90-4101-94c9-8cfabf2a945b)



---

## Code Quality Check (GitHub Actions & Flake8)
We implemented **GitHub Actions** to enforce **code quality checks** using **Flake8**. Any Pull Request to the **Dev Branch** must pass the Flake8 check before merging. This ensures clean and maintainable code.
- **Screenshot:**

![image](https://github.com/user-attachments/assets/bad4545f-3252-47d1-8496-5a2db0f58d85)   ![image](https://github.com/user-attachments/assets/85d17c30-3be2-44b6-9acd-13ff40ebdbfb)

- This workflow is triggered whenever a user creates a pull request to the dev branch. Merge is not possible unless all the checks in this workflow are cleared.
- Screenshot:

![image](https://github.com/user-attachments/assets/458c5d6c-8a3b-4be2-836d-6293b7f1e461)


---

## Feature Testing (GitHub Actions && PyTest)
1. When a feature is completed in the **Dev Branch**, a **pull request** is submitted to the **Test Branch**.
2. This triggers an **automated testing workflow** using GitHub Actions.
3. Unit tests validate the feature before merging into the Test Branch.
   
- **Screenshot:**

![image](https://github.com/user-attachments/assets/f60bfecf-8973-474c-bb02-487d16d423d5) ![image](https://github.com/user-attachments/assets/66867d18-b24e-470b-b8be-6a4da5c36025)


---

## Deployment with Jenkins & Docker
After successful testing:
1. Merging into the **Master Branch** triggers a **Jenkins job**.
   
   1.1. We expose Jenkins using Ngrok and then add that link to Github webhooks. The webhook is set up so that it sends a call to jenkins every time a branch merges with master. 
![Screenshot 2025-03-06 100318](https://github.com/user-attachments/assets/62a38a8e-801c-4b9a-b33d-377b7c35215b)
![Screenshot 2025-03-06 100325](https://github.com/user-attachments/assets/19e99009-13ce-4f4a-9e2c-ecabbc2b9db5)



3. The Jenkins job:
   - **Containerizes the application** using **Docker**.

   - **Pushes the Docker image** to **Docker Hub**.
   - - **Screenshot:**
     ![Screenshot 2025-03-07 041144](https://github.com/user-attachments/assets/66f9e331-1a01-4a6e-abeb-023d7aabdf3f) ![Screenshot 2025-03-06 100409](https://github.com/user-attachments/assets/25e169e1-823c-4428-b54a-baace2b34ea0)


---

## Admin Notification
Once the deployment is successful **an email notification** is sent to the admin via Jenkins to confirm the **successful deployment**.
We used the following steps to set up the email notifications in jenkins: 
   - Installed the Email notification plugin on jenkins.
   - Configured the plugin to send emails to the target email (in this case masterminder12378@gmail.com)
   - Added the email text body in the post step of the jenkins job. This means that the email will be sent after all the stages in the jenkins job have been completed.
   
![image](https://github.com/user-attachments/assets/3f05f7e1-9557-42b5-b227-1d9ecf637c7c)





