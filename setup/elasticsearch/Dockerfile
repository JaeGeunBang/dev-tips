FROM ubuntu:16.04
RUN apt-get update && apt-get install -y vim && apt-get install -y git && apt-get install -y wget && apt-get install -y gradle

# WORKDIR & git clone
#RUN mkdir -p /usr/src/git/ && cd /usr/src/git
#RUN git clone https://github.com/JaeGeunBang/elasticsearch
WORKDIR /usr/src/git/elasticsearch

# open jdk 11 설치
RUN wget https://download.java.net/openjdk/jdk11/ri/openjdk-11+28_linux-x64_bin.tar.gz
RUN tar vxfz openjdk-11+28_linux-x64_bin.tar.gz
RUN rm openjdk-11+28_linux-x64_bin.tar.gz
RUN mv jdk-11/ /usr/share

# 환경 변수 설정
RUN echo 'export JAVA_HOME=/usr/share/jdk-11' >> ~/.bashrc
RUN echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

# 빌드
#RUN cd /usr/src/git/elasticsearch
#RUN ./gradlew assemble
