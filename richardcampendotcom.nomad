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
      name = "richardcampendotcom-web"
      port = "http"
      provider = "nomad"
      tags = [
        "traefik.enable=true",
        "traefik.http.routers.http.rule=Host(`richardcampen.com`)",
        "traefik.http.routers.http.tls=true",
        "traefik.http.routers.http.tls.certresolver=letsencrypt",
      ]
    }

    task "flask" {
      driver = "docker"

      config {
        image = "campenr/richardcampendotcom:latest"
        force_pull = true
        auth = {
          username = "campenr"
          password = "<todo>"
        }
        ports = ["http"]
      }

      resources {
        cpu = 50 # MHz
        memory = 75 # MB
      }
    }
  }
}
