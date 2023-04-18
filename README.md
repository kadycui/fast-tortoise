## 基于FastAPI + TortoiseORM的后台系统



### 数据迁移
进入到aerich文件夹
```
aerich init -t env.TORTOISE_ORM 
```
会生成`migrations`文件夹和`pyproject.toml`文件

```
aerich init-db
```
`migrations`文件夹下生成`models`文件夹,其中是SQL文件类似于`0_20220812225242_init.sql`

此操作会连接数据库

### 更新操作
```
# 重新生成SQL语句：aerich migrate 
aerich migrate
    
# 把新生成的SQL推送到数据库
aerich upgrade
```

### 回退版本
```
# 回到上一个版本
aerich downgrade

```

### 其他操作
```
# 查看历史迁移记录
aerich history


# 查看形成当前版本的迁移记录文件
aerich heads

```