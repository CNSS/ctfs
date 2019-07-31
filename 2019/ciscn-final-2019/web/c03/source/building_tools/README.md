# 源码目录说明

## 目录结构
1. frontend -- 前端代码目录
2. backend -- 后端代码目录
3. building_tools -- 前后端的构建环境

  - 前端：NodeJs 10
  - 后端：JDK1.8，Apache Maven 3.6.1

4. 构建方式：

  - 前端：

    1. 安装依赖

    ```
    npm install
    ```

    2. 构建

    ```
    npm run build
    ```

    3. dist 文件下即为构建好的前端文件
    4. 将构建好的文件拷贝到后端的 src/main/resources/static

  - 后端:

    1. 构建

    ```
    mvn package
    ```

    2. target/*-SNAPSHOT.jar 即为构建好的文件。
