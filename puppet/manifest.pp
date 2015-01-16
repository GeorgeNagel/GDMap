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

# See https://github.com/elasticsearch/puppet-elasticsearch/issues/39
class our_elasticsearch($version='1.4.2') {

  # We couldn't simply rely on the 'elasticsearch' module from:
  # https://github.com/elasticsearch/puppet-elasticsearch because it requires your desired
  # version to be in your package manager, but ours isn't.

  exec { "download_elasticsearch":
    command => "/usr/bin/wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-${version}.deb -O /tmp/elasticsearch-${version}.deb",
    creates => "/tmp/elasticsearch-${version}.deb"
  }

  package { 'openjdk-7-jre': ensure => present }

  class { 'elasticsearch':
    package_url => "file:/tmp/elasticsearch-${version}.deb",
    require     => [ Package['openjdk-7-jre'], Exec['download_elasticsearch'] ],
    autoupgrade => true,
  }
}

include our_elasticsearch
