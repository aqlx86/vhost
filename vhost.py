#!/usr/bin/python

import os
import sys
import getpass

# ip address
ip_address = '127.0.0.1'

# apache directory
apache_dir = '/etc/apache2/'

# available vhost
vhost_available = apache_dir + 'sites-available/'

# enabled vhost
vhost_enabled = apache_dir + 'sites-enabled/'

# host file
host_file = '/etc/hosts'

# virtual host template
template = """<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	ServerName {__server_name__}
	DocumentRoot {__doc_root__}
	<Directory />
		Options FollowSymLinks
		AllowOverride None
	</Directory>
	<Directory {__doc_root__}/>
		Options Indexes FollowSymLinks MultiViews
		AllowOverride All
		Require all granted
	</Directory>
	ErrorLog ${{APACHE_LOG_DIR}}/{__server_name__}-error.log
	LogLevel warn
	CustomLog ${{APACHE_LOG_DIR}}/{__server_name__}-access.log combined
</VirtualHost>"""

# check if root.
if getpass.getuser() != 'root':
	sys.exit('> abort!! you need to run this as root')

# get server name
server_name = raw_input('> server name [ex. testsite.dev] - ')

# get document root
doc_root = raw_input('> document root [ex. /vaw/www/html/] - ')

# construct conf file
conf_file = vhost_available + server_name + '.conf';

# check vhost if existing
if os.path.isfile(conf_file):
	sys.exit('> abort!! virtual host name exists.')

# check doc root
if not os.path.exists(doc_root):
	os.makedirs(doc_root)

# write to file
with open(conf_file, 'w') as n:
	# replate template variables
	n.write(template.format(**{'__server_name__': server_name, '__doc_root__': doc_root}))

# create symbolic link to sites-enable directory
os.symlink(vhost_available + server_name, vhost_enabled + server_name)

# append to hosts file
with open(host_file, 'a') as h:
	h.write("%s %s \n" % (ip_address, server_name))

# reload apache service
#print '> restarting'

print '> created conf file: ' + conf_file
print '> restart apache with: service apache2 reload'
print '> done.'
