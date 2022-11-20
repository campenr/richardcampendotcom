job "richardcampendotcom" {
  datacenters = ["dc1"]
  type = "service"

  meta {
    run_uuid = "${uuidv4()}"
  }

  group "web" {
    count = 1

    network {
      port "http" {
        to = 4325
      }
    }

    service {
      name     = "richardcampendotcom-web"
      tags     = ["global"]
      port     = "http"
      provider = "nomad"
    }

    task "flask" {
      driver = "docker"

      config {
        image = "campenr/richardcampendotcom:12"
        force_pull = true
        auth {
            username = "campenr"
            password = "<TODO>"
        }
        ports = ["http"]
      }

      resources {
        cpu    = 500 # 500 MHz
        memory = 256 # 256MB
      }
    }
  }
}
