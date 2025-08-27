## EC2 미작동 디버깅 - EBS 볼륨 이슈 확인

- 밥먹뽀먹 프로젝트 진행중, 서버 만든 직후에는 테스트 잘 되던 EC2가 다음날 갑자기 외부접속/ssh접속이 안 됨

- AWS cloudshell에서 인스턴스 상태 확인

  `aws ec2 describe-instance-status --instance-ids <ec-2 id> --include-all-instances`

```shell
{
    "InstanceStatuses": [
        {
            "AvailabilityZone": "ap-northeast-2c",
            "AvailabilityZoneId": "apne2-az3",
            "Operator": {
                "Managed": false
            },
            "InstanceId": "i-xx",
            "InstanceState": {
                "Code": 16,
                "Name": "running"
            },
            "InstanceStatus": {
                "Details": [
                    {
                        "ImpairedSince": "2025-08-26T14:16:00+00:00",
                        "Name": "reachability",
                        "Status": "failed"
                    }
                ],
                "Status": "impaired"
            },
            "SystemStatus": {
                "Details": [
                    {
                        "Name": "reachability",
                        "Status": "passed"
                    }
                ],
                "Status": "ok"
            }
        }
    ]
}
```

##### InstanceStatus -> reachability failed/impaired -> OS 문제 확인



- soft reboot

  - OS 재부팅 명령 
  - 물리 호스트, EBS 등 상태가 유지되며 Public IP도 바뀌지 않음

  ```shell
  aws ec2 reboot-instances --instance-ids <i-xx> && sleep 90 && aws ec2 describe-instance-status --instance-ids <i-xx> --include-all-instances --query 'InstanceStatuses[].{System:SystemStatus.Status,Instance:InstanceStatus.Status}'
  ```

##### soft reboot 해봤는데 상태 같음



- hard reboot

  - 인스턴스를 완전히 종료(전원 off) → 다시 기동
  - Elastic IP 붙여놓지 않으면 IP주소 변경됨
  - EBS는 그대로 붙음

  ```shell
  aws ec2 stop-instances --instance-ids <i-xx> && aws ec2 wait instance-stopped --instance-ids <i-xx> && aws ec2 start-instances --instance-ids <i-xx> && aws ec2 wait instance-running --instance-ids <i-xx>
  ```

##### 이것도 잘 안 되고.. 생각해보니까 EBS 볼륨을 너무 작게 잡아놓은 것 같음

##### 8GB -> 20GB로 볼륨 키우고 나서 테스트하니까 ssh접속 성공

##### `df -h`로 스토리지 상태 확인해보니까..

```shell

Filesystem      Size  Used Avail Use% Mounted on
/dev/root       6.8G  4.5G  2.3G  67% /
tmpfs           479M     0  479M   0% /dev/shm
tmpfs           192M  1.1M  191M   1% /run
tmpfs           5.0M     0  5.0M   0% /run/lock
/dev/xvda16     881M   87M  733M  11% /boot
/dev/xvda15     105M  6.2M   99M   6% /boot/efi
overlay         6.8G  4.5G  2.3G  67% /var/lib/docker/overlay2/3d3818a4fa2d6a97cb1101297b671b2656fa44785052d5658811eb54d7c116d1/merged
overlay         6.8G  4.5G  2.3G  67% /var/lib/docker/overlay2/aee74910d4c6a04dba4fc9bd86c031dc8da0e020d1d7624cbe35bbe0a2de2a0c/merged
tmpfs            96M   12K   96M   1% /run/user/1000

```

##### 8GB로 어림도 없음

- `growpart`로 파티션 확장

  `sudo growpart /dev/xvda 1`

- 파일 시스템 확장

  `sudo resize2fs /dev/xvda1`

##### 이후 `df -h` 다시 찍어보니까 dev/root가 19GB로 늘어나있음. 용량 확보 완료

##### 보통은 db는 ebs도 따로 분리해놓고, 공간도 좀 넉넉하게 주고, 주기적인 로그 청소 등 관리를 해줘야 하긴 하는데

##### 지금은 프로젝트 진행이 급해서 일단넘어감