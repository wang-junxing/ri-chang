### 打开我的电脑-属性-远程设置

1. 勾选“允许远程协助连接这台计算机(R)”
2. 勾选“允许远程连接到此计算机(L)”

这样局域网就能够远程控制这台电脑了

##### 意点：受控电脑需要设置用户名密码

### 如果想在外网控制这台电脑

1. 需要在路由器中设置端口转发
2. 如果受控电脑开启了防火墙,需要在受控电脑上添加防火墙放行规则,或者关闭防火墙（不建议）

### 如果想修改远程控制端口(为安全起见)

可以通过我提供的脚本方便的修改

```bat
::以下代码保存为 XXX.bat 双击运行即可
::win默认远程桌面端口号3389
::远程桌面端口号1024-65535

set rdpPort=3333

netsh advfirewall firewall add rule name="allow rdp out" dir=out protocol=tcp localport=%rdpPort% action=allow
netsh advfirewall firewall add rule name="allow rdp in" dir=in protocol=tcp localport=%rdpPort% action=allow

reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v PortNumber /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v PortNumber /t reg_dword /d %rdpPort% /f

reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\Wds\rdpwd\Tds\tcp" /v PortNumber /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\Wds\rdpwd\Tds\tcp" /v PortNumber /t reg_dword /d %rdpPort% /f
```

