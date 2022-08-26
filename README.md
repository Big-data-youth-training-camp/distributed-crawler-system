# 分布式爬虫系统

## 简介：
#### 整个分布式系统被配置到docker容器中。通过多进程来模拟多机爬虫，实现伪分布。通过docker我们能够更快，更高效的部署分布式系统，并维持一致的开发环境。爬虫方面，我们用到了beautifulsoup和request模块。Python脚本爬取的数据会通过kafka消息队列传输给java通过flink调度存储数据。最后为用户提供查询数据的借口。在此过程中凭借thrift进行python端和java端的RPC。
<br>
<br>

## docker及环境配置
<br>

#### 在文件夹（流式计算框架）中，介绍了我们环境配置到docker中的基本方法。[点击此处](https://hub.docker.com/repository/docker/879314144/distributed_crawler)获取我们在docker中的镜像。

#### docker拉去项目： docker pull 879314144/distributed_crawler:v1


