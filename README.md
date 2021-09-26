# Octo-Tweet

## Modifiers for Quaterback (c# program):

`-a` or `--all`
Get all the history useful when deploying the program for the first time as subsequent calls require the database to hold some data within it.

`-c` or `--chart-tracker-fill`
Fills the chart tracker with data so the python program is able to start generating charts from the very beguining

## Modifiers for Striker (python program):

Probably best to use `-h` for help

- `charts` subsection:

This is followed by three fariables `datetime_from`, `datetime_to` and `charts`. Datetimes must be given in ISO format, calling this function will force the creation of the charts for the specified time period.

- `generate` subsection:

`-t` or `--tweet`
Default false, can set to true to tweet the charts generated

`-l` or `--lazy`
Skips generating charts and tweeting (ideal for a new environment with no previous charts generated)

`-f` or `--folders`
Makes sure that the folders the program need to run are in place, if they are not found they will be created, this is intended as the first command run in a new environment as it would be wastefull to constantly check every time the program is run.

## Other notes:

The charts added are Daily, Weekly, Monthly, Quaterly and Yearly (planning on adding a Rolling_Yearly chart in the future), all of the charts take in data from their selective time periods but both the Quaterly and Yearly chart take in extra data from both ends in order to produce a better looking chart once the rolling average is applied.

## Deployment instructions

Have a computer running linux, either personal or a cloud virtual compute instance.

SSH into it

`ssh -i ".ssh/personal-ec2-key.pem" ubuntu@ec2-18-132-1-123.eu-west-2.compute.amazonaws.com`

Update packages

```
sudo apt update
sudo apt upgrade
```

Install MySql

```
cd /tmp
curl -OL https://dev.mysql.com/get/mysql-apt-config_0.8.17-1_all.deb
```

Check checksum

```
md5sum mysql-apt-config_0.8.17-1_all.deb
```

```
sudo dpkg -i mysql-apt-config*
```


```
sudo apt update
rm mysql-apt-config*
sudo apt install mysql-server

sudo apt install mysql-server
```

```
mysql_secure_installation

```

Install .net core

Change appsettings and mysql user passwords

Run python database builder script
Log in to mysql and run the output from said script
> Look into being able to just deploy it from running the python program


> All of the following settup could be automated with a shell script

publish c# app
```
dotnet publish ./Quarterback/Quarterback.csproj -c Release -o ./publish
```

run app with -a followed with -c


use the virtual environmetn
pip3 install -r requirements.txt

make sure to make shell script executable with 
```
chmod +x filename
```

Configure crontab
```
crontab -e

0 6 * * * /home/ubuntu/Octo-Tweet/Ace.sh >> /home/ubuntu/Octo-Tweet/Ace.log
```