## Email Redshift query results using SES

This project is to show how you can query a Redshift table, change one of the fields from the query results to a clickable link, change the query results to HTML styles, and finally send an email to specified recipients using Amazon SES. Below steps are followed in the code to accomplish the goals.
1.	Connect to Amazon Redshift cluster using AWS credentials. Use your own credentials for this step.
2.	Run a sample query on Redshift. Change the query based on your requirements. 
3.	Define a cursor and execute the query
4.	Define column names Python DataFrame with the selected columns from the table. Note that one of the columns ("Age-of-Request") in the query was a calculated field 
5.	Create a DataFrame
6.	Convert one of the fields in the DataFrame to a clickable link using Python Lambda function
7.	Style the DataFrame into HTML
8.	Setup Email configurations with sender, recipient, aws-region information
9.	Send the emails. Please check this AWS documentation before executing the program to setup Amazon SES https://docs.aws.amazon.com/ses/latest/dg/send-an-email-using-sdk-programmatically.html 

To execute the program from your CLI, setup AWS CLI following the instructions in https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html 

Finally run the Python program from your AWS CLI.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

