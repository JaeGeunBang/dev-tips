# ubuntu 16.04 설치
FROM ubuntu:16.04
RUN apt-get update && apt-get install -y vim && apt-get install -y git && apt-get install -y wget

# WORKDIR
WORKDIR /usr/src/git/elasticsearch

# open jdk 13 설치
RUN wget https://download.java.net/java/GA/jdk13.0.2/d4173c853231432d94f001e99d882ca7/8/GPL/openjdk-13.0.2_linux-x64_bin.tar.gz
RUN tar vxfz openjdk-13.0.2_linux-x64_bin.tar.gz
RUN rm openjdk-13.0.2_linux-x64_bin.tar.gz
RUN mv jdk-13.0.2/ /usr/share

# 환경 변수 설정
RUN echo 'export JAVA_HOME=/usr/share/jdk-13.0.2' >> ~/.bashrc
RUN echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"