from vboxmanage_wrapper import parse_vbox_manage_list_hdd

def test_parse_vboxmanage_list_hdd():
    # VBoxManage list hdds

    output = """
UUID:           49ab2c4d-9774-45ff-8501-1cb49d320b05
Parent UUID:    base
State:          inaccessible
Type:           normal (base)
Location:       /home/gitlab-runner/VirtualBox VMs/baremetal-pxe-environment_pxe_server_1522934644737_41281/ubuntu-xenial-16.04-cloudimg.vmdk
Storage format: VMDK
Capacity:       10240 MBytes
Encryption:     disabled

UUID:           4d20d546-fa69-41a9-b61e-e42648069bfc
Parent UUID:    base
State:          locked write
Type:           normal (base)
Location:       /home/gitlab-runner/VirtualBox VMs/baremetal-pxe-environment_pxe_server_1522934644737_41281/ubuntu-xenial-16.04-cloudimg-configdrive.vmdk
Storage format: VMDK
Capacity:       10 MBytes
Encryption:     disabled

UUID:           9114677b-33ee-4b18-9a3a-9f8d014877f4
Parent UUID:    base
State:          locked write
Type:           normal (base)
Location:       /home/gitlab-runner/VirtualBox VMs/baremetal-pxe-environment_pxe_server_1522934644737_41281/ubuntu-xenial-16.04-cloudimg.vdi
Storage format: VDI
Capacity:       61440 MBytes
Encryption:     disabled

UUID:           8ba1314e-0c19-4efc-9215-28f4ef7fbd7c
Parent UUID:    base
State:          inaccessible
Type:           normal (base)
Location:       /home/gitlab-runner/VirtualBox VMs/baremetal-pxe-environment_pxe_server_1522934998078_64370/ubuntu-xenial-16.04-cloudimg.vmdk
Storage format: VMDK
Capacity:       10240 MBytes
Encryption:     disabled

UUID:           8e340f0d-318a-4451-8040-0eaa136b843e
Parent UUID:    base
State:          inaccessible
Type:           normal (base)
Location:       /home/gitlab-runner/builds/0de7ef7d/4/baremetal/baremetal-pxe-environment/packer/debian-raid1/packer_disk2.vmdk
Storage format: VMDK
Capacity:       2048 MBytes
Encryption:     disabled

UUID:           39afc078-c24a-4619-ba17-0958f29cb50e
Parent UUID:    8e340f0d-318a-4451-8040-0eaa136b843e
State:          inaccessible
Type:           normal (differencing)
Location:       /home/gitlab-runner/VirtualBox VMs/packer-build-baremetal-debian-9.3.0-amd64-raid1/Snapshots/{39afc078-c24a-4619-ba17-0958f29cb50e}.vmdk
Storage format: VMDK
Capacity:       2048 MBytes
Encryption:     disabled
"""
    result = parse_vbox_manage_list_hdd(output)

    assert result[0]['uuid'] == '49ab2c4d-9774-45ff-8501-1cb49d320b05'
    assert result[0]['state'] == 'inaccessible'
    assert result[0]['location'] == '/home/gitlab-runner/VirtualBox VMs/baremetal-pxe-environment_pxe_server_1522934644737_41281/ubuntu-xenial-16.04-cloudimg.vmdk'

    assert result[2]['uuid'] == '9114677b-33ee-4b18-9a3a-9f8d014877f4'
    assert result[2]['state'] == 'locked write'
    assert result[2]['location'] == '/home/gitlab-runner/VirtualBox VMs/baremetal-pxe-environment_pxe_server_1522934644737_41281/ubuntu-xenial-16.04-cloudimg.vdi'
