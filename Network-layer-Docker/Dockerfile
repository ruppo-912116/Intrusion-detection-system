FROM ubuntu

MAINTAINER sagar dangal <ragaslagnad28@gmail.com>

RUN apt-get update


RUN apt update \

	&& apt install -y apt-transport-https ca-certificates wget dirmngr gnupg software-properties-common  \
	
	&& wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public |  apt-key add - \

	&& add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ \

	&& apt update \

	&& apt -y install adoptopenjdk-8-hotspot \
	
	&& apt update \
	
	&& apt -y install sysvbanner \

	&& apt -y install git \

	&& apt-get -y install python3-pip \

	&& pip3 install grpcio grpcio-tools \

	&& pip3 install pandas \

	&& pip3 install sklearn \

	&& apt update \

	&& git clone https://git.sireto.io/Dangal/flowmeter.git \

	&& cd flowmeter \
	
	&& chmod +x run.sh \

	&& apt-get install gradle -y \

	&& apt -y install maven \

	&& cd jnetpcap/linux/jnetpcap-1.4.r1425 \

	&& apt-get install -y libpcap-dev \

	&& mvn install:install-file -Dfile=jnetpcap.jar -DgroupId=org.jnetpcap -DartifactId=jnetpcap -Dversion=1.4.1 -Dpackaging=jar \

	&& cd ../../.. \

	&& apt update

