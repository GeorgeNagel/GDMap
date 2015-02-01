Exec {
  path => [ "/bin/", "/sbin/", "/usr/bin/", "/usr/local/bin/" ]
}

exec {
  "apt-get update": command => "/usr/bin/apt-get update",
                    user => root
}

class { 'python':
  version => 'system',
  virtualenv => true,
  pip => true,
}

class { 'mongodb::server':
  port    => 27017,
  verbose => true,
  bind_ip => ["0.0.0.0"],
}


class { 'elasticsearch':
  package_url => "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.2.deb",
  java_install => true,
}

elasticsearch::instance { 'es-01': }
