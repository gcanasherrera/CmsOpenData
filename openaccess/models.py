import os
import stat
from Crypto.PublicKey import RSA

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import paramiko

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    key = models.TextField()
    username = models.CharField(max_length=20)
    extra_keys = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.username

    def setup_user(self):
        self.username = 'cms%04d' % self.user.pk
        self._generate_key()
        self._create_remote_user()
        self._save_profile_key()

    def _save_profile_key(self):
        profile_dir = os.path.join(settings.OPENACCESS_GATEONE_PROFILE_DIR,
                                   self.username, '.ssh')
        # TODO: do this properly
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)
        key_file = os.path.join(profile_dir, 'id_rsa')
        with open(key_file, 'w+') as f:
            f.write(self.key) 
        os.chmod(key_file, stat.S_IREAD | stat.S_IWRITE)
        pub_key_file = os.path.join(profile_dir, 'id_rsa.pub')
        with open(pub_key_file, 'w+') as f:
            f.write(self.get_public_key()) 
        os.chmod(key_file, stat.S_IREAD | stat.S_IWRITE)
        defaults_file = os.path.join(profile_dir, '.default_ids')
        with open(defaults_file, 'w+') as f:
            f.write("id_rsa\n") 
        os.chmod(key_file, stat.S_IREAD | stat.S_IWRITE)
 
    def _generate_key(self):
        rsa_key = RSA.generate(2048, os.urandom)
        self.key = rsa_key.exportKey()

    def get_public_key(self):
        key = RSA.importKey(self.key) 
        return key.exportKey('OpenSSH')

    def update_ssh_keys(self):
        # this is ugly as it gets, but it's the easier way right now
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys('/etc/ssh/ssh_known_hosts')
        ssh_port = getattr(settings, 'OPENACCESS_ANALYSIS_SSH_PORT', 22)
        ssh_user = getattr(settings, 'OPENACCESS_ANALYSIS_SSH_USER', 'root')
        ssh_cmd = getattr(settings, 'OPENACCESS_ANALYSIS_SSH_CMD',
                          '/var/cmsopendata/update_ssh_keys.sh')
        updated_keys = '\n'.join([self.get_public_key(), self.extra_keys])
        cmd_line = '%s %s "%s"' % (ssh_cmd, self.username, updated_keys) 
        ssh_client.connect(settings.OPENACCESS_ANALYSIS_SSH_HOST,
                           port=ssh_port, username=ssh_user,
                           key_filename=settings.OPENACCESS_ANALYSIS_SSH_KEY)
        channel = ssh_client.get_transport().open_session()
        channel.exec_command(cmd_line)
        status = channel.recv_exit_status()        

    def _create_remote_user(self):
        # this should be as async as possible
        # ERROR CHECKING MISSING!!
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys('/etc/ssh/ssh_known_hosts')
        ssh_port = getattr(settings, 'OPENACCESS_ANALYSIS_SSH_PORT', 22)
        ssh_user = getattr(settings, 'OPENACCESS_ANALYSIS_SSH_USER', 'root')
        ssh_cmd = getattr(settings, 'OPENACCESS_ANALYSIS_SSH_CMD',
                          '/var/cmsopendata/createuser.sh')
        cmd_line = '%s %s "%s"' % (ssh_cmd, self.username, self.get_public_key())
        ssh_client.connect(settings.OPENACCESS_ANALYSIS_SSH_HOST,
                           port=ssh_port, username=ssh_user,
                           key_filename=settings.OPENACCESS_ANALYSIS_SSH_KEY)
        channel = ssh_client.get_transport().open_session()
        channel.exec_command(cmd_line)
        status = channel.recv_exit_status()
