resource "aws_efs_file_system" "main" {
  creation_token = "${var.project_name}-efs"
  encrypted      = true

  tags = {
    Name = "${var.project_name}-efs"
  }
}

resource "aws_efs_mount_target" "public_1" {
  file_system_id  = aws_efs_file_system.main.id
  subnet_id       = aws_subnet.public_1.id
  security_groups = [aws_security_group.efs.id]
}

resource "aws_efs_mount_target" "public_2" {
  file_system_id  = aws_efs_file_system.main.id
  subnet_id       = aws_subnet.public_2.id
  security_groups = [aws_security_group.efs.id]
}
