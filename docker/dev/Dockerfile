#  Licensed to the Apache Software Foundation (ASF) under one   *
#  or more contributor license agreements.  See the NOTICE file *
#  distributed with this work for additional information        *
#  regarding copyright ownership.  The ASF licenses this file   *
#  to you under the Apache License, Version 2.0 (the            *
#  "License"); you may not use this file except in compliance   *
#  with the License.  You may obtain a copy of the License at   *
#                                                               *
#    http://www.apache.org/licenses/LICENSE-2.0                 *
#                                                               *
#  Unless required by applicable law or agreed to in writing,   *
#  software distributed under the License is distributed on an  *
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY       *
#  KIND, either express or implied.  See the License for the    *
#  specific language governing permissions and limitations      *
#  under the License.                                           *

FROM python:2.7-jessie

# install deps
RUN apt-get update -y && apt-get install -y \
        wget \
        python3-dev \
        libcurlpp-dev \
        curl \
        libssl-dev \
        git \
        inetutils-telnet \
        bind9utils \
        zip \
        unzip \
    && apt-get clean



# Since we install vanilla Airflow, we also want to have support for Postgres and Kubernetes
RUN pip install kubernetes && \
    pip install cryptography && \
    pip install psycopg2-binary #==2.7.4  # I had issues with older versions of psycopg2, just a warning

COPY . /airflow

RUN cd /airflow && \
    pip install -e .[devel_all]
