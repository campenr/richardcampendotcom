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

    task "flask" {
      driver = "docker"

      config {
        image = "campenr/richardcampendotcom:13"
        force_pull = true
        ports = ["http"]
      }

      resources {
        cpu = 500 # MHz
        memory = 256 # MB
      }

      service {
        name = "richardcampendotcom-web"
        port = "http"
        provider = "nomad"
        tags = [
          "traefik.enable=true",
          "traefik.http.routers.richardcampendotcom-web.rule=Host(`staging-richardcampen.com`)",
          "traefik.http.routers.richardcampendotcom-web.tls=true",
          "traefik.http.routers.richardcampendotcom-web.tls.certresolver=letsencrypt",
        ]
      }
    }
  }
}
