provider "aws" {}


resource "aws_instance" "deploy-flask" {
  ami                         = "ami-408c7f28"
  instance_type               = "t3a.micro"
  key_name                    = "key-deploy-flask"
  subnet_id                   = "subnet-0073b2cf6844fa8b2"
  vpc_security_group_ids      = ["sg-5ea45241", ]

  timeouts {
    create = "10m"
  }

  provisioner "file" {
    source      = "../"
    destination = "."
    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = "${file("key-deploy-flask.pem")}"
      host        = "${self.public_dns}"
      timeout       = "5m"
    }
  }

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = "${file("key-deploy-flask.pem")}"
      host        = "${self.public_dns}"
      timeout       = "5m"
    }
    inline = [
      "pip install flask",
      "python main.py"
    ]
  }
}