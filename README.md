# Stock-portfolio-Calculator
Generates personalized stock portfolios and asset allocation for different investment strategies. 

Dependencies 
------------
1. Install python 2.7 on your computer. 
2. Make sure the following modules are installed before running the project.
	Flask
	flaskext.mysql 
	yahoo_finance 
3. Run the following commands in a Mac or Linux envirnment to install the modules 
	pip install flask
	pip install flaskext_mysql
	pip install yahoo_finance
4. Make sure MySQL database server is installed and a database schema named portfolio is created. 
5. Run the SQL scripts to generate necessary tables and insert statements.
6. For windows/mac, flask can be used by creating a virtual envirnment using the following command before installing flask. 
	python3 -m venv f_form

	source f_form/bin/activate

Steps for running
------------------

1. Copy the project folder StockPortfolioSuggestion.zip to a location and unzip. 
2. Make sure the required modules are installed. 
3. Open your terminal and run app.py using the following command
	python app.py
4. Go to your browser and enter the URL http://0.0.0.0:8000/ to run the project. 
5. Select an investment strategy and enter an amount to see your portfolio suggestion. 
