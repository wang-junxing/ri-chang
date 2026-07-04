
```
# 列出所有磁盘，找到你的外置硬盘分区（disk2s1/disk3s1）
diskutil list
# 查看分区详细信息，复制 Volume UUID
diskutil info /dev/disk2s1
```

# mac config
```
~$:cat /etc/exports
/Users/xxx/Documents/USBDisk/nfs -alldirs -maproot=root -network 192.168.6.0 -mask 255.255.255.0

~$:cat /etc/fstab
UUID=C5A2169F-4569-4149-A7C5-1B1C6716EF99 /Users/xxx/Documents/USBDisk apfs rw,auto,nobrowse
~$:
```

# linux config
```
cat /etc/fstab
192.168.6.108:/Users/xxx/Documents/USBDisk/nfs  /media/nfs  nfs  rw,_netdev,noatime  0  0
```

# .env
下面是 immich 具体的配置
```
root@vbox:/media/nfs/immich-app# cat .env
# You can find documentation for all the supported env variables at https://docs.immich.app/install/environment-variables

# The location where your uploaded files are stored
UPLOAD_LOCATION=./library

# The location where your database files are stored. Network shares are not supported for the database
DB_DATA_LOCATION=./postgres

# To set a timezone, uncomment the next line and change Etc/UTC to a TZ identifier from this list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
# TZ=Etc/UTC

# The Immich version to use. You can pin this to a specific version like "v2.1.0"
IMMICH_VERSION=v3

# Connection secret for postgres. You should change it to a random password
# Please use only the characters `A-Za-z0-9`, without special characters or spaces
DB_PASSWORD=postgres

# The values below this line do not need to be changed
###################################################################################
DB_USERNAME=postgres
DB_DATABASE_NAME=immich
# 新增这一行（3.0强制向量引擎）
DB_VECTOR_EXTENSION=vectorchord

MACHINE_LEARNING_PRELOAD__FACIAL_RECOGNITION__DETECTION=buffalo_l
MACHINE_LEARNING_PRELOAD__FACIAL_RECOGNITION__RECOGNITION=buffalo_l
#MACHINE_LEARNING_PRELOAD__CLIP__VISUAL=XLM-Roberta-Large-Vit-B-16Plus
# 注释原有整行，替换为下面这句
MACHINE_LEARNING_PRELOAD_MODELS=facial-recognition
```

# docker-compose.yml 
```
root@vbox:/media/nfs/immich-app# cat docker-compose.yml 
#
# WARNING: To install Immich, follow our guide: https://docs.immich.app/install/docker-compose
#
# Make sure to use the docker-compose.yml of the current release:
#
# https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml
#
# The compose file on main may not be compatible with the latest release.

name: immich

services:
  immich-server:
    container_name: immich_server
    image: ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}
    # extends:
    #   file: hwaccel.transcoding.yml
    #   service: cpu # set to one of [nvenc, quicksync, rkmpp, vaapi, vaapi-wsl] for accelerated transcoding
    volumes:
      # Do not edit the next line. If you want to change the media storage location on your system, edit the value of UPLOAD_LOCATION in the .env file
      - ${UPLOAD_LOCATION}:/data
      - /etc/localtime:/etc/localtime:ro
    env_file:
      - .env
    ports:
      - '2283:2283'
    depends_on:
      - redis
      - database
    restart: always
    healthcheck:
      disable: false

  immich-machine-learning:
    container_name: immich_machine_learning
    # For hardware acceleration, add one of -[armnn, cuda, rocm, openvino, rknn] to the image tag.
    # Example tag: ${IMMICH_VERSION:-release}-cuda
    image: ghcr.io/immich-app/immich-machine-learning:${IMMICH_VERSION:-release}
    # extends: # uncomment this section for hardware acceleration - see https://docs.immich.app/features/ml-hardware-acceleration
    #   file: hwaccel.ml.yml
    #   service: cpu # set to one of [armnn, cuda, rocm, openvino, openvino-wsl, rknn] for accelerated inference - use the `-wsl` version for WSL2 where applicable
    volumes:
      - ./immich-models:/cache
    env_file:
      - .env
    restart: always
    healthcheck:
      disable: false

  redis:
    container_name: immich_redis
    image: docker.io/valkey/valkey:9
    healthcheck:
      test: redis-cli ping || exit 1
    restart: always

  database:
    container_name: immich_postgres
    image: ghcr.io/immich-app/postgres:14-vectorchord0.4.3-pgvectors0.2.0
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_USER: ${DB_USERNAME}
      POSTGRES_DB: ${DB_DATABASE_NAME}
      POSTGRES_INITDB_ARGS: '--data-checksums'
      # Uncomment the DB_STORAGE_TYPE: 'HDD' var if your database isn't stored on SSDs
      # DB_STORAGE_TYPE: 'HDD'
    volumes:
      # Do not edit the next line. If you want to change the database storage location on your system, edit the value of DB_DATA_LOCATION in the .env file
      - ${DB_DATA_LOCATION}:/var/lib/postgresql/data
    shm_size: 128mb
    restart: always
    healthcheck:
      disable: false
```

# docker proxy configuration
```
root@vbox:/media/nfs/immich-app# cat /etc/systemd/system/docker.service.d/proxy.conf 

[Service]
Environment="HTTP_PROXY=http://192.168.6.108:58591"
Environment="HTTPS_PROXY=http://192.168.6.108:58591"
Environment="ALL_PROXY=socks5://192.168.6.108:51837"
Environment="NO_PROXY=localhost,127.0.0.1,172.17.0.0/16"
```