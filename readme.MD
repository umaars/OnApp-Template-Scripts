Move onapp-script.service to sudo /lib/systemd/system/
systemctl daemon-reload
systemctl enable --now onapp-script.service
