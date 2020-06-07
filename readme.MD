Move onapp-script.service to /etc/systemd/system so its not lost upon package updates.
systemctl daemon-reload
systemctl enable --now onapp-script.service
