# Wave Software Development Challenge

Applicants for the Full-stack Developer role at Wave must
complete the following challenge, and submit a solution prior to the onsite
interview.

The purpose of this exercise is to create something that we can work on
together during the onsite. We do this so that you get a chance to collaborate
with Wavers during the interview in a situation where you know something better
than us (it's your code, after all!)

There isn't a hard deadline for this exercise; take as long as you need to
complete it. However, in terms of total time spent actively working on the
challenge, we ask that you not spend more than a few hours, as we value your
time and are happy to leave things open to discussion in the on-site interview.

Please use whatever programming language and framework you feel the most
comfortable with.

Feel free to email [dev.careers@waveapps.com](dev.careers@waveapps.com) if you
have any questions.

## Project Description

Imagine that this is the early days of Wave's history, and that we are prototyping a new payroll system API. A front end (that hasn't been developed yet, but will likely be a single page application) is going to use our API to achieve two goals:

1. Upload a CSV file containing data on the number of hours worked per day per employee
1. Retrieve a report detailing how much each employee should be paid in each _pay period_

All employees are paid by the hour (there are no salaried employees.) Employees belong to one of two _job groups_ which determine their wages; job group A is paid $20/hr, and job group B is paid $30/hr. Each employee is identified by a string called an "employee id" that is globally unique in our system.

Hours are tracked per employee, per day in comma-separated value files (CSV).
Each individual CSV file is known as a "time report", and will contain:

1. A header, denoting the columns in the sheet (`date`, `hours worked`,
   `employee id`, `job group`)
1. 0 or more data rows

In addition, the file name should be of the format `time-report-x.csv`,
where `x` is the ID of the time report represented as an integer. For example, `time-report-42.csv` would represent a report with an ID of `42`.

You can assume that:

1. Columns will always be in that order.
1. There will always be data in each column and the number of hours worked will always be greater than 0.
1. There will always be a well-formed header line.
1. There will always be a well-formed file name.

A sample input file named `time-report-42.csv` is included in this repo.

### What your API must do:

We've agreed to build an API with the following endpoints to serve HTTP requests:

1. An endpoint for uploading a file.

   - This file will conform to the CSV specifications outlined in the previous section.
   - Upon upload, the timekeeping information within the file must be stored to a database for archival purposes.
   - If an attempt is made to upload a file with the same report ID as a previously uploaded file, this upload should fail with an error message indicating that this is not allowed.

2. An endpoint for retrieving a payroll report structured in the following way:

   _NOTE:_ It is not the responsibility of the API to return HTML, as we will delegate the visual layout and redering to the front end. The expectation is that this API will only return JSON data.

   - Return a JSON object `payrollReport`.
   - `payrollReport` will have a single field, `employeeReports`, containing a list of objects with fields `employeeId`, `payPeriod`, and `amountPaid`.
   - The `payPeriod` field is an object containing a date interval that is roughly biweekly. Each month has two pay periods; the _first half_ is from the 1st to the 15th inclusive, and the _second half_ is from the 16th to the end of the month, inclusive. `payPeriod` will have two fields to represent this interval: `startDate` and `endDate`.
   - Each employee should have a single object in `employeeReports` for each pay period that they have recorded hours worked. The `amountPaid` field should contain the sum of the hours worked in that pay period multiplied by the hourly rate for their job group.
   - If an employee was not paid in a specific pay period, there should not be an object in `employeeReports` for that employee + pay period combination.
   - The report should be sorted in some sensical order (e.g. sorted by employee id and then pay period start.)
   - The report should be based on all _of the data_ across _all of the uploaded time reports_, for all time.

As an example, given the upload of a sample file with the following data:

   | date       | hours worked | employee id | job group |
   | ---------- | ------------ | ----------- | --------- |
   | 4/1/2023   | 10           | 1           | A         |
   | 14/1/2023  | 5            | 1           | A         |
   | 20/1/2023  | 3            | 2           | B         |
   | 20/1/2023  | 4            | 1           | A         |

A request to the report endpoint should return the following JSON response:

   ```json
   {
     "payrollReport": {
       "employeeReports": [
         {
           "employeeId": "1",
           "payPeriod": {
             "startDate": "2023-01-01",
             "endDate": "2023-01-15"
           },
           "amountPaid": "$300.00"
         },
         {
           "employeeId": "1",
           "payPeriod": {
             "startDate": "2023-01-16",
             "endDate": "2023-01-31"
           },
           "amountPaid": "$80.00"
         },
         {
           "employeeId": "2",
           "payPeriod": {
             "startDate": "2023-01-16",
             "endDate": "2023-01-31"
           },
           "amountPaid": "$90.00"
         }
       ]
     }
   }
   ```

We consider ourselves to be language agnostic here at Wave, so feel free to use any combination of technologies you see fit to both meet the requirements and showcase your skills. We only ask that your submission:

- Is easy to set up
- Can run on either a Linux or Mac OS X developer machine
- Does not require any non open-source software
- Includes all the source code you write for the submission, including any models used for setting up your database

### Documentation:

Please commit the following to this `README.md`:

1. Instructions on how to build/run your application
1. Answers to the following questions:
   - How did you test that your implementation was correct?
   - If this application was destined for a production environment, what would you add or change?
   - What compromises did you have to make as a result of the time constraints of this challenge?

## Submission Instructions

1. Clone the repository.
1. Complete your project as described above within your local repository.
1. Ensure everything you want to commit is committed.
1. Create a git bundle: `git bundle create your_name.bundle --all`
1. Email the bundle file to [dev.careers@waveapps.com](dev.careers@waveapps.com) and CC the recruiter you have been in contact with.

## Evaluation

Evaluation of your submission will be based on the following criteria.

1. Did you follow the instructions for submission?
1. Did you complete the steps outlined in the _Documentation_ section?
1. Were models/entities and other components easily identifiable to the
   reviewer?
1. What design decisions did you make when designing your models/entities? Are
   they explained?
1. Did you separate any concerns in your application? Why or why not?
1. Does your solution use appropriate data types for the problem as described?


### Nnaemeka Eneh - se-challenge-payroll

#### Instructions on how to build/run your application

In order to run the application, kindly follow the steps below:
1. run `docker build .` to build the image.
2. run `docker-compose run web python manage.py migrate` to setup all the migrations.
3. run `docker-compose up` to run the container.

There is only one valid url path which is :
`http://127.0.0.1:3000/payroll-report/`

- Once you load the page, upload a valid csv file which meets the criteria as mention in the project description.
- If the file loads successfully, a successful message will displayed, however if the file is not valid an error message will be displayed.
- Once you successfully upload a file, on refresh a JSON object `payrollReport` is returned and also printed in the terminal.


#### How did you test that your implementation was correct?
1.  I wrote some tests which addresses the following below:
    - Test to check the url path is link to the view class.
    - Test for a FAILED request if an invald file is uploaded.
    - Test for a PASSED request if a valid file is uploaded.
    - Test can be found in `reports/tests/test_report`.

To check if my test passed kindly run `docker-compose run web python manage.py test reports`

2. I manually double checked each endpoint to ensure that result produced is what I expected

#### If this application was destined for a production environment, what would you add or change?

- I will use a better framework such as `Material UI React Framework` for the frontend. I will build and design it such way a splendid way it will quite presentable, easy to use, navigate and adjust depending on the user screen size.
- After uploading a file, i would add a better message display which only pops up and disappears after a couple of seconds with its either a success or an error message.
- I will ensure there is a better flow after submitting a file. Either to redirect to another page or re-render the page showing the actual payrollReport result.
- I will present the payroll Report with a table, graph or chart and make the information have more meaning to the user than just the raw data.
- I will use the User model, work on a couple of user functions and create a login page so that only users who have access can upload files or view report.
- I will add permission, login access and authentication so that only users with access can reach the endpoint.
- Also write more test to ensure the system is thoroughly tested.
- Ensure that certain information especially in the setting.py are configured to be restricted.


#### What compromises did you have to make as a result of the time constraints of this challenge?
- Not a beautiful webpage - little CSS done on the display.
- Ugly message display - when a file is uploaded or rejected.
- Poor flow after uploading csv file.
- No login access platform which means anyone can upload file or view the report.
- I could improve ORM querying of data
