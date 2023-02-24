>如何执行？
- 
本地执行步骤
1. 修改config.server_info 中的ip即可，数据库密码通过已提供方法查询
2. copy起流服务器的test.conf文件替换config.business中的test.conf，并修改config.server_info中的file_path
3. 运行pytest-run.py


服务器执行
1. 修改ip
2. 修改config.server_info中的file_path为固定目录：/mnt/openebs/test/test.con
3. 运行pytest-run.py

>本地文件夹
1. 生成报告需要在本地创建reports 和temp 文件夹

