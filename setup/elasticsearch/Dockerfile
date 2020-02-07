# ubuntu 설치
FROM ubuntu:16.04
RUN apt-get update && apt-get install -y vim && apt-get install -y git && apt-get install -y wget

# WORKDIR
WORKDIR /usr/src/git/elasticsearch

# open jdk 11 설치
RUN wget https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_linux-x64_bin.tar.gz
RUN tar vxfz openjdk-11+28_linux-x64_bin.tar.gz
RUN rm openjdk-11+28_linux-x64_bin.tar.gz
RUN mv jdk-11/ /usr/share
ENV export JAVA_HOME /usr/share/jdk-11
RUN export JAVA_HOME
#ENV export PATH $PATH:$JAVA_HOME/bin
#RUN export PATH
# 안되면 source에 밀어넣자

# gin clone 할것
