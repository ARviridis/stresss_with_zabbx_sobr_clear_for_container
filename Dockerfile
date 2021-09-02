FROM centos:8
MAINTAINER kod

RUN yum -y install httpd python3-mod_wsgi.x86_64 python3-devel python3-setuptools mc gcc.x86_64 python3-pip; mkdir /var/www/testapp; adduser testapp; chown -R testapp:disk /var/www/testapp; chcon -R -t httpd_sys_content_t /var/www/testapp
COPY . /var/www/testapp/
RUN cd /usr/local/bin; ln -s /usr/bin/python3 python; cd /var/www/testapp; chmod 755 /usr/sbin/httpd 

COPY testapp.conf /etc/httpd/conf.d/testapp.conf
COPY /venv/lib/  /usr/local/lib/
COPY /venv/lib64/  /usr/local/lib64/

EXPOSE 80 443

ENTRYPOINT ["/bin/bash", "/usr/sbin/apachectl", "-D", "FOREGROUND"]
