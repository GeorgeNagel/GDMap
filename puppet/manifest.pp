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

