# seting up your web servers for the deployment of web_static

$config = "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    add_header X-Served-By ${hostname};

    root   /var/www/html;
    index  index.html index.htm;
    location / {
        try_files ${uri} ${uri}/ =404; 
    }

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://linktr.ee/firdaus_h_salim/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}"

exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
}

-> package { 'nginx':
ensure => 'installed',
}

-> file { '/data':
  ensure  => 'directory'
}

-> file { '/data/web_static':
  ensure => 'directory'
}

-> file { '/data/web_static/releases':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory'
}

-> file { '/data/web_static/shared':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => 'Hello this is Fake!!'
}

-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test'
}

-> exec {'owner':
command  => 'chown -hR ubuntu:ubuntu /data',
provider => shell,
before   => Exec['conf_nginx'],
}

file { '/var/www':
  ensure => 'directory'
}

-> file { '/var/www/html':
  ensure => 'directory'
}

-> file { '/var/www/html/index.html':
  ensure  => 'present',
  content => 'Hello World!'
}

-> file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n"
}

-> file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $config
}

-> exec { 'restart_nginx':
provider => shell,
command  => 'sudo service nginx restart',
}
