class pip {
  exec { "apt-get install python-pip":
    unless=>"which pip"
  }
  exec { "pip install virtualenv":
    require => Exec['apt-get install python-pip']
  }
}
