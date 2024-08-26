### Nnaemeka Eneh - se-challenge-payroll

#### Instructions on how to build/run your application

In order to run the application, kindly follow the steps below:
1. run `docker compose up --build` to build the image
2. run `docker-compose run web python manage.py migrate` to setup all the migrations
3. run `docker-compose up` to run the container

There is only one valid url path which is :
`put the url path in here`

    - Once you to load the page, upload a valid csv file which meets the criteria as mention project description
    - If the file loads successfully, a successfully message will display, however if the file is not valid and error message will be displayed.
    Once you successfully upload a file, on refresh a JSON object `payrollReport` is return and also printed on the terminal.


#### How did you test that your implementation was correct?
    1.  I wrote some tests which addresses the following below:
        - Test to check the url path is link to the view class
        - Test for a FAIL request if an invald file is uploaded
        - Test for a pass request if a valid file is uploaded

    To check if my test passed kindly run `python3 manage.py test reports`

    2. I manually double checked each endpoint to ensure that result is what I expected

#### If this application was destined for a production environment, what would you add or change?

    - I used a better framework such as Material UI React Framework work for the frontend. I will build and design it such way a splendid way it will easy to use, navigate and adjust depending on the user screen size.
    - Upon uploading a file, i would add a better message display which pops up when submitted it a success message or an error
    - I will ensure there is a better flow after submitting a file. Either to redirect to another page or re-render the page showing the actual payrollReport
    - I will the present the payrollReport with table or graph chart and makes the information have more meaning to the user that just a json data
    - Use User model and create a login page to have access to upload or view report
    - I will add permission, login access and authentication so that it will not be anybody that have access to upload data to our databases or view the `payrollReport` data
    - Also write more test to ensure the system is tested properly
    - Ensure that certain information especially in the setting.py are configured to be restricted.


#### What compromises did you have to make as a result of the time constraints of this challenge?
    - Not a beautiful webpage - little CSS done on the display
    - Ugly message display - when a file is uploaded or rejected
    - No login access platform which means anyone can upload file or view the report
