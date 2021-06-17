
FROM mesudip/nginx-proxy
ENV MODSECURITY_VERSION=3.0.4 \
    MODSECURITY_CONNECTOR_VERSION=1.0.1 \
    OWASP_MODSECURITY_RULE_VERSION=3.2.0
RUN apk add libstdc++ lua yajl\
    && apk add --no-cache --virtual .build-deps \
        curl \
        g++ \
        geoip-dev \
		automake \
		autoconf \
	    yajl-dev \
	    lmdb-dev \
	    lua-dev \
		libtool pcre-dev linux-headers make zlib-dev file \
    && curl -fSL https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz -o nginx.tar.gz \
	&& mkdir -p /usr/src \
	&& tar -zxC /usr/src -f nginx.tar.gz \
	&& rm nginx.tar.gz \
    && curl -fSL https://github.com/SpiderLabs/ModSecurity/releases/download/v${MODSECURITY_VERSION}/modsecurity-v${MODSECURITY_VERSION}.tar.gz -o modsecurity.tar.gz \
	&& tar -zxC /usr/src/ -f modsecurity.tar.gz \
	&& rm modsecurity.tar.gz \
	&& curl -fSL https://github.com/coreruleset/coreruleset/archive/v${OWASP_MODSECURITY_RULE_VERSION}.zip  -o coreruleset-${OWASP_MODSECURITY_RULE_VERSION}.zip \
	&& unzip -d /usr/src coreruleset-${OWASP_MODSECURITY_RULE_VERSION}.zip \
	&& rm -f coreruleset-${OWASP_MODSECURITY_RULE_VERSION}.zip \
	&& mkdir -p /etc/owasp \
    && mv /usr/src/coreruleset-${OWASP_MODSECURITY_RULE_VERSION}/crs-setup.conf.example /etc/owasp/crs-setup.conf \
	&& mv /usr/src/coreruleset-${OWASP_MODSECURITY_RULE_VERSION}/rules/ /etc/owasp/ \
    && apk add \
    && cd /usr/src/modsecurity-v${MODSECURITY_VERSION} \
	&& ./build.sh && ./configure && make && make install \
	&& mkdir -p /etc/nginx/modsec && mv modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf \
	&& sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/nginx/modsec/modsecurity.conf \
    && curl -fSL https://github.com/SpiderLabs/ModSecurity-nginx/releases/download/v${MODSECURITY_CONNECTOR_VERSION}/modsecurity-nginx-v${MODSECURITY_CONNECTOR_VERSION}.tar.gz -o modsecurity-nginx.tar.gz \
	&& tar -zxC /usr/src/ -f modsecurity-nginx.tar.gz \
	&& cd /usr/src/nginx-$NGINX_VERSION \
	&& ./configure --with-compat --add-dynamic-module=../modsecurity-nginx-v${MODSECURITY_CONNECTOR_VERSION} \
	&&  make modules && install -m755 ./objs/ngx_http_modsecurity_module.so /usr/lib/nginx/modules/ngx_http_modsecurity_module.so \
    && mv /usr/src/modsecurity-v${MODSECURITY_VERSION}/unicode.mapping /etc/nginx/modsec/unicode.mapping \
    && rm -rf /usr/src/* && apk del .build-deps 
    
COPY detection_script/detection.py /home/detection_script/detection.py
COPY detection_script/mailing.py /home/detection_script/mailing.py
COPY run.sh /home/detection_script/run.sh
COPY nginx-with-modsecurity.conf /etc/nginx/nginx.conf
COPY nginx-modsecurity.conf /etc/nginx/modsec/main.conf
COPY crs-setup.conf /etc/nginx/modsec/crs-setup.conf
