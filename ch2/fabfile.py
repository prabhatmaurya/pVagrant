import vagrant
from fabric.api import *

def start():
    ## Initialise
    v = vagrant.Vagrant()
    ## make sure vagrant is up
    v.up()

    env.hosts = [v.user_hostname_port()]
    env.key_filename = v.keyfile()
    env.disable_known_hosts = True # useful for when the vagrant box ip changes.
    env.hostname = v.hostname()
    # change from the default user to 'vagrant'
    env.user = 'vagrant'

def uname():
    run('uname -a')

def deploy_mysql():
    ## Install Mysql-Server
    run('sudo yum -y install mysql-server')

    ## Add iptable rules
    run('sudo iptables -I INPUT -p tcp --dport 3306 -m state --state NEW,ESTABLISHED -j ACCEPT')
    run('sudo iptables -I OUTPUT -p tcp --sport 3306 -m state --state ESTABLISHED -j ACCEPT')
    run('sudo service iptables save')

    ##Start Application
    run('sudo /sbin/service mysqld start')

    ## Launch at reboot
    run('sudo chkconfig mysqld on')

    ## Set Mysql password
    mysqlPassword = 'fabricDeploy'

    ## Check condietion for for 2nd attempt of script, in case password already reset in first attempt
    result = run("mysql -u root -p%s <<< 'show databases'" % mysqlPassword,warn_only=True)
    if result.failed:
        run("/usr/bin/mysqladmin -u root password '%s'" % mysqlPassword)
        run("/usr/bin/mysqladmin -u root --password='%s' -h %s password '%s'" % (mysqlPassword,env.hostname,mysqlPassword))

def deploy_apache():
    ## Install Apache
    run("sudo yum -y install httpd  mod_ssl")

    ## Add IPtable rules
    run("sudo iptables -I INPUT -p tcp --dport 80 -j ACCEPT")
    run(" sudo service iptables save")

    ## Start Apache
    run("sudo service httpd start")

    ## Launch at boot
    run(" sudo /sbin/chkconfig httpd on")

def deploy_php():
    ## Insatll PHP
    run("sudo yum -y install php php-devel php-mysql")
    run("sudo service httpd restart")

def deploy_project():
    ##Deploy Dummy Project
    run("echo '<?php phpinfo(); ?>' | sudo tee /var/www/html/index.php")

def deploy_lamp_stack():
    execute(deploy_mysql)
    execute(deploy_apache)
    execute(deploy_php)
