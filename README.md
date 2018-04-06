# Virtualbox VBoxManage helper

Install with:

```
$ pip install https://github.com/harobed/vboxmanage_plus/archive/master.zip
```

Execute this command to list all Virtualbox orphaned hdds:

```
$ vboxmanage_plus list orphaned hdds
49ab2c4d-9774-45ff-8501-1cb49d320b05 - /home/gitlab-runner/VirtualBox VMs/server_1522934644737_41281/ubuntu-xenial-16.04-cloudimg.vmdk
8ba1314e-0c19-4efc-9215-28f4ef7fbd7c - /home/gitlab-runner/VirtualBox VMs/server_1522934998078_64370/ubuntu-xenial-16.04-cloudimg.vmdk
39afc078-c24a-4619-ba17-0958f29cb50e - /home/gitlab-runner/VirtualBox VMs/packer-debian-9.3.0-amd64-raid1/Snapshots/{39afc078-c24a-4619-ba17-0958f29cb50e}.vmdk
```


Execute this command to clean all Virtualbox orphaned hdds:

```
$ vboxmanage_plus remove orphaned hdds
vboxmanage_plus remove orphaned hdds
Remove 49ab2c4d-9774-45ff-8501-1cb49d320b05 - /home/gitlab-runner/VirtualBox VMs/server_1522934644737_41281/ubuntu-xenial-16.04-cloudimg.vmdk
Remove medium 49ab2c4d-9774-45ff-8501-1cb49d320b05
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
Remove 8ba1314e-0c19-4efc-9215-28f4ef7fbd7c - /home/gitlab-runner/VirtualBox VMs/server_1522934998078_64370/ubuntu-xenial-16.04-cloudimg.vmdk
Remove medium 8ba1314e-0c19-4efc-9215-28f4ef7fbd7c
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
```


## Execute tests

```
$ pip install pytest
```

```
$ pytest
```
