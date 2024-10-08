# Real-Time Research Data Visualization Dashboard (RTRDVD)


**Implementation Manual for Linux (Ubuntu)**

The current dashboard is designed by using Python, Flask and Plotly and tested on Ubuntu 22.04 with an Apache web server. 
It can be installed on other operating systems also with modifications in Web servers. 
The Data Visualization dashboard is very light, and it can be installed on any existing servers running applications like Koha ILMS. 
So, it does not require many resources or separate systems for testing and implementation. 
The current application uses OpenAlex database for fetching the research data of any institutes. 

Installation of Apache2 (if it is not there and already running some application like Koha ILMS)

1.	Update your Ubuntu 22.04 system with the following commands:

```
sudo apt update
```
```
sudo apt upgrade
```

2.	Install the software.
```
sudo apt install apache2
```
Press “Y” and then “Enter” when prompted for confirmation. Download and install Apache Web Server on your system.

3.	Start and activate the Apache service
The Apache service starts automatically as soon as the installation has been completed successfully. Use the following command to ensure that it is loaded automatically at every system startup:
```
sudo systemctl enable apache2
```
Start the Apache service with the following command:
```
sudo systemctl start apache2
```

4.	Check the installation.
Open your web browser and enter the IP address of your Ubuntu 22.04 server in the address bar. You should see the default Apache start page, which confirms that the Apache Web Server was successfully installed.

**Create Virtual Environment**

Creating a virtual environment on the same machine where Apache is installed is straightforward. Here's how you can create a virtual environment:

1.	Install Python3-pip: Execute the following command to Install the python3-pip if it is not installed on your Server.

```
apt install python3-pip
```

2.	Python Project Files: Transfer all your Python project files to “opt” folder of Ubuntu, for example, if your project folder name is “datavisuopenalex” then you can move it to any folder with the following command:

```
cp -r /home/koha/datavisuopenalex /opt
```
3.	Navigate to Your Project Directory: First, navigate to the directory where you want to create the virtual environment. This should be the directory where your Python project files are located. (example: /opt/datavisuopenalex), to reach your project directory execute the following command:

```
cd /opt/datavisuopenalex/
```
4.	Install “virtualenv” (if not already installed): If “virtualenv” is not already installed on your system, you can install it using pip, Python's package manager:
```
sudo apt update
```
```
sudo apt install python3-venv
```

5.	Create the Virtual Environment: Use the “python3 -m venv” command to create a new virtual environment. You can specify the name of the directory where you want to create the virtual environment. Conventionally, it's named env:

```
python3 -m venv env
```
This command will create a new directory named “env” in your current directory (/opt/datavisuopenalex/env), which will contain the virtual environment.

6.	Activate the Virtual Environment: Once the virtual environment is created, you need to activate it. Activating the virtual environment ensures that any Python commands you run will use the Python interpreter and packages installed within the virtual environment:

```
source env/bin/activate
```
After activation, you should see (env) in your terminal prompt, indicating that the virtual environment is active. “(env) root@koha-OptiPlex-9010:/opt/datavisuopenalex#”

7.	Install Dependencies: With the virtual environment activated, you can now install your project dependencies using pip. Typically, you would have a requirements.txt file containing a list of dependencies. You can install them using:

```
pip install plotly
```
```
pip install flask
```
```
pip install requests
```
```
pip install openpyxl
```
```
pip install pandas
```

OR 

You can install all above with the following command

```
pip install -r requirements.txt
```


8.	Deactivate the Virtual Environment: Once you're done working on your project, you can deactivate the virtual environment with the command:

```
deactivate
```

By following the above steps, you can create a virtual environment on the same machine where Apache is installed. This virtual environment will isolate your project's dependencies from other Python projects and system-wide installations, ensuring that your project runs smoothly alongside Koha ILMS.

**Configure the Dashboard on apache server (You may configure alongside Koha or other applications already running)**

1.	Enable mod_wsgi: Apache uses modules to extend its functionality. One such module is mod_wsgi, which allows Apache to serve Python web applications. You'll need to enable mod_wsgi if it's not already enabled and install it if not available:

```
sudo apt-get install libapache2-mod-wsgi-py3
```

```
sudo a2enmod wsgi

```

2.	Configure a New Virtual Host: Create a new Apache virtual host configuration file for your Python application. This file will specify how Apache should handle requests to your application. For example, create a file named “dashboard.conf” in Apache's sites-available directory:


```
sudo nano /etc/apache2/sites-available/dashboard.conf

```
Add the following configuration to the above file:


```
<VirtualHost *:83>
    ServerName 192.168.201.108
    
    # Configuration for Python files
    WSGIDaemonProcess python_apps python-home=/opt/datavisuopenalex/env python-path=/opt/datavisuopenalex
    WSGIProcessGroup python_apps
    WSGIScriptAlias / /opt/datavisuopenalex/
    # Directory configuration for HTML files
    Alias /templates /opt/datavisuopenalex/templates
    <Directory /opt/datavisuopenalex/templates>
        Require all denied
    </Directory>
    <Directory /opt/datavisuopenalex>
        Require all granted
    </Directory>
   # Directory configuration for static files to execute on web like logo.jpg
Alias /static/ /opt/datavisuopenalex/static/
<Directory /opt/datavisuopenalex/static>
    Require all granted
</Directory>
</VirtualHost>

```
Replace yourdomain.com with your actual domain name or server IP address. Adjust /path/to/your/virtualenv and /path/to/your/project with the appropriate paths to your Python virtual environment and project directory (as you have created in previous steps and shown above).

3.	Enable the Virtual Host: Enable the virtual host you created and change the ports if changed above:


```
sudo a2ensite dashboard.conf

```
Add new port as you have added in the above virtualhost file and save it.
```
sudo nano /etc/apache2/ports.conf

```

4.	Restart Apache: After making any configuration changes, restart Apache to apply the changes:

   
```
sudo systemctl restart apache2

```

**How to access the Virtual Dashboard**

1.	Access Your Application: Once Apache is configured, you should be able to access your Python application by visiting the appropriate URL in a web browser (http://IP_address:83/dashboard.py). Apache will handle requests to your application and serve responses accordingly.
   
By configuring Apache to serve your Python application using mod_wsgi, you can run your dashboard alongside Koha ILMS or any other applications on the same server. This approach allows Apache to efficiently handle requests for both applications, ensuring they coexist harmoniously.

**Customization of Charts with affiliation ID**

If you are willing to use the same charts to visualize data on the dashboard, then little effort is needed as explained below. For visualizing another type of data and charts, separate coding is required, which may be done in line with existing codes. For every plotly chart there is one URL in the **api_urls.py** file; with careful examination, you will find a number in the URL, which is assigned by the OpenAlex database to search the documents with affiliation like other databases such as Scopus/WoS. 

For example, if you want to display the charts of IIT Bombay then you need to replace the affiliation/Institute ID from the file api_urls.py code:

Institution ID code in api_urls.py file

**Define the common ID**
institution_id = "i16292982"

Replace it with IIT Bombay code:

**Define the common ID**
institution_id = "i162827531"

After replacing automatically all charts data will be changed along with the text

Most of the data, including text, are fetched from OpenAlex, but if desired, the same can be modified through corresponding Python files HTML or within Python files.

**Customization of Charts with Spreadsheet**

The sample file demonstrates how to extract data from CSV and Excel files. It allows you to generate statistical charts from any type of data that can be visualized. This approach is particularly useful for analyzing local data that might not be available elsewhere. For optimal results, using CSV files is recommended, with each chart having a corresponding CSV file named appropriately. Python code can be adapted from existing scripts with minor modifications to handle these CSV files effectively.

**Logo and other files to execute/display on web**

You may keep your files/images like logo.jpg in "static/images" folder and replace the logo.png with your own logo.

**Home page image**
![](https://github.com/mishravk79/datavisuopenalex/blob/main/static/images/dashboard.png)



