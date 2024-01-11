# seting up your web servers for the deployment of web_static

exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
  before   => Package['nginx'],
}

package { 'nginx':
ensure => 'installed',
before => Exec['add_dir_test'],
}

exec { 'add_dir_test':
command  => 'mkdir -p /data/web_static/releases/test/',
provider => shell,
before   => Exec['add_dir_shared'],
}

exec { 'add_dir_shared':
command  => 'mkdir -p /data/web_static/shared/',
provider => shell,
before   => File['index'],
}

file { 'index':
path = '/data/web_static/releases/test/index.html',
ensure  => present,
content => 'Hello this is Fake!!',
before  => File['rm_symbolic']
}

file { 'rm_symbolic':
path = '/data/web_static/current',
ensure => absent,
before => Exec['create_symbolic']
}

exec {'create_symbolic':
command  => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
provider => shell,
before   => Exec['owner'],
}

exec {'owner':
command  => 'chown -hR ubuntu:ubuntu /data',
provider => shell,
before   => Exec['conf_nginx'],
}

exec {'conf_nginx':
command  => 'sed -i "38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default',
provider => shell,
before   => Exec['restart_nginx'],
}

exec { 'restart_nginx':
provider => shell,
command  => 'sudo service nginx restart',
}
