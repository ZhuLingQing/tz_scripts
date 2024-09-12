import paramiko
import os

def download_file_from_remote(remote_host, remote_port, username, password, remote_file_path, local_path):
    # 获取脚本当前目录
    local_file_path = os.path.join(local_path, os.path.basename(remote_file_path))
    
    try:
        # 创建 SSH 客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接到 remote 主机
        ssh.connect(remote_host, port=remote_port, username=username, password=password)
        
        # 创建 SCP 客户端
        scp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        
        # 下载文件
        scp.get(remote_file_path, local_file_path)
        
        # 关闭连接
        scp.close()
        ssh.close()
    
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    remote_host = '10.102.16.109'
    remote_port = 22  # SSH 端口
    username = 'root'
    password = 'test1234'
    remote_file_path = '/home/admin001/pace2_bringup/aurora_diag/test_log/aurora-diag-2024.08.03-23.07.22/aurora-diag.log'

    download_file_from_remote(remote_host, remote_port, username, password, remote_file_path)
